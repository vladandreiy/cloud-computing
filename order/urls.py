from django.urls import path

from order import views

urlpatterns = [
    path('orders/', views.OrdersList.as_view()),
    path('checkout/', views.Checkout.as_view()),
]