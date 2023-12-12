from django.urls import path
from .views import *
urlpatterns = [
    path('',handle_login,name="login"),
    path('register/',handle_register,name="signup"),
    path('logout/',handle_logout,name="logout")
]
