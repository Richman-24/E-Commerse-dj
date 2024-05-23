from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator

from .models import Products

def catalog(request, category_slug):

    page = request.GET.get("page", 1)

    if category_slug == "all":
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    
    context = {
        "title": "Best Coffee - Каталог",
        "goods": current_page
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    
    product = Products.objects.get(slug = product_slug)
    
    context = {
        "title": "Best Coffee",
        "product": product
    }

    return render(request, 'goods/product.html', context)