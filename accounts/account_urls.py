from django.urls import path
from accounts.views import ShowLogin, ShowSignUp, ShowProfilePage

urlpatterns = [
    path('login/', ShowLogin.as_view(), name='show_login'),
    path('sign_up/', ShowSignUp.as_view(), name='show_sign_up'),
    path('profile/', ShowProfilePage.as_view(), name="profile")
]
