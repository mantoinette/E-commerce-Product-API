from django.contrib import admin
from .models import CustomUser, Product, Category

# Define custom actions for the Category model
def mark_as_updated(modeladmin, request, queryset):
    queryset.update(name='Updated Category')
    modeladmin.message_user(request, "Selected categories have been updated.")

mark_as_updated.short_description = "Mark selected categories as updated"

# Custom admin for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [mark_as_updated]  # Add custom action

# Custom admin for Product (if needed)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity')
    search_fields = ('name', 'category__name')  # Search functionality
    list_filter = ('category',)  # Filter by category

# Register models with custom admin classes
admin.site.register(CustomUser)  # You can create a custom admin for CustomUser as well if needed
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
