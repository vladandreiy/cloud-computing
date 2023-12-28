from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('wishlist/add_to_wishlist/', views.AddToWishlist.as_view(), name='add_to_wishlist'),
    path('wishlist/remove_from_wishlist/', views.RemoveFromWishlist.as_view(), name='remove_from_wishlist'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/check_product/<slug:product_slug>/', views.WishlistProductCheck.as_view(), name='check_product_wishlist'),
]