from django.shortcuts import get_object_or_404
from django.http import Http404

from django.views.generic import DetailView, ListView

from .models import Products
from .utils import q_search


class CatalogView(ListView):
    model = Products
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3
    title_obj = " "

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale", None)
        order_by = self.request.GET.get("order_by", None)
        query = self.request.GET.get("q", None)
        
        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
            self.title_obj = f"- {goods[0].category.name}"
        
        if on_sale:
            goods = goods.filter(discount__gt = 0)
        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
        
        return goods
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title_obj
        context["slug_url"] = self.kwargs.get("category_slug")
        return context


class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def get_object(self):
        return get_object_or_404(Products, slug = self.kwargs[self.slug_url_kwarg])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context