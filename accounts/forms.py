from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from accounts.models import OtpModel
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form_input login_input",
                "placeholder": "Введите электронную почту",
            }
        ),
        label="",
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form_input nickname_input",
                "placeholder": "Придумайте никнейм",
            }
        ),
        label="",
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form_input password_input",
                "placeholder": "Придумайте пароль",
            }
        ), label="", )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form_input password_input",
                "placeholder": "Повторите пароль",
            }
        ), label="", )

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password1", "password2", "is_active"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 20:
            raise ValidationError("Длина превышает 20 символов")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if len(email) > 254:
            raise ValidationError("Длина адреса электронной почты превышает 254 символа ")
        return email


class UserLoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form_input login_input",
            "placeholder": "Введите электронную почту",
        }))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form_input password_input",
                "placeholder": "Введите пароль",
            }
        ), label="", )

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Неверное имя пользователя или пароль"))

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise forms.ValidationError(_("Неверное имя пользователя или пароль"), code="invalid")
        if user.role == "IA":
            raise forms.ValidationError(_("Пользователь заблокирован"))

        return cleaned_data


class OTPCodeForm(forms.ModelForm):
    otp = forms.CharField(required=True, max_length=7, min_length=7, widget=forms.TextInput(
        attrs={'class': "form_input password_input code_input",
               "placeholder": "Ваш код"}
    ))

    class Meta:
        model = OtpModel
        fields = '__all__'


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": "Введите электронную почту", "class": "form_input password_reset_input"}),
    )


class MyPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "form_input password_input",
                                          "placeholder": "Придумайте пароль", }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                          "class": "form_input password_input",
                                          "placeholder": "Повторите пароль", }),
    )

