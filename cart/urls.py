from django.urls import path

from cart import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='api-cart'), 
    path('cart/remove_from_cart/', views.RemoveFromCart.as_view(), name='remove_cart'),
    path('cart/add_to_cart/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/update_cart/', views.UpdateCartItem.as_view(), name='update_cart'),
]