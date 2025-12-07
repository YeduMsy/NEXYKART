from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Added 'stock' to display and editable list
    list_display = ['title', 'price', 'stock', 'in_stock', 'created']
    list_editable = ['price', 'stock'] 
    prepopulated_fields = {'slug': ('title',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'email', 'paid', 'created']
    inlines = [OrderItemInline]