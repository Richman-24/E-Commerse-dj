from django.shortcuts import render

def index(request):

    context = {
        "title": "Главная",
    }
    return render(request, 'main/index.html', context)

def about(request):

    context = {
        "title": "Интернет магазин премиум кофе – Эксклюзивные редкие сорта кофе купить",
    }

    return render(request, 'main/about.html', context)