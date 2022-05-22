from manage_currency.models import Purchase
from os import name
from re import template
from django.urls import path
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, CreateView
from .views import PurchaseView, ProductListView, SignUpView, QuizView, TradeView

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
        "product_list/",
        ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "purchase/<int:pk>/",
        PurchaseView.as_view(),
        name="purchase",
    ),
    path(
        "quiz/<int:quiz_num>/",
        QuizView.as_view(),
        name="quiz",
    ),
    path("trade/", TradeView.as_view(), name="trade"),
    path(
        "trade_finished/",
        TemplateView.as_view(template_name="manage_currency/trade_finished.html"),
        name="trade_finished",
    ),
    path(
        "trade_started/",
        TemplateView.as_view(template_name="manage_currency/trade_started.html"),
        name="trade_started",
    ),
    path(
        "purchase_done",
        TemplateView.as_view(template_name="manage_currency/purchase-done.html"),
        name="purchase_done",
    ),
]
