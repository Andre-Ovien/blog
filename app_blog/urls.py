from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogList.as_view(), name="blog_list"),
    path('create-blog/', views.CreateBlog.as_view(), name="create_blog")    
]
