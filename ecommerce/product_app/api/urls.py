from django.urls import path,include
from product_app.api.views import * 

urlpatterns = [
    path('categories/',get_categories,name="categories"),
    path('<int:pk>',category_details,name="category_details"),
    path('category/',create_category,name="create_category"),
    path('update/<int:pk>',update_category,name="update_category"),
    path('delete/<int:pk>',deleted_category,name="deleted_category"),
]
