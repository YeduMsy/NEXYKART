from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction 
from store.models import Order, Product, OrderItem

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                for item in order.items.all():
                    
                    product = Product.objects.select_for_update().get(id=item.product.id)
                    
                    if product.stock < item.quantity:
                        raise ValueError(f"Sorry, {product.title} just went out of stock!")
                    if item.price != product.price:
                        raise ValueError(f"Price for {product.title} has changed. Please refresh cart.")

                    product.stock -= item.quantity
                    product.save()

                order.paid = True
                order.save()
                
                if 'order_id' in request.session:
                    del request.session['order_id']
                
                return redirect('payment:success')

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart:cart_detail')
            
        except Exception as e:
            messages.error(request, "An error occurred processing your payment. Please try again.")
            return redirect('cart:cart_detail')
        
    return render(request, 'payment/process.html', {'order': order})

def payment_success(request):
    return render(request, 'payment/success.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')