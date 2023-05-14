from django.contrib import admin
from order_app.models import Order
from django.contrib.admin.sites import AlreadyRegistered
from django.apps import apps
app_models = apps.get_app_config('order_app').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
