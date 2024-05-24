from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm


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

def registration(request): 
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        
        if form.is_valid():
            form.save()

            user = form.instance
            auth.login(request, user)

            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    
    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)

def profile(request): ...

def logout(request): 
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))