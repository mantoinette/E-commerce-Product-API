from django.urls import path
from . import views

urlpatterns = [
    # User management URLs
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/create/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/update/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),
    path('api/users/delete/<int:pk>/', views.UserDelete.as_view(), name='user-delete'),
    
    # Product management URLs
    path('api/products/', views.ProductList.as_view(), name='product-list'),  # List and search products
    path('api/products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),  # Product detail
    path('api/products/create/', views.ProductCreate.as_view(), name='product-create'),  # Create a product
    path('api/products/update/<int:pk>/', views.ProductUpdate.as_view(), name='product-update'),  # Update a product
    path('api/products/delete/<int:pk>/', views.ProductDelete.as_view(), name='product-delete'),  # Delete a product
]
