from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class SigninView(TemplateView):
    template_name = "authentication/signin.html"


class SignupView(TemplateView):
    template_name = "authentication/signup.html"
