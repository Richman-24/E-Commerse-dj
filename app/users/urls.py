from django.urls import path

from . import views

app_name='users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('user_cart/', views.user_cart, name='user_cart'),
    path('logout/', views.logout, name='logout'),
]