from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    
    # NEW: Link to users who liked this product
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self): return reverse('store:product_detail', args=[self.slug])
    def __str__(self): return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self): return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def get_cost(self): return self.price * self.quantity