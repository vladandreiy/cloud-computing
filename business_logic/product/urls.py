from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', GetMethod, basename='products')
urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path(r'', include(router.urls)),
]