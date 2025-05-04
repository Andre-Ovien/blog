from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def sign_up(request):
    form = UserCreationForm()
    registered = False
    if request.method == "POST":
        form = UserCreationForm(data= request.POST)
        if form.is_valid():
            form.save()
            registered = True
    context={
        'registered': registered,
        'form' : form
    }
    return render(request, 'app_login/sign_up.html',context)

def login_page(request):
    form = AuthenticationForm
    if request.method == "POST":
        form = AuthenticationForm(data= request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            
    context={
        'form': form,
    }
    return render(request, 'app_login/login.html', context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')    