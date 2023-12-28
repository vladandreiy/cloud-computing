from rest_framework import serializers
from .models import Wishlist, WishlistItem
from product.serializers import ProductSerializer

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = WishlistItem
        fields = ['wishlist', 'product']