"""match_testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import account_urls
from accounts.views import ProfileDetailView, ProfileSettingsDetailView
from core.views import *
from match_testing import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(account_urls)),
    path("", HomeView.as_view(), name="home"),
    path("<str:slug>/", ProfileDetailView.as_view(), name='profile'),
    path("<str:slug>/settings/", ProfileSettingsDetailView.as_view(), name='profile_settings'),
    # добавить эту страницу в будущем
    # path("<str:slug>/settings/safety", ProfileSettingsDetailView.as_view(), name='safety_settings'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
