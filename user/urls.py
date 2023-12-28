from django.urls import path, include

from user import views

urlpatterns = [
    path('users/me', views.UserView.as_view()),
    path('users/add_balance', views.AddBalance.as_view()),
]