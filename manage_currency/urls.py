from os import name
from re import template
from django.urls import path
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, CreateView
from .views import SignUpView, QuizView

urlpatterns = [
    path("top/", TemplateView.as_view(template_name="manage_currency/top.html"), name="top"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        LoginView.as_view(
            template_name="manage_currency/login.html", form_class=AuthenticationForm
        ),
        name="log_in",
    ),
    path(
        "product_list",
        TemplateView.as_view(template_name="manage_currency/top.html"),
        name="product_list",
    ),
    path(
        "product_detail/",
        TemplateView.as_view(template_name="manage_currency/top.html"),
        name="product_detail",
    ),
    path(
        "quiz/<int:quiz_num>/",
        TemplateView.as_view(template_name="manage_currency/top.html"),
        name="quiz",
    ),
    path("trade/", TemplateView.as_view(template_name="manage_currency/top.html"), name="trade"),
    #     path(
    #         "create_team/",
    #         create_team,
    #         name="create_team",
    #     ),
]
