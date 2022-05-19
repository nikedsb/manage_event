from ctypes.wintypes import PINT
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Member, Quiz, QuizOption, Team, Wallet, Star, Product, Purchase, Transaction
from .forms import SignUpForm, QuizForm
from .variables import quiz_volume


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
    template_name = "manage_currency/quiz.html"
    form_class = QuizForm
    success_url = reverse_lazy("top")
    # 選択肢の生成と代入
    def get_form_kwargs(self, *args, **kwargs):
        kwarg = super().get_form_kwargs(**kwargs)
        # 基本primaryについquizは一つ
        print(self.kwargs["quiz_num"])
        quiz = Quiz.objects.filter(is_active=True, primary=self.kwargs["quiz_num"]).first()
        print(quiz)
        quiz_options = QuizOption.objects.filter(quiz=quiz)
        print(quiz_options)
        quiz_choices = []
        for quiz_option in quiz_options:
            quiz_choices.append((quiz_option.option, quiz_option.option))
        kwarg["option"] = quiz_choices
        print(kwarg["option"])
        return kwarg

    # def get_form(self):
    #     form = super().get_form()
    #     quiz = Quiz.objects.filter(is_active=True, primary=self.kwargs["quiz_num"]).first()
    #     quiz_options = QuizOption.objects.filter(quiz=quiz)
    #     form.fields["option"].queryset = quiz_options
    #     return form

    # def get_success_url(self, *args, **kwargs):
    #     if self.kwargs["quiz_num"] == quiz_volume:
    #         self.success_url = reverse_lazy("top")
    #         print(self.success_url)
    #     else:
    #         self.success_url = reverse_lazy(
    #             "quiz", kwargs={"quiz_num": self.kwargs["quiz_num"] + 1}
    #         )
    #         print(self.success_url)

    # return self.success_url

    def form_valid(self, form, *args, **kwargs):
        print("dfghjkl")
        return super().form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        print("不正な値")
        print(self.request.POST)
        # print(form.fields["option"])
        return super().form_invalid(form, *args, **kwargs)
