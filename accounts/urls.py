from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

from .views import register


app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),

]