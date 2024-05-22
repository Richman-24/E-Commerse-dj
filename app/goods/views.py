from django.shortcuts import render

from .models import Products

def catalog(request):
    
    goods = Products.objects.all()

    context = {
        "title": "Главная",
        "goods": goods
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request):

    context = {
        "title": "Интернет магазин премиум кофе – Эксклюзивные редкие сорта кофе купить",
    }

    return render(request, 'goods/product.html', context)