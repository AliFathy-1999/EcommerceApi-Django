from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40,unique=True,db_index=True)
    categoryPic = models.ImageField(upload_to='static', blank=True, null=True)
    def __str__(self):
        return self.name
    def clean(self):
        if not self.name.isalpha():
            raise ValidationError("Category name must be a Alphabetic.")
        if len(self.name) < 3 or len(self.name) > 40:
            raise ValidationError("Category name length must be between 3 and 40 characters.")

        