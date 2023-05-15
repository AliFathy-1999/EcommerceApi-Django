from django.db import models
from django.contrib.auth import get_user_model
from user_app.models import Address
from product_app.models import Product

from django.core.validators import MinValueValidator
User = get_user_model()

class Order(models.Model):
    # additional note to Model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders',through='OrderItem')
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    orderDate = models.DateTimeField(auto_now_add=True)
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'pending'),
        ('SHIPPED', 'shipped'),
        ('DELIVERED', 'delivered'),
    ]
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default=("Pending"),
    )
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.user.username}'s order is ordered at {(self.orderDate).strftime('%Y-%m-%d %H:%M:%S')} and order status is {self.status}"    
    
class OrderItem(models.Model):
    # Orderitem(orderId,productid,price,quantity)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])     
    def __str__(self):
        return f"{self.order} | {self.product} | {self.price} | {self.quantity}"    