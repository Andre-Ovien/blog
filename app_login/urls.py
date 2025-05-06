from django.urls import path
from . import views

urlpatterns = [
    path('Sign-up/', views.sign_up, name="sign_up"),
    path('login/', views.login_page, name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('update-profile/',views.user_change, name="update_profile"),
    path('password/',views.password_update,name="password_update"),
    path('change-image/',views.add_picture,name="picture"),
    path('update-image/',views.change_dp,name="change_dp")
]
