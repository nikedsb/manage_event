from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Member, Quiz, Team, Wallet, Star, Product, Purchase, Transaction
from .forms import SignUpForm


# Create your views here.

FormView


class SignUpView(CreateView):
    model = Member
    form_class = SignUpForm
    success_url = reverse_lazy("top")
    template_name = "manage_currency/signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        Star.objects.create(user=self.object, star=3)
        Wallet.objects.create(user=self.object, cash=0)

        return HttpResponseRedirect(self.get_success_url())


class QuizView(FormView):
    # 選択肢の生成と代入
    def get_form_kwargs(self, *args, **kwargs):
        kwarg = super().get_form_kwargs(self, *args, **kwargs)
        quiz=
