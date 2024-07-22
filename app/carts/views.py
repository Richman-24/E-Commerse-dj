from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from carts.models import Cart
from carts.utils import get_user_carts
from django.urls import reverse

from goods.models import Products


class CartMixin:

    def get_cart(self, request, product=None, cart_id=None):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product
        if cart_id:
            query_kwargs["id"] = cart_id

        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        referer = request.META.get("HTTP_REFERER")
        if reverse("orders:create_order") in referer:
            context["order"] = True

        return render_to_string(
            "includes/included_cart.html", context, request=request
        )

class CartAddView(CartMixin, View):
    
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)

        cart = self.get_cart(request, product=product)

        if cart:
            cart.amount +=1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product, amount=1)
            
        response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": self.render_cart(request),
    }
        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        cart.amount = request.POST.get("amount")
        cart.save()

        amount = cart.amount

        response_data = {
        "message": "Количество изменено",
        "amount": amount,
        "cart_items_html": self.render_cart(request),
    }
        
        return JsonResponse(response_data)
            

class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        amount = cart.amount
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": amount,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)