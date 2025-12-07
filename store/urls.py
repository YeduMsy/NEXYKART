from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
]