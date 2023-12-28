from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem
from product.models import Product
from .serializers import WishlistItemSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes


class WishlistView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        wishlist_items = WishlistItem.objects.filter(
            wishlist__user=request.user)
        serializer = WishlistItemSerializer(wishlist_items, many=True)
        return Response(serializer.data)
    
class WishlistProductCheck(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, product_slug, format=None):
        item_in_wishlist = WishlistItem.objects.filter(
            wishlist__user=request.user, product__slug=product_slug).exists()
        return Response({'itemInWishlist': item_in_wishlist}, status=status.HTTP_200_OK)


class RemoveFromWishlist(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data.get('product').get('id')
        wishlist_item = WishlistItem.objects.filter(
            product__id=product_id, wishlist__user=request.user)
        wishlist_item.delete()
        return Response({'message': 'Wishlist item deleted successfully'}, status=status.HTTP_200_OK)


class AddToWishlist(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        product_id = request.data.get('product').get('id')

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        product = Product.objects.get(id=product_id)

        # Check if the product is already in the wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(
            product=product, wishlist=wishlist)

        wishlist_item.save()

        return Response({'message': 'Added item to wishlist successfully'}, status=status.HTTP_200_OK)
