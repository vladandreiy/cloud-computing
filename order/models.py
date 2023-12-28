from django.contrib.auth.models import User
from django.db import models
from product.models import Product
from user.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True) 
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    class Meta:
        ordering = ['-created_at',]

    def __str__(self):
        return f'Order ID: {self.id}' 


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Order Item ID: {self.id}'  

class Payment(models.Model):
    order = models.ForeignKey(
        Order, related_name='payments', on_delete=models.CASCADE)
    PENDING = 0
    DONE = 1
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='incomplete')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment ID: {self.id}'
