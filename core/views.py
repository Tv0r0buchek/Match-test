from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/home.html"

class ShowBase(TemplateView):
    template_name = "core/base.html"

