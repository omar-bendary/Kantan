from django.contrib import admin
from .models import (Category, Product, Image,
                     Detail, Material, Size, Review, WishlistItem)


class ProductDetailInline(admin.StackedInline):
    model = Detail
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'material']
    inlines = [ProductDetailInline]


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['product',  'price']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['product']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'length', 'width', 'height', ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'rate']


@admin.register(WishlistItem)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
