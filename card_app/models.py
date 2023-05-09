from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from product_app.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username}'s cart with {self.quantity} {self.product.name}(s)"

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity should be greater than or equal to 0')
        if not User.objects.filter(id=self.user.id).exists():
            raise ValidationError('User not found')
        if not Product.objects.filter(id=self.product.id).exists():
            raise ValidationError('Product not found')
        if self.product.quantity < self.quantity:
            raise ValidationError('Not enough products available')

    def save(self, *args, **kwargs):
        self.total_amount = self.product.price * self.quantity
        super().save(*args, **kwargs)