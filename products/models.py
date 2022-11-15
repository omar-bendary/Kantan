from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from decimal import Decimal
from uuid import uuid4


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return self.name


class Product(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    main_image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Size(models.Model):
    length = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.length} X {self.width} X {self.height}"


class Detail(models.Model):
    ADULT_TYPE = 'Adult'
    KIDS_TYPE = 'Kids'
    TYPE_CHOICES = [
        (ADULT_TYPE, 'Adult'),
        (KIDS_TYPE, 'Kids'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='details')
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, related_name='detail_item')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    discount_in_precentage = \
        models.DecimalField(max_digits=3,  decimal_places=0, default=Decimal(
            0), validators=PERCENTAGE_VALIDATOR)
    type = models.CharField(
        max_length=5, choices=TYPE_CHOICES, default=ADULT_TYPE)

    def __str__(self):
        return self.product.name


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField()

    def __str__(self):
        return self.product.name


class Review(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    description = models.TextField()
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])


class WishlistItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'user',)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['product', 'cart']]
