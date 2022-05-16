from django import views
from django.urls import path
from django.views.generic import TemplateView, CreateView

urlpatterns = [
    path("top/", TemplateView.as_view(template_name="manage_currency/top.html"), name="top")
]
