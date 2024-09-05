from django.db import models
from match_testing.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Test(models.Model):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    displayed = models.BooleanField(default=False)  # будет ли виден вопрос на главной странице
    is_active = models.BooleanField(default=False)  # будет ли тест доступным для прохождения
    time_to_complete_in_seconds = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(36000)])
    number_of_questions = models.IntegerField()  # число вопросов, задается автоматически, когда тест создается


class VariantsOfNumbers(models.Model):
    visible = models.BooleanField(default=False)  # виден ли набор чисел в списке на странице создания вопросов
    teaching_class = models.TextField(max_length=2)
    name_of_list_of_numbers = models.CharField(max_length=25)
    list_of_numbers = models.JSONField()
    list_of_numbers_2 = models.JSONField(blank=True)
    list_of_numbers_3 = models.JSONField(blank=True)


class Question(models.Model):
    class Answer_option(models.TextChoices):
        answer = "A"
        option = "O"

    header = models.CharField(max_length=120, blank=True)
    text = models.TextField(max_length=1000)
    answer_options_or_the_answer = models.TextField(choices=Answer_option.choices)  # конкретный ответ или варианты ответов
    is_a_permanent_condition = models.BooleanField(default=True)  # будут ли числа в вопросе подбираться рандомно или нет
    connected_set_of_variants = models.ForeignKey(VariantsOfNumbers, blank=True, null=True, on_delete=models.CASCADE)
    date_of_publication = models.DateTimeField(auto_now_add=True)
    correct_answer = models.CharField(max_length=30)
    number_of_points_per_question = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)])
    test_connected = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.header)


class AnswerOptions(models.Model):
    question_connected = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=30)
    IsCorrect = models.BooleanField(default=False)  # является ли ответ верным


class QuestionPhoto(models.Model):
    question_connected = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_photo")
    image = models.ImageField(upload_to="questions/")

    def __str__(self):
        return str(self.question_connected.header)


class PassedTest(models.Model):
    """
        Пройденные пользователем тесты
    """
    user_connected = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    connected_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    scores = models.IntegerField()  # баллы, которые получены при прохождении теста
    date_of_passage = models.DateTimeField(auto_now_add=True)  # дата прохождения
