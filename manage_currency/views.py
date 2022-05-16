from re import template
from django.shortcuts import render
from .models import Member, Team, Wallet, Star, Product, Purchase, Transaction
from django.views.generic import TemplateView, CreateView

# Create your views here.


class SignUpView(CreateView):
    model = Member
    template_name = "signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        

        return HttpResponseRedirect(self.get_success_url())
