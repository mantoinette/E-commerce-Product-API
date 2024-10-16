from django.urls import path
from . import views

urlpatterns = [
    # User management URLs
    path('api/v1/users/', views.UserList.as_view(), name='user-list'),
    path('api/v1/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/v1/users/create/', views.UserCreate.as_view(), name='user-create'),
    path('api/v1/users/update/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),
    path('api/v1/users/delete/<int:pk>/', views.UserDelete.as_view(), name='user-delete'),

    # Product management URLs
    path('api/v1/products/', views.ProductList.as_view(), name='product-list'),  # List and search products
    path('api/v1/products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),  # Product detail
    path('api/v1/products/create/', views.ProductCreate.as_view(), name='product-create'),  # Create a product
    path('api/v1/products/update/<int:pk>/', views.ProductUpdate.as_view(), name='product-update'),  # Update a product
    path('api/v1/products/delete/<int:pk>/', views.ProductDelete.as_view(), name='product-delete'),  # Delete a product
    

    # Authentication URLs
    path('', views.home, name='home'),  # Home view
    path('products/', views.product_list, name='product-list'),  # Product list view
    path('make-order/', views.make_order, name='make-order'),  # Order creation (Updated URL name)
    path('edit-order/<int:order_id>/', views.edit_order, name='edit-order'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete-order'),
    path('signup/', views.signup, name='signup'),  # Signup view
    path('login/', views.login_view, name='login'),  # Login view

    # User dashboard
    path('dashboard/', views.user_dashboard, name='user-dashboard'),  # User dashboard
   
]

