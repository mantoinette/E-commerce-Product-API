from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            # Admin
            ("can_manage_everything", "Can manage everything in the system"),

            # Product Manager Permissions
            ("can_manage_products", "Can manage products (add, edit, delete)"),

            # Content Editor Permissions
            ("can_edit_content", "Can edit content but cannot delete"),

            # Sales Manager Permissions
            ("can_manage_discounts", "Can manage discounts"),
            ("can_manage_orders", "Can manage orders"),
            ("can_manage_customers", "Can manage customer information"),

            # Customer Support Permissions
            ("can_view_customer_info", "Can view customer information"),
            ("can_assist_issues", "Can assist with customer issues"),
            ("can_view_orders", "Can view orders"),

            # Viewer Permissions
            ("can_read_only", "Can only view data"),

            # Marketing Permissions
            ("can_manage_promotions", "Can manage promotions and discounts"),
            ("can_manage_product_visibility", "Can manage product visibility"),

            # Warehouse Manager Permissions
            ("can_manage_inventory", "Can manage inventory"),
            ("can_update_product_quantity", "Can update product quantity"),
        ]


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("can_view_category", "Can view category"),
        ]


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def reduce_stock(self, quantity):
        """
        Reduces the stock quantity when an order is placed.
        Returns True if successful, False if insufficient stock.
        """
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False

    class Meta:
        permissions = [
            # Warehouse Manager Permissions
            ("can_manage_inventory", "Can manage inventory"),
            ("can_update_product_quantity", "Can update product quantity"),

            # Marketing Permissions
            ("can_manage_product_visibility", "Can manage product visibility"),

            # Viewer Permissions for Product
            ("can_view_product", "Can view product"),
        ]


# Order Model
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    class Meta:
        permissions = [
            # Sales Manager Permissions for Order
            ("can_manage_orders", "Can manage orders"),

            # Viewer Permissions for Order
            ("can_view_order", "Can view order"),
        ]


class SomeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
