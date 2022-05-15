from re import template
from django.shortcuts import render
from .models import Member, Team, Wallet, Star, Product, Purchase, Transaction
from django.views.generic import TemplateView, CreateView

# Create your views here.


class Template(TemplateView):
    template_name = ""
