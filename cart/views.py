from .models import Cart, CartItem
from product.models import Product
from .serializers import CartItemSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

class CartView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        print(request.user)
        cart_items = CartItem.objects.filter(cart__user=request.user)
        for cart_item in cart_items:
            if cart_item.product.stock <= 0:
                cart_item.delete()
            elif cart_item.quantity > cart_item.product.stock:
                cart_item.quantity = cart_item.product.stock
                cart_item.total = cart_item.quantity * cart_item.product.price
                cart_item.save()
        cart_items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
class RemoveFromCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        product_id = request.data.get('product_id')
        cart_item = CartItem.objects.filter(product__id=product_id, cart__user=request.user)
        cart_item.delete()
        cart = Cart.objects.get(user=request.user)
        cart_total = sum(item.total for item in CartItem.objects.filter(cart__user=request.user))
        cart.total = cart_total
        cart.save()
        return Response({'message': 'Cart item deleted successfully'}, status=status.HTTP_200_OK)
    
class AddToCart(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data.get('product').get('id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({'error': 'Product ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user)

        product = Product.objects.get(id=product_id)

     
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'total': product.price * quantity, 'quantity': quantity})
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += int(quantity)

        cart_item.total = cart_item.quantity * cart_item.product.price

        cart_item.save()
        cart_total = sum(item.total for item in CartItem.objects.filter(cart__user=request.user))
        cart.total = cart_total
        
        cart.save()

        return Response({'message': 'Added item to cart successfully'}, status=status.HTTP_200_OK)
    
class UpdateCartItem(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data.get('product').get('id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({'error': 'Product ID and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.get(user=request.user)

        product = Product.objects.get(id=product_id)

        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity = int(quantity)
        cart_item.total = cart_item.quantity * cart_item.product.price
        
        cart_item.save()
        cart_total = sum(item.total for item in CartItem.objects.filter(cart__user=request.user))
        cart.total = cart_total
        
        cart.save()

        return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)