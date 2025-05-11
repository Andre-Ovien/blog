from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView
from .models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .forms import CommentForm

# Create your views here.

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = "app_blog/blog_list.html"


class CreateBlog(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = "app_blog/create_blog.html"
    fields = ('blog_title','blog_content','blog_image')

    from django.utils.text import slugify
import uuid

def form_valid(self, form):
    blog_obj = form.save(commit=False)
    blog_obj.author = self.request.user
    title = blog_obj.blog_title
    unique_id = str(uuid.uuid4())[:8]  
    blog_obj.slug = f"{slugify(title)}-{unique_id}"
    blog_obj.save()
    return HttpResponseRedirect(reverse('index'))


def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':slug}))


    context = {
        'blog': blog,
        'comment_form': comment_form
    }
    return render(request, 'app_blog/blog_details.html', context)