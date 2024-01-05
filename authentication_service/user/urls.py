from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', GetMethod, basename='user')
urlpatterns = router.urls
urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('verify/', VerifyView.as_view(), name='verify_view'),
    path(r'', include(router.urls)),
]