from django.db import models
from django.core.validators import RegexValidator,FileExtensionValidator,MinValueValidator
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=40,unique=True,db_index=True,
    validators=[RegexValidator(regex='[a-zA-Z\s]+$', message='Field must contain only alphabetic characters', code='invalid_alpha')])
    categoryPic = models.ImageField(upload_to='static', blank=True, null=True,validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    def __str__(self):
        return self.name
# Category Product Model
class Product(models.Model):
    name = models.CharField(
    unique=True,
    max_length=40,
    db_index=True,
    validators=[RegexValidator(regex='[a-zA-Z]+', message='Field must contain at least one alphabetic characters', code='invalid_alpha')]
    )
    description = models.CharField(max_length=255,  null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    productPic = models.ImageField(upload_to='static',null=False, blank=False)
    avgRating = models.DecimalField(max_digits=4, decimal_places=2 ,default=0.0)
    quantity = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name