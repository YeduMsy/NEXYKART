from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages # Import Messages to alert user
from store.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
        
    # --- STOCK VALIDATION LOGIC ---
    
    product_key = str(product_id)
    current_qty_in_cart = 0
    if product_key in cart.cart:
        current_qty_in_cart = cart.cart[product_key]['quantity']
 
    if current_qty_in_cart + quantity > product.stock:
        available_to_add = product.stock - current_qty_in_cart
        
        if available_to_add > 0:
            cart.add(product=product, quantity=available_to_add)
            messages.warning(request, f"Stock limit reached. We added the remaining {available_to_add} items to your cart.")
        else:
            messages.error(request, f"You already have all available stock ({product.stock}) of '{product.title}' in your cart.")
    else:
        cart.add(product=product, quantity=quantity)
        messages.success(request, f"Added {product.title} to your cart.")
        
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, "Item removed from cart.")
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})