from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_adress", "promocode", "user", "products"
        labels = {
            'user': 'Покупатель',
            'delivery_adress': 'Адрес доставки',
            'promocode': 'Промокод',
        }


