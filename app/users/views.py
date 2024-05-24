from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages

from .forms import UserLoginForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data = request.POST)
        
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
        
            if user:
                auth.login(request, user)
                messages.success(request, f"Приветствуем Вас {username}")
                return HttpResponseRedirect(reverse("main:index"))
    else: 
        form = UserLoginForm()
    
    context = {
        "title":"Авторизация",
        "form": form,
    }

    return render(request, "users/login.html", context)

def registration(request): ...

def profile(request): ...

def logout(request): ...
