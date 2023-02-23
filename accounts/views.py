from django.contrib.auth.views import LoginView, TemplateView


class ShowLogin(TemplateView):
    template_name = 'accounts/login.html'

class ShowSignUp(TemplateView):
    template_name = 'accounts/sign_up.html'

class ShowProfilePage(TemplateView):
    template_name = 'accounts/profile_page.html'