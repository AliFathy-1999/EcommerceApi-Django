from django.contrib import admin
from product_app.models import Category,Product
from django.contrib.admin.sites import AlreadyRegistered
from django.apps import apps
app_models = apps.get_app_config('product_app').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
