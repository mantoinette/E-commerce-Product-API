from django.urls import path
from . import views

urlpatterns = [
    # API - User management URLs
    path('api/v1/users/', views.UserList.as_view(), name='user-list'),  # List all users
    path('api/v1/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),  # Retrieve a specific user
    path('api/v1/users/create/', views.UserCreate.as_view(), name='user-create'),  # Create a new user
    path('api/v1/users/update/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),  # Update user details
    path('api/v1/users/delete/<int:pk>/', views.UserDelete.as_view(), name='user-delete'),  # Delete a user

    # API - Product management URLs
    path('api/v1/products/', views.ProductList.as_view(), name='product-list'),  # List and search products
    path('api/v1/products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),  # Retrieve product details
    path('api/v1/products/create/', views.ProductCreate.as_view(), name='product-create'),  # Create a new product
    path('api/v1/products/update/<int:pk>/', views.ProductUpdate.as_view(), name='product-update'),  # Update a product
    path('api/v1/products/delete/<int:pk>/', views.ProductDelete.as_view(), name='product-delete'),  # Delete a product
    
    # Frontend - Authentication URLs
    path('', views.home, name='home'),  # Home view
    path('products/', views.product_list, name='product-list'),  # Product listing view
    path('order/create/', views.make_order, name='make-order'),  # Create a new order
    path('order/edit/<int:order_id>/', views.edit_order, name='edit-order'),  # Edit an existing order
    path('order/delete/<int:order_id>/', views.delete_order, name='delete-order'),  # Delete an order
    path('signup/', views.signup, name='signup'),  # User signup
    path('login/', views.login_view, name='login'),  # User login

    # Frontend - User Dashboard
    path('dashboard/', views.user_dashboard, name='user-dashboard'),  # User dashboard
]
