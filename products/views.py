
from django.db.models.aggregates import Count, Max, Min, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Category, Detail, Material, Product, Review, WishlistItem
from .serializers import (CategorySerilaizer, WishlistItemSerializer,
                          ProductListSerializer, ProductDetailSerializer,
                          MaterialSerilaizer, ReviewSerializer)
from .filters import ProductFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import json


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related("details").all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class FilterListAPIView(APIView):
    def get(self, request):
        materials = Material.objects.all().values_list('name', flat=True)
        details = Detail.objects.all()
        types = details.values_list('type', flat=True).distinct()
        lengths = details.values_list('size__length', flat=True).distinct()
        widths = details.values_list('size__width', flat=True).distinct()
        heights = details.values_list('size__height', flat=True).distinct()
        prices = details.values_list(
            'price').aggregate(min=Min('price'), max=Max('price'),
                               count=Count('price'), avg=Avg('price'))

        prices_ranges = []
        diff = prices['max']-prices['min']

        for i in range(prices['count']):
            avg = diff/prices['count']
            if i == 0:
                prices_ranges.append(prices['min'])
                value = prices['min']

            value += avg
            prices_ranges.append(value)
        prices_ranges_v2 = []
        for i in range(len(prices_ranges)):
            try:
                prices_ranges_v2.append({'min_price': prices_ranges[i],
                                         'max_price': prices_ranges[i+1]})
            except Exception:
                break

        return Response({'materials': materials,
                         'types': types,
                        'lengths': lengths,
                         'widths': widths,
                         'heights': heights,
                         'prices': prices,
                         'prices_ranges': prices_ranges,
                         'prices_ranges_v2': prices_ranges_v2,
                         })


class CategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerilaizer


class MaterialAPIView(APIView):
    def get(self, request, pk):
        query_set = Material.objects.filter(category__id=pk)
        serializer = MaterialSerilaizer(query_set, many=True)
        return Response(serializer.data)


class ProductReviewAPIViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.request.
                                     query_params.get('product_pk'))

    def get_serializer_context(self, **kwargs):
        return {'user_id': self.request.user.id}


class WishlistModelViewSet(ModelViewSet):
    serializer_class = WishlistItemSerializer

    def get_queryset(self):
        user = self.request.user
        return WishlistItem.objects.filter(user=user)

    def get_serializer_context(self, **kwargs):
        return {'user_id': self.request.user.id}


class AddToCartAPIView(APIView):
    def post(self, request):

        product_ids = request.data['products'].split(',')
        quantities = request.data['quantities'].split(',')
        sizes = request.data['sizes'].split(',')

        cart = []
        id_unique = {}
        total_price = 0
        for index, product_id in enumerate(product_ids):

            try:
                product = Product.objects.get(pk=product_id)
                product_detail = Detail.objects.get(
                    product=product_id, size=sizes[index])

            except Exception:
                continue

            if product_id in id_unique.keys():
                id_index = id_unique[product_id]
                cart[id_index]['quantity'] += int(quantities[index])
                total_price += (float(product_detail.price)
                                - (float(product_detail.price)
                                   * float(product_detail.discount_in_precentage/100)))\
                    * float(quantities[index])

            else:
                product_dict = {'product_id': product_id,
                                'product_name': product.name,
                                'quantity': int(quantities[index]),
                                'product_original_price':
                                float(product_detail.price),
                                'discount':
                                float(product_detail.price) *
                                float(product_detail.discount_in_precentage/100),
                                'unit_price_after_discount':
                                    float(product_detail.price) -
                                (float(product_detail.price)
                                        * float(product_detail.discount_in_precentage/100)),
                                'product_size': str(product_detail.size),
                                'out_of_stock': (product_detail.quantity > quantities[index])
                                }

                cart.append(product_dict)
                id_unique[product_id] = index

                total_price += product_dict['unit_price_after_discount'] * \
                    float(product_dict['quantity'])

        cart.append({'total_price': total_price})
        return Response(cart)
        # return Response('Hi')
