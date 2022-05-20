from tokenize import group
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    FinishedQuiz,
    Member,
    Quiz,
    QuizOption,
    Team,
    Wallet,
    Star,
    Product,
    Purchase,
    Transaction,
)
from .forms import SignUpForm, QuizForm, TradeForm
from .variables import quiz_volume
from django.http import HttpResponseForbidden


# Create your views here.

FormView


class SignUpView(CreateView):
    model = Member
    form_class = SignUpForm
    success_url = reverse_lazy("top")
    template_name = "manage_currency/signup.html"

    def form_valid(self, form):
        self.object = form.save()
        Star.objects.create(user=self.object, star=3)
        Wallet.objects.create(user=self.object, cash=0)

        return HttpResponseRedirect(self.get_success_url())


class QuizView(LoginRequiredMixin, FormView):
    template_name = "manage_currency/quiz.html"
    form_class = QuizForm

    def get(self, request, *args, **kwargs):
        team = self.request.user.group
        # チームリーダーのみ回答可能
        # チームリーダーではない時
        if not team.leader == self.request.user:
            return HttpResponseForbidden()
        quiz_num = self.kwargs["quiz_num"]
        answered_quizes_num = FinishedQuiz.objects.filter(team=self.request.user.group).count()
        print(answered_quizes_num)
        print(quiz_num)
        # 二回目以降の解答をしようとしていた場合、あるいは先に問題に取り組もうとした場合
        if not answered_quizes_num == quiz_num - 1:
            return redirect("quiz", answered_quizes_num + 1)

        return super().get(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        # 選択肢をオーバーライドしてる
        form = super().get_form(**kwargs)
        quiz = Quiz.objects.filter(is_active=True, primary=self.kwargs["quiz_num"]).first()
        quiz_options = QuizOption.objects.filter(quiz=quiz)
        form.fields["option"].queryset = quiz_options
        return form

    def get_success_url(self, *args, **kwargs):
        if self.kwargs["quiz_num"] == quiz_volume:
            self.success_url = reverse_lazy("top")
            print(self.success_url)
        else:
            self.success_url = reverse_lazy(
                "quiz", kwargs={"quiz_num": self.kwargs["quiz_num"] + 1}
            )
            print(self.success_url)

        return self.success_url

    def form_valid(self, form, *args, **kwargs):
        # 正解かどうかの検証
        user_choice = form.cleaned_data["option"]
        team = self.request.user.group
        quiz = get_object_or_404(Quiz, is_active=True, primary=self.kwargs["quiz_num"])
        # finished_quizに入れて遅延評価
        finished_quiz, is_created = FinishedQuiz.objects.get_or_create(
            team=team,
            quiz=quiz,
            defaults={"team": team, "quiz": quiz, "selected_choice": user_choice},
        )
        # ほとんど想定されないが
        if not is_created:
            finished_quiz.selected_choice = user_choice
            finished_quiz.save()
        # 最終問題の時は得点集計
        if self.kwargs["quiz_num"] == quiz_volume:
            group = Team.objects.get(leader=self.request.user)
            finished_quizes = FinishedQuiz.objects.select_related(
                "quiz__answer", "selected_choice"
            ).filter(team=group)
            score = 0
            for finished_quiz in finished_quizes:
                question = finished_quiz.quiz
                correct_answer = finished_quiz.quiz.answer.correct_option
                # 正解の時
                if finished_quiz.selected_choice == correct_answer:
                    score += 1
                    print(score)
            group.score = score
            group.save()
        return super().form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        print("不正な値")
        return super().form_invalid(form, *args, **kwargs)


class TradeView(FormView):
    template_name = "manage_currency/trade.html"
    form_class = TradeForm
