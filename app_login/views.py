from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserProfileChange, ProfilePic

def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == "POST":
        form = SignUpForm(data= request.POST)
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

@login_required
def profile(request):
    context={

    }
    return render(request,'app_login/profile.html', context)

@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == "POST":
        form = UserProfileChange(data=request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
            return redirect('profile')
    context={
        'form': form
    }
    return render(request,'app_login/change_profile.html',context)

@login_required
def password_update(request):
    current_user = request.user
    change = False
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            change = True
    context={
        'form': form,
        'change': change
    }
    return render(request,'app_login/password.html',context)

@login_required
def add_picture(request):
    form = ProfilePic()

    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save() 
            return redirect('profile')

    context={
        'form': form
    }
    return render(request,'app_login/picture.html', context)

@login_required
def change_dp(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == "POST":
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context = {
        'form': form
    }
    return render(request,'app_login/picture.html',context)