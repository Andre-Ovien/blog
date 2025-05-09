from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from .models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from django.http import HttpResponseRedirect
from django.utils.text import slugify

# Create your views here.

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = "app_blog/blog_list.html"


class CreateBlog(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = "app_blog/create_blog.html"
    fields = ('blog_title','blog_content','blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = slugify(title) + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))