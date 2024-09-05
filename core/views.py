import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

User = get_user_model()


class HomeView(TemplateView):
    template_name = "core/home.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data()
        if self.request.user.is_authenticated:
            data['User'] = User.objects.get(id=self.request.user.id).username
        else:
            data['User'] = ""
        return data

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Если это ajax запрос
            body_data = json.loads(request.body.decode('utf-8'))
            _key = body_data['key']
            if _key == "is_authenticated":
                if request.user.is_authenticated:
                    username = User.objects.get(id=self.request.user.id).username
                    url = reverse('profile', kwargs={'slug': username})  # Отправка url для переадресации
                    domain_url = self.request.build_absolute_uri(url)
                    return JsonResponse({'redirect_url': domain_url})
                else:
                    return JsonResponse({'is_authenticated': False})
