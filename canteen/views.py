from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem
from .forms import RegisterForm, LoginForm, UPIPaymentForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def home_view(request):
    categories = Category.objects.prefetch_related('items').all()
    for category in categories:
        category.available_items = category.items.filter(is_available=True)
    return render(request, 'home.html', {'categories': categories})


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.select_related('menu_item').all()
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': 1}
        )
        if not created:
            if cart_item.quantity < menu_item.stock_quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                return JsonResponse({'success': False, 'message': 'Not enough stock!'})
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'item_quantity': cart_item.quantity,
            'item_subtotal': str(cart_item.subtotal),
            'cart_total': str(cart.total),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        menu_item = get_object_or_404(MenuItem, id=item_id)
        cart = get_object_or_404(Cart, user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, menu_item=menu_item)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                item_quantity = cart_item.quantity
            else:
                cart_item.delete()
                item_quantity = 0
        except CartItem.DoesNotExist:
            item_quantity = 0
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'item_quantity': item_quantity,
            'cart_total': str(cart.total),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def delete_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, menu_item_id=item_id).delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
@require_POST
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cart_items.all().delete()
    messages.info(request, 'Cart cleared.')
    return redirect('cart')


@login_required
def payment_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.select_related('menu_item').all()
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('home')
    upi_form = UPIPaymentForm()
    return render(request, 'payment.html', {
        'cart': cart,
        'cart_items': cart_items,
        'upi_form': upi_form,
    })


@login_required
@require_POST
def process_payment(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.select_related('menu_item').all()
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('home')
    payment_method = request.POST.get('payment_method', 'cash')
    upi_transaction_id = None
    if payment_method == 'upi':
        upi_form = UPIPaymentForm(request.POST)
        if not upi_form.is_valid():
            return render(request, 'payment.html', {
                'cart': cart,
                'cart_items': cart_items,
                'upi_form': upi_form,
            })
        upi_transaction_id = upi_form.cleaned_data['transaction_id']
    order = Order.objects.create(
        user=request.user,
        payment_method=payment_method,
        payment_status='paid' if payment_method == 'upi' else 'cash',
        upi_transaction_id=upi_transaction_id,
        total_amount=cart.total,
        status='confirmed',
    )
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            quantity=cart_item.quantity,
            unit_price=cart_item.menu_item.price,
        )
        item = cart_item.menu_item
        item.stock_quantity = max(0, item.stock_quantity - cart_item.quantity)
        item.save()
    cart.cart_items.all().delete()
    messages.success(request, f'Order #{order.id} placed successfully!')
    return redirect('payment_success', order_id=order.id)


@login_required
def payment_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment_success.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__menu_item')
    return render(request, 'order_history.html', {'orders': orders})