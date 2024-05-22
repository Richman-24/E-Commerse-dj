from django.shortcuts import get_list_or_404, render

from .models import Products

def catalog(request, category_slug):
    if category_slug == "all":
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    context = {
        "title": "Best Coffee - Каталог",
        "goods": goods
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request):

    context = {
        "title": "Best Coffee",
    }

    return render(request, 'goods/product.html', context)