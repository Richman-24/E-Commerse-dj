from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, TemplateView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.db.models import Prefetch
from django.urls import reverse, reverse_lazy


from common.mixins import CacheMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from orders.models import Order, OrderItem
from carts.models import Cart


class UserLoginView(LoginView):
    
    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("user:logout"):
            return redirect_page
        return reverse_lazy("main:index")
    
    def form_valid(self, form): #!!! отработает только после того как сработает if form.is_valid()
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)

                if forgot_carts.exists():
                    forgot_carts.delete() 

                Cart.objects.filter(session_key = session_key).update(user=user)
                messages.success(self.request, f"Приветствуем Вас {user.username}")
                return HttpResponseRedirect(self.get_success_url())


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("users:profile")
    
    def form_valid(self, form):
        session_key = self.request.session.session_key

        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Cart.objects.filter(session_key = session_key).update(user=user)

            messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(self.get_success_url())
    

class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Изменения в профиле сохранены")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )).order_by("-id")
        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60)
        return context
    

class UserCartView(TemplateView):
    template_name = "users/user_cart.html"


@login_required
def logout(request): #Сознательно оставим FBV, т.к. версии logout выполняется по предоставлению csrf токена из post запроса через форму
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))