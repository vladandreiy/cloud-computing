from django.contrib.auth.models import User
from django.db import models
from product.models import Product
from user.models import CustomUser

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, related_name='wishlists', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Wishlist ID: {self.id}'

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Wishlist Item ID: {self.id}'
