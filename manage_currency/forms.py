from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member


class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "job")
