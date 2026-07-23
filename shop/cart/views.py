from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from home.models import Product
from .forms import OrderCreateForm, OrderItemFormSet


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'price': product.price, 'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        messages.success(request, f'{product.name} به سبد اضافه شد', 'success')
        return redirect('home:home')


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        return redirect('cart:cart_detail')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        get_object_or_404(CartItem, pk=item_id,
                          cart__user=request.user).delete()
        return redirect('cart:cart_detail')


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.all()

        if not items.exists():
            messages.error(request, 'سبد خرید شما خالی است', 'danger')
            return redirect('cart:cart_detail')

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user, total_price=cart.total_price)
            for item in items:
                OrderItem.objects.bulk_create([
                    OrderItem(order=order, product=item.product,
                              quantity=item.quantity, price=item.price)

                ])
            items.delete()

        messages.success(request, 'سفارش شما ثبت شد', 'success')
        return redirect('cart:order_detail', order.id)


class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'cart/order_list.html', {'orders': orders})


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        return render(request, 'cart/order_detail.html', {'order': order})


class AdminOrderCreateView(UserPassesTestMixin, View):
    raise_exception = True  

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request):
        form = OrderCreateForm()
        formset = OrderItemFormSet()
        return render(request, 'cart/admin_order_create.html', {
            'form': form, 'formset': formset,
        })

    def post(self, request):
        form = OrderCreateForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.created_by_admin = True
                order.total_price = 0
                order.save()

                formset.instance = order
                formset.save()

                order.total_price = sum(
                    i.price * i.quantity for i in order.items.all())
                order.save()
            
            messages.success(request, 'فاکتور با موفقیت ثبت شد', 'success')
            return redirect('cart:admin_order_detail', order.id)

        return render(request, 'cart/admin_order_create.html', {
            'form': form, 'formset': formset,
            
        })

class AdminOrderDetailView(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)  
        return render(request, 'cart/order_detail.html', {'order': order})    
# Create your views here.
