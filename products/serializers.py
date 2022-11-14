from itertools import count
from rest_framework import serializers
from django.db.models.aggregates import Min, Sum, Avg
from .models import Category, Image, Material, Product, Detail, Review, WishlistItem


class ProductListSerializer(serializers.ModelSerializer):
    start_from = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()

    def get_average_rate(self, obj):
        avgerage_rate = Review.objects.filter(product_id=obj.id)\
            .aggregate(value=Avg('rate'))

        return avgerage_rate['value']

    def get_start_from(self, obj):
        product = Product.objects.get(id=obj.id)
        detail = Detail.objects.filter(
            product=product).aggregate(strat_from=Min('price'))

        return detail['strat_from']

    class Meta:
        model = Product
        fields = ['id', 'name', 'main_image', 'start_from', 'average_rate']


class DetailSerializer(serializers.ModelSerializer):
    dimensions = serializers.SerializerMethodField()
    price_after_discount = serializers.SerializerMethodField()

    def get_dimensions(self, obj):
        return f"{obj.size.length} x {obj.size.width} x {obj.size.height}"

    def get_price_after_discount(self, obj):
        discount = (obj.price * obj.discount_in_precentage/100)
        price_after_discount = (obj.price-discount)

        return price_after_discount

    class Meta:
        model = Detail
        fields = ['id', 'dimensions', 'price',
                  'price_after_discount', 'quantity', 'type']


class ExtraImageSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    details = DetailSerializer(many=True)
    extra_images = ExtraImageSerilaizer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'main_image',
                  'description', 'details', 'extra_images']


class MaterialSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name']


class FilterDetialProducts(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ['type', 'length', 'width', 'height', 'price']


class FilterListSerilaizer(serializers.Serializer):
    materials = serializers.SerializerMethodField()

    def get_materials(self, obj):
        materials = Material.objects.all()
        serializers = MaterialSerilaizer(materials, many=True)
        return serializers.data


class CategorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'description', 'rate']
        read_only_fields = ('user',)

    def save(self, **kwargs):
        Review.objects.create(
            product=self.validated_data['product'],
            user_id=self.context['user_id'],
            description=self.validated_data['description'],
            rate=self.validated_data['rate'])


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ['id', 'user', 'product']
        read_only_fields = ('user',)

    def save(self, **kwargs):
        WishlistItem.objects.create(
            product=self.validated_data['product'], user_id=self.context['user_id'])
