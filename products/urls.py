from django.urls import path
from .views import (MaterialAPIView, ProductListAPIView, ProductDetailAPIView,
                    FilterListAPIView, CategoryAPIView,
                    ProductReviewAPIViewSet, WishlistModelViewSet,
                    AddToCartAPIView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reviews', ProductReviewAPIViewSet, basename='product-reviews')
router.register('wishlist', WishlistModelViewSet, basename='wishlist')

urlpatterns = [
    path('category_list/', CategoryAPIView.as_view(), name='category-list'),
    path('<int:pk>/material_list/',
         MaterialAPIView.as_view(), name='material_list'),
    path('product_list/',
         ProductListAPIView.as_view(), name='product-list'),
    path('product_detail/<int:pk>/',
         ProductDetailAPIView.as_view(), name='product-detail'),
    path('filter-list/', FilterListAPIView.as_view(), name='filter-list'),

    path('add_to_cart', AddToCartAPIView.as_view(), name='add_to_cart')
]
urlpatterns += router.urls
