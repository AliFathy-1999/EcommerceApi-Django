from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator, MaxLengthValidator

class User(AbstractBaseUser):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10, validators=[MinLengthValidator(8), MaxLengthValidator(10)])
    profilePic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.email

    
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
        
        
