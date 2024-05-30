from django.urls import path

from users.views import login, registration, profile, user_cart, logout

app_name='users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('user_cart/', user_cart, name='user_cart'),
    path('logout/', logout, name='logout'),
]