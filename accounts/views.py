"""Profile pages and accounts views"""
import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView

from accounts.username_validator import UsernameValidator
from accounts.accounts_view_utils import get_full_role
from accounts.forms import UserSignUpForm, UserLoginForm, MyPasswordResetForm, MyPasswordResetConfirmForm
from match_testing.settings import LOGIN_REDIRECT_URL
from .tokens import account_activation_token

logger = logging.getLogger('django')

User = get_user_model()


class ProfileDetailView(DetailView):
    template_name = 'accounts/profile_page.html'
    model = User
    slug_field = "username"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        current_profile_id = self.get_object().id  # ID текущего профиля
        profile_data = self.get_user_profile_data(current_profile_id=current_profile_id)  # Данные текущего профиля
        data['user_data'] = profile_data
        data['user_data']['role'] = get_full_role(data['user_data']['role'])
        if self.request.user.is_authenticated:
            current_user_id = self.request.user.id
            if profile_data['record_id'] != current_user_id:
                data['current_user'] = True
        return data

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Если это ajax запрос
            body_data = json.loads(request.body.decode('utf-8'))
            _key = body_data['key']
            response_data = {}
            if _key == "is_authenticated":
                if request.user.is_authenticated:
                    response_data["is_authenticated"] = True
                else:
                    response_data["is_authenticated"] = False
            return JsonResponse(response_data)

    @staticmethod
    def get_user_profile_data(current_profile_id) -> dict[any]:
        """Получает данные пользователя, чей профиль открыт, из таблицы Profile по объекту таблицы User и возвращает
        словарь с данными для их последующего отображения на странице"""
        try:
            current_profile = User.objects.get(id=current_profile_id)
        except ObjectDoesNotExist:
            logger.error('Object user_connected_id not found')
            raise ObjectDoesNotExist('Object user_connected_id not found')

        record_id = current_profile.id
        username = current_profile.username
        teaching_class = current_profile.teaching_class
        description = current_profile.description
        date_of_registration = current_profile.date_joined.now().date()
        role = current_profile.role
        number_of_completed_tests = current_profile.number_of_completed_tests

        if not description:
            description = ""

        avatar = None
        if current_profile.avatar:
            avatar = current_profile.avatar

        profile_data = {
            'record_id': record_id,
            "username": username,
            "teaching_class": teaching_class,
            "description": description,
            "avatar": avatar,
            "date_of_registration": date_of_registration.strftime("%d.%m.%Y"),
            "role": role,
            "number_of_completed_tests": number_of_completed_tests,
        }
        return profile_data


class ProfileSettingsDetailView(DetailView):
    template_name = 'accounts/profile_settings_page.html'
    model = User
    slug_field = "username"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user_object = User.objects.get(email=self.get_object())
        data['user_data'] = user_object
        data['user_data'].role = get_full_role(data['user_data'].role)
        return data

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Если это ajax запрос
            body_data = json.loads(request.body.decode('utf-8'))
            _key = body_data['key']
            response_data = {}
            if _key == "check_username":
                username = body_data['username']
                validator = UsernameValidator()
                validated_username: list = validator.validate_all(username=username)
                if not validated_username:
                    response_data["is_username_valid"] = True
                else:
                    response_data["is_username_valid"] = False
                    response_data["username_errors"] = validated_username
            if _key == "is_authenticated":
                if self.request.user.is_authenticated:
                    response_data["is_authenticated"] = True
                else:
                    response_data["is_authenticated"] = False
            return JsonResponse(response_data)


class LoginOrSendCodeView(FormView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "OTP_code" in request.POST:
            ...

        else:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                print('форма валидна')
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, email=username, password=password)
                if user.two_factor_authentication:
                    # otp_model_object = OtpModel(user=user)
                    # otp_model_object.save()
                    # otp_model_object.send_otp_in_mail()
                    # заглушка
                    raise Http404("Страница не найдена")  # двухфакторная авторизация будет добавлена в будущем
                else:
                    login(self.request, user)
                    return redirect('home')
            else:
                print('форма не валидна')
                return render(request, self.template_name, {"form": form})


# регистрация пользователя
class UserCreationView(CreateView):
    template_name = "accounts/sign_up.html"
    form_class = UserSignUpForm

    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.role = "IA"
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('Email/activate_account.html', {
                'User': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            params = {
                "message": 'Вам отправлена ссылка на электронный адрес, перейдите по ней для подтверждения регистрации. Эту страницу можно закрыть'}
            return render(request, "accounts/registration_message.html", params)
        return render(request, self.template_name, {"form": form}, )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.role = "ST"
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')  #TODO сделать страницу с успешным подтверждением регистрации
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Ссылка для активации недействительна')


# _________________________ Восстановление пароля _________________________


class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    form_class = MyPasswordResetForm


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = MyPasswordResetConfirmForm


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


# _________________________ проверка авторизации _________________________


def check_auth(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            return JsonResponse({'is_authenticated': True})
        else:
            return JsonResponse({'is_authenticated': False})
    else:
        raise PermissionDenied()
