from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True)  # Change to ImageField
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
