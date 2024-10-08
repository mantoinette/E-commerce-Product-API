from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            # Sales Manager Permissions
            ("can_manage_discounts", "Can manage discounts"),
            ("can_manage_orders", "Can manage orders"),
            ("can_manage_customers", "Can manage customer information"),

            # Customer Support Permissions
            ("can_view_customer_info", "Can view customer information"),
            ("can_assist_issues", "Can assist with issues"),
            ("can_view_orders", "Can view orders"),

            # Viewer Permissions
            ("can_read_only", "Can read-only access"),

            # Marketing Permissions
            ("can_manage_promotions", "Can manage promotions"),
            ("can_manage_product_visibility", "Can manage product visibility"),

            # Warehouse Manager Permissions
            ("can_manage_inventory", "Can manage inventory"),
            ("can_update_product_quantity", "Can update product quantity"),
        ]


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            # Viewer Permissions for Category
            ("can_view_category", "Can view category"),
        ]


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
            # Warehouse Manager Permissions for Product
            ("can_manage_inventory", "Can manage inventory"),
            ("can_update_product_quantity", "Can update product quantity"),

            # Marketing Permissions for Product
            ("can_manage_product_visibility", "Can manage product visibility"),

            # Viewer Permissions for Product
            ("can_view_product", "Can view product"),
        ]

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
