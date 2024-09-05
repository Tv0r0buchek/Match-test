from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from accounts.views import LoginOrSendCodeView, \
    UserCreationView, \
    ProfileDetailView, \
    activate, \
    MyPasswordResetView, \
    MyPasswordResetDoneView, \
    MyPasswordResetCompleteView, \
    MyPasswordResetConfirmView, \
    check_auth

#  match_test/accounts/...

urlpatterns = [
    path('login/', LoginOrSendCodeView.as_view(), name='login'),
    path('sign_up/', UserCreationView.as_view(), name='sign_up'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),  # введите ваш email
    path('password_reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),  # мы отправили вам инструкции на почту
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # ссылка внутри письма
    path('reset/done/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # поздравляем, вы молодец

    path('check_authentication/', check_auth, name='check_authentication')
]
