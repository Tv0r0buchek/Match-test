import logging
import math
import random
# from datetime import datetime, timedelta
import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from match_testing.settings import EMAIL_HOST_USER

logger = logging.getLogger('django')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'AD')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be a staff'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be a superuser'
            )

        return self._create_user(email, password, **extra_fields)


username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    email = models.EmailField(_("email_address"), unique=True)

    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        help_text=_(
            "Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    class RoleChoise(models.TextChoices):
        standard = "ST", "Стандартный"
        admin = "AD", "Администратор"
        worker = "WK", "Сотрудник"
        inactive = "IA", "Неактивен"  # забанен

    role = models.CharField(choices=RoleChoise.choices, default=RoleChoise.standard, max_length=2)  # роль пользователя на сайте
    secret_question = models.CharField(max_length=50, blank=True)  # секретный вопрос, который может быть использован для какой-либо идентификации
    answer_to_secret_question = models.CharField(max_length=50, blank=True)  # ответ на секретный вопрос
    two_factor_authentication = models.BooleanField(default=False)  # включена ли двухфакторная аутентификация
    teaching_class = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(11), MinValueValidator(0)])  # класс обучения
    date_of_registration = models.DateTimeField(auto_now_add=True)  # дата регистрации пользователя
    description = models.CharField(max_length=120, null=True, blank=True)  # описание, которое отображается в профиле
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    unique_user_code = models.CharField(max_length=15, null=True, blank=True)  # TODO написать уникальный код пользователя, убрать null
    show_tests = models.BooleanField(default=True)  # отображать ли тесты пользователя на странице его профиля

    average_percent_for_tests = models.DecimalField(decimal_places=2, max_digits=4, default=0)  # процент правильных ответов во всех тестах
    number_of_completed_tests = models.IntegerField(validators=[MinValueValidator(0)], default=0)  # общее количество пройденных тестов

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]


class OtpModelManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            expiration_time__lt=datetime.datetime.utcnow()
        )


class OtpModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()

    objects = OtpModelManager()

    def __str__(self):
        return f"{self.user.email}, code: '{self.otp}' "

    def send_otp_in_mail(self):
        subject = 'Math-test, подтверждение входа'
        message = f'Привет {self.user.email}, это письмо с кодом подтверждения, никому не сообщайте его. \n Ваш код  - {self.otp}'
        email_from = EMAIL_HOST_USER
        recipient_list = [self.user.email]
        send_mail(subject, message, email_from, recipient_list)

    def save(self, *args, **kwargs):
        if not self.pk:  # если запись новая
            self.expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=20)
            if not self.otp:
                self.otp = self.otp_generator()
        return super().save(*args, **kwargs)

    def code_is_correct(self, code: str):
        try:
            str(code)
        except TypeError as e:
            logger.error(f"def code_is_correct(), невозможно преобразовать {type(code)} в строку {e}")
            raise TypeError(f"Ошибка: невозможно преобразовать {type(code)} в строку") from e
        if code == self.otp and self.is_active:
            return True
        else:
            return False

    @staticmethod
    def otp_generator():
        corpus = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        generate_OTP = ""
        size = 7
        length = len(corpus)
        for i in range(size):
            generate_OTP += corpus[math.floor(random.random() * length)]
        return generate_OTP
