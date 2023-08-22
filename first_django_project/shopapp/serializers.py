from rest_framework import serializers
from .models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "price",
            "description",
            "discount",
            "created_at",
            "archived",
            "preview",
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "delivery_adress",
            "description",
            "products",
            "user",
            "promocode",
        )
