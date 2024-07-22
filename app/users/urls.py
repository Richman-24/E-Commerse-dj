from django.urls import path

from users.views import UserLoginView, UserProfileView, UserRegistrationView, UserCartView, logout

app_name='users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user_cart/', UserCartView.as_view(), name='user_cart'),
    path('logout/', logout, name='logout'),
]