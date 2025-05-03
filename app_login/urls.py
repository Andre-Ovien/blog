from django.urls import path
from . import views

urlpatterns = [
    path('Sign-up/', views.sign_up, name="sign_up")
]
