from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    class RoleChoise(models.TextChoices):
        standard = 'ST', 'Стандартный'
        admin = "AD", "Администратор"
        worker = "WK", "Сотрудник"
        inactive = "IA", "Неактивен"

    user_connected = models.OneToOneField(User, on_delete=models.CASCADE)  # связь со стандартной моделью пользователь
    role = models.CharField(choices=RoleChoise.choices, default=RoleChoise.inactive, max_length=2)  # роль пользователя на сайте
    secret_question = models.CharField(max_length=50)  # секретный вопрос, который может быть использован для какой-либо идентификации
    answer_to_secret_question = models.CharField(max_length=50)  # ответ на секретный вопрос

    teaching_class = models.IntegerField(blank=True, null=True, validators=[
        MaxValueValidator(11),
        MinValueValidator(0)
    ])  # класс обучения
    date_of_registration = models.DateTimeField(auto_now_add=True)  # дата регистрации пользователя
    last_class_change = models.DateTimeField()  # дата смены класса
    changing_training_class = models.BooleanField(default=True)  # Разрешить смену класса обучения - т.к. часто его менять нельзя
    description = models.CharField(max_length=50, blank=True)  # описание, которое отображается в профиле
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    unique_user_code = models.CharField(max_length=15)  # TODO написать уникальный код пользователя

    average_percent_for_tests = models.DecimalField(decimal_places=2, max_digits=4)  # процент правильных ответов во всех тестах
    number_of_completed_tests = models.IntegerField(validators=[MinValueValidator(0)])  # общее количество пройденных тестов
