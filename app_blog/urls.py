from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogList.as_view(), name="blog_list"),
    path('create-blog/', views.CreateBlog.as_view(), name="create_blog"),
    path('details/<slug:slug>/',views.blog_details,name="blog_details"),
    path('like/<pk>/',views.like,name="like"),
    path('unlike/<pk>/',views.unlike,name="unlike"),
    path('my-blogs/',views.MyBlog.as_view(),name="my_blog"),
    path('edit-blog/<pk>/',views.UpdateBlog.as_view(),name="edit_blog")    
]
