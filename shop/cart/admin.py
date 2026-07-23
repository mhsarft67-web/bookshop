from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    # extra ->تعداد ردیف های خالی صفر باشد
    # inline -> مدلهای مرتبط با یکدیگر را بدون اینکه نیاز به ایجاد صفحه جدا باشد امکان ویرایش کردن میدهد
    # tabular -> استایلی برای نمایش inline است ->
    # بصورت جدول نمایش میدهد
    # stacked -> استایلی دیگر است به صورت عمودی و فرمی است


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'total_price']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price',
                    'status', 'created_at', 'created_by_admin']
    list_filter = ['status', 'created_by_admin']
    list_editable = ['status']
    inlines = [OrderItemInline]

# Register your models here.
