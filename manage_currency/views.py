from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Member, Team, Wallet, Star, Product, Purchase, Transaction
from .forms import SignUpForm


# Create your views here.


class SignUpView(CreateView):
    model = Member
    form_class = SignUpForm
    success_url = reverse_lazy("top")
    template_name = "manage_currency/signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        Star.objects.create(user=self.object, star=3)

        return HttpResponseRedirect(self.get_success_url())


# def create_team(request):
#     if request.method == "POST":
#         # チーム分けアルゴリズムを書く
#         print(request.POST)
#         return
#     else:
#         if request.user.is_superuser:
#             return reverse_lazy("admin:manage_currency_Team_changelist")
#         # return HttpResponseBadRequest()
