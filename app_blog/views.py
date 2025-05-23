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

class MyBlog(LoginRequiredMixin,TemplateView):
    template_name = 'app_blog/my_blogs.html'

class UpdateBlog(LoginRequiredMixin,UpdateView):
    model = Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = 'app_blog/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog_details', kwargs={'slug':self.object.slug})


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
        unique_id = str(uuid.uuid4())[:8]  
        blog_obj.slug = f"{slugify(title)}-{unique_id}"
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))


def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog,user=request.user)
    if already_liked:
        like = True
    else:
        like = False

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
        'comment_form': comment_form,
        'like': like
    }
    return render(request, 'app_blog/blog_details.html', context)

@login_required
def like(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':blog.slug}))

@login_required
def unlike(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked =Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':blog.slug}))
