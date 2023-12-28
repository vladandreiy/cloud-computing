from rest_framework import serializers
from .models import CartItem
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'total']