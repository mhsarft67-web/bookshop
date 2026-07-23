from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status']


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=['product', 'quantity', 'price'],
    extra=3,
    can_delete=True,
)
