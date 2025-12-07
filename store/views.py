from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Category, Product, Order, OrderItem
from cart.cart import Cart
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.models import User


def create_superuser_view(request):
    token = request.GET.get("token")

    if token != settings.ADMIN_CREATE_TOKEN:
        return HttpResponseForbidden("Unauthorized")

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="holasoydora"
        )
        return HttpResponse("<h1>✅ Superuser created successfully</h1>")
    else:
        return HttpResponse("<h1>⚠️ Superuser already exists</h1>")


def store_home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            stock__gt=0
        )
        return render(request, 'store/category_detail.html', {
            'products': products,
            'page_title': f'Search Results for "{query}"'
        })
    else:
        categories = Category.objects.all()
        return render(request, 'store/home.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, stock__gt=0)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products,
        'page_title': category.name
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        stock__gt=0
    ).exclude(id=product.id)[:4]

    return render(request, 'store/detail.html', {
        'product': product,
        'related_products': related_products
    })


@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, f"Removed {product.title} from your wishlist.")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, f"Added {product.title} to your wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'store:store_home'))


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        request.session['order_id'] = order.id
        return redirect('payment:process')

    return render(request, 'store/checkout.html', {'cart': cart})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'store/wishlist.html', {'products': products})
