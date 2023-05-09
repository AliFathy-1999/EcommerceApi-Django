from django.db import models
from user_app.models import User
from product_app.models import Product
from django.core.exceptions import ValidationError

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s cart with {self.quantity} {self.product.name}(s)"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity should be greater than 0')
        if not User.objects.filter(id=self.user.id).exists():
            raise ValidationError('User not found')
        if not Product.objects.filter(id=self.product.id).exists():
            raise ValidationError('Product not found')

    def save(self, *args, **kwargs):
        product = self.product
        if product.quantity < self.quantity:
            raise ValidationError('Not enough products available')
        self.total_price = product.price * self.quantity
        super().save(*args, **kwargs)