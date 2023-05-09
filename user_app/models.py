from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
       
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=100)
    street_no = models.CharField(max_length=10)
    government = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    house_no = models.CharField(max_length=10)
    apartment_no = models.CharField(max_length=10, blank=True, null=True)
    floor_no = models.CharField(max_length=10, blank=True, null=True)
    additional_info = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s address"

    def clean(self):
        """
        Check if the address fields are valid.
        """
        if not isinstance(self.street_name, str):
            raise ValidationError("Street name must be a string.")
        if len(self.street_name) < 2 or len(self.street_name) > 100:
            raise ValidationError("Street name length must be between 2 and 100 characters.")
        if not self.street_name:
            raise ValidationError("Street name cannot be empty.")
        if any(char.isdigit() for char in self.street_name):
            raise ValidationError("Street name cannot contain numbers.")

        if not isinstance(self.street_no, str):
            raise ValidationError("Street number must be a string.")
        if len(self.street_no) < 1 or len(self.street_no) > 10:
            raise ValidationError("Street number length must be between 1 and 10 characters.")

        if not isinstance(self.government, str):
            raise ValidationError("Government must be a string.")
        if len(self.government) < 2 or len(self.government) > 100:
            raise ValidationError("Government length must be between 2 and 100 characters.")
        if not self.government:
            raise ValidationError("Government cannot be empty.")
        if any(char.isdigit() for char in self.government):
            raise ValidationError("Government cannot contain numbers.")

        if not isinstance(self.district, str):
            raise ValidationError("District must be a string.")
        if len(self.district) < 2 or len(self.district) > 100:
            raise ValidationError("District length must be between 2 and 100 characters.")

        if not isinstance(self.house_no, str):
            raise ValidationError("House number must be a string.")
        if len(self.house_no) < 1 or len(self.house_no) > 10:
            raise ValidationError("House number length must be between 1 and 10 characters.")

        if self.apartment_no and not isinstance(self.apartment_no, str):
            raise ValidationError("Apartment number must be a string.")
        if self.apartment_no and (len(self.apartment_no) < 1 or len(self.apartment_no) > 10):
            raise ValidationError("Apartment number length must be between 1 and 10 characters.")

        if self.floor_no and not isinstance(self.floor_no, str):
            raise ValidationError("Floor number must be a string.")
        if self.floor_no and (len(self.floor_no) < 1 or len(self.floor_no) > 10):
            raise ValidationError("Floor number length must be between 1 and 10 characters.")

        if self.additional_info and not isinstance(self.additional_info, str):
            raise ValidationError("Additional info must be a string.")
        if self.additional_info and len(self.additional_info) > 500:
            raise ValidationError("Additional info length must be less than or equal to 500 characters.")