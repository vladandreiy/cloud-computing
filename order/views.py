from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction, IntegrityError

from .models import Order, OrderItem, Payment, CustomUser, Product
from .serializers import OrderSerializer, MyOrderSerializer, ProductSerializer
from cart.models import Cart, CartItem


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)


class Checkout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        address = request.data.get('address')
        phone_number = request.data.get('phone_number')

        try:
            with transaction.atomic():
                cart = get_object_or_404(Cart, user=user)
                cart_items = CartItem.objects.filter(cart__user=request.user)

                order = Order.objects.create(
                    user=user,
                    total=cart.total,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    phone_number=phone_number
                )

              
                for cart_item in cart_items:
                    if cart_item.quantity > cart_item.product.stock:
                        serializer = ProductSerializer(cart_item.product)
                        raise IntegrityError('Stoc insuficient', 'stock', serializer.data)
                    
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        price=cart_item.product.price,
                        quantity=cart_item.quantity
                    )

                   
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()
                if user.balance < cart.total:
                    raise IntegrityError('Plata nu a putut fi procesata.', 'balance', None)
 
                user.balance -= order.total
                user.save()
                payment = Payment.objects.create(order=order, status='completed')
                cart_items.all().delete()
                cart.delete()
        except IntegrityError as e:
            message, reason, product = e.args
            if product is None:
                return Response({'message': message, 'reason': reason}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': message, 'reason': reason, 'product': product}, status=status.HTTP_400_BAD_REQUEST)


        return Response({'message': 'Comanda plasata cu succes'})
