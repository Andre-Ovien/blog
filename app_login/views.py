from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

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