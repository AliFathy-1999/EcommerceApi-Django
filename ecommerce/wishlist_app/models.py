from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from product_app.models import Product

User = get_user_model()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username}'s wishlist with {self.product.name}"

    def clean(self):
        if not User.objects.filter(id=self.user.id).exists():
            raise ValidationError('User not found')
        if not Product.objects.filter(id=self.product.id).exists():
            raise ValidationError('Product not found')

    class Meta:
        unique_together = ('user', 'product',)