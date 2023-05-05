from django.urls import path,include
from product_app.api.views import * 

urlpatterns = [
    # Category URLs
    path('categories/',get_categories,name="categories"),
    path('category/<int:pk>',category_details,name="category_details"),
    path('category/',create_category,name="create_category"),
    path('category/update/<int:pk>',update_category,name="update_category"),
    path('category/delete/<int:pk>',deleted_category,name="deleted_category"),
    # Product URLs
    path('products/',get_products,name="products"),
    path('<int:pk>/',product_details,name="product_details"),
    path('product/',create_product,name="create_product"),
    path('update/<int:pk>',update_product,name="update_product"),
    path('delete/<int:pk>',deleted_product,name="deleted_product"),
]
