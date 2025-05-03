from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse


def index(request):
    return redirect('blog_list')