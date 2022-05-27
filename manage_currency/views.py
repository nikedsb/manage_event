import math

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, TemplateView

from .forms import PurchaseForm, QuizForm, SignUpForm, TradeForm
from .models import (
    AllCash,
    FinishedQuiz,
    Member,
    Product,
    Purchase,
    Quiz,
    QuizOption,
    Star,
    Team,
    Transaction,
    Wallet,
)
from .variables import quiz_volume


def detect_leader(user):
    try:
        leader = user.group.leader
        if leader == user:
            return {"leader": user}
        else:
            return {}
    except:
        return {}


# Create your views here.
class TopView(LoginRequiredMixin, TemplateView):
    template_name = "manage_currency/top.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = Wallet.objects.get(user=self.request.user)
        star = Star.objects.get(user=self.request.user)
        try:
            leader_name = self.request.user.group.leader.username
        except:
            leader_name = "なし"
        purchases = Purchase.objects.select_related("product").filter(user=self.request.user)
        if purchases.exists():
            context.update(
                {
                    "star": star.star,
                    "cash": wallet.cash,
                    "purchases": purchases,
                    "leader_name": leader_name,
                }
            )
        else:
            context.update({"star": star.star, "cash": wallet.cash, "leader_name": leader_name})
        context.update(detect_leader(self.request.user))
        return context


class SignUpView(CreateView):
    model = Member
    form_class = SignUpForm
    success_url = reverse_lazy("top")
    template_name = "manage_currency/signup.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.id != None:
            return redirect("log_in")
        return super().get(request, *args, **kwargs)

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
        # チームに入ってない場合はトップにリダイレクト
        if team == None:
            return redirect("top")

        # チームリーダーのみ回答可能
        # チームリーダーではない時
        if not team.leader == self.request.user:
            raise PermissionDenied()
        quiz_num = self.kwargs["quiz_num"]
        answered_quizes_num = FinishedQuiz.objects.filter(team=self.request.user.group).count()
        all_quizes = Quiz.objects.filter(is_active=True).count()
        # 二回目以降の解答をしようとしていた場合、あるいは先に問題に取り組もうとした場合
        if not answered_quizes_num == quiz_num - 1:
            return redirect("quiz", answered_quizes_num + 1)
        elif all_quizes <= answered_quizes_num:
            return redirect("top")

        return super().get(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        # 選択肢をオーバーライドしてる
        form = super().get_form(**kwargs)
        quiz = Quiz.objects.filter(is_active=True, primary=self.kwargs["quiz_num"]).first()
        quiz_options = QuizOption.objects.filter(quiz=quiz)
        form.fields["option"].queryset = quiz_options
        return form

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        team = self.request.user.group
        quiz = Quiz.objects.filter(is_active=True, primary=self.kwargs["quiz_num"]).first()
        kwgs.update({"team": team, "quiz": quiz})

        return kwgs

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
            group.score = score
            group.save()
        return super().form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        return super().form_invalid(form, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_num = self.kwargs["quiz_num"]
        quiz = Quiz.objects.filter(is_active=True, primary=quiz_num).first()
        context.update(
            {
                "quiz": quiz,
                "quiz_num": quiz_num,
            }
        )
        context.update(detect_leader(self.request.user))
        return context


class TradeView(LoginRequiredMixin, FormView):
    template_name = "manage_currency/trade.html"
    form_class = TradeForm

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        user = self.request.user
        kwgs["oneself"] = user
        kwgs["is_sender"] = self.request.POST.get("is_sender")
        return kwgs

    def form_valid(self, form, *args, **kwargs):
        # ほんちゃんの処理、
        user = self.request.user
        trade_with = Member.objects.get(id=form.cleaned_data["trade_with"].id)
        star = form.cleaned_data["star"]
        cash = form.cleaned_data["cash"]
        if form.cleaned_data["is_sender"]:
            sender = self.request.user
            receiver = trade_with
        else:
            sender = trade_with
            receiver = self.request.user

        # transactionを探す
        try:
            # 誰かが自分に対して申請した取引を取得
            transaction = Transaction.objects.get(
                trade_with=user,
                send_from=sender,
                send_to=receiver,
                is_done=False,
                is_canceled=False,
            )

            # 取引量の合意があるか
            if transaction.cash == cash and transaction.star == star:
                sender_wallet = Wallet.objects.get(user=sender)
                sender_star = Star.objects.get(user=sender)
                receiver_wallet = Wallet.objects.get(user=receiver)
                receiver_star = Star.objects.get(user=receiver)

                # Starの取引
                if star > 0:
                    sender_star.star -= star
                    sender_star.save()
                    receiver_star.star += star
                    receiver_star.save()
                # Cashの取引
                if cash > 0:
                    sender_wallet.cash -= cash
                    sender_wallet.save()
                    receiver_wallet.cash += cash
                    receiver_wallet.save()

                transaction.is_done = True
                transaction.save()
                # get_success_urlに引き渡す。
                self.is_trade_done = True
            else:

                form.add_error(None, "スターおよびコインの取引量が合意された量ではありません。")
                return self.render_to_response(self.get_context_data(form=form))
        except:
            # ミスの送信の可能性
            error_transaction = Transaction.objects.filter(
                trade_with=user,
                send_from=receiver,
                send_to=sender,
                is_done=False,
                is_canceled=False,
            )
            if error_transaction.exists():
                form.add_error(None, "送信者と受信者が合致しません。")
                return self.render_to_response(self.get_context_data(form=form))

            new_transanction = Transaction(
                requested_by=user,
                trade_with=trade_with,
                send_from=sender,
                send_to=receiver,
                star=star,
                cash=cash,
                is_canceled=False,
                is_done=False,
            )
            new_transanction.save()
            # get_success_urlに引き渡す
            self.is_trade_done = False
        return super().form_valid(form, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_present:
            return redirect("top")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # request.POSTからとってきて,キャンセルボタンが押された時に現在のTransactionをis_doneにする
        if "取引をキャンセル" in request.POST.getlist("cancel_trade"):
            # 自分が申請してるものをキャンセル。
            user = self.request.user
            try:
                transaction = Transaction.objects.get(
                    requested_by=user, is_done=False, is_canceled=False
                )
                transaction.is_canceled = True
                transaction.save()
                context = self.get_context_data(*args, **kwargs)
                context["cancel_message"] = "申請した取引のキャンセルが完了しました。"
                context["form"] = TradeForm()
            except:
                context = self.get_context_data(*args, **kwargs)
                context["cancel_message"] = "申請している取引はありません。"
                context["form"] = TradeForm()
            return render(self.request, "manage_currency/trade.html", context)

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        if self.is_trade_done:
            success_url = reverse_lazy("trade_finished")
        else:
            success_url = reverse_lazy("trade_started")
        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = Wallet.objects.get(user=self.request.user)
        star = Star.objects.get(user=self.request.user)
        transaction_set = Transaction.objects.filter(
            requested_by=self.request.user, is_done=False, is_canceled=False
        )
        context.update(detect_leader(self.request.user))
        try:
            leader_name = self.request.user.group.leader.username
        except:
            leader_name = "なし"
        if transaction_set.exists():
            context.update(
                {
                    "star": star.star,
                    "cash": wallet.cash,
                    "transaction": transaction_set.first(),
                    "leader_name": leader_name,
                }
            )
        else:
            context.update({"star": star.star, "cash": wallet.cash, "leader_name": leader_name})
        return context


class ProductListView(LoginRequiredMixin, ListView):
    template_name = "manage_currency/product-list.html"
    model = Product

    def get(self, request, *args, **kwargs):
        if not request.user.is_present:
            return redirect("top")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["wallet"] = Wallet.objects.get(user=self.request.user)
        context.update(detect_leader(self.request.user))
        return context


class PurchaseView(LoginRequiredMixin, FormView):
    template_name = "manage_currency/purchase.html"
    form_class = PurchaseForm
    success_url = reverse_lazy("purchase_done")

    def get(self, request, *args, **kwargs):
        if not request.user.is_present:
            return redirect("top")
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        user = self.request.user
        product = Product.objects.get(id=self.kwargs["pk"])
        self.product = product
        self.quantity = None
        if self.request.method == "POST":
            try:
                self.quantity = int(float(self.request.POST.get("quantity")))
                print(self.quantity)
            except:
                self.quantity = None
        kwgs.update(
            {
                "product": product,
                "quantity": self.quantity,
                "oneself": user,
            }
        )
        return kwgs

    def form_valid(self, form, *args, **kwargs):
        # 購入処理
        quantity = form.cleaned_data["quantity"]
        # 引き落とし
        wallet = Wallet.objects.get(user=self.request.user)
        wallet.cash -= form.cleaned_data["price_sum"]
        wallet.save()
        # 在庫数調整
        self.product.stock -= quantity
        self.product.save()
        # 購入履歴更新
        purchase = Purchase.objects.create(
            user=self.request.user,
            product=self.product,
            quantity=quantity,
            is_delivered=False,
        )
        if self.product.name == "DeMiStar":
            purchase.is_delivered = True
            purchase.save()
            star = Star.objects.get(user=self.request.user)
            star.star += quantity
            star.save()
        # DeMiStarの価格リセット
        demi_star = Product.objects.get(name="DeMiStar")
        initial_all_cash = AllCash.objects.all().first().all_cash
        current_all_cash = Wallet.objects.aggregate(models.Sum("cash"))["cash__sum"]
        s = initial_all_cash / current_all_cash
        demi_star.price = math.ceil(1100 * s)
        demi_star.save()
        return super().form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        product = Product.objects.get(id=self.kwargs["pk"])
        wallet = Wallet.objects.get(user=self.request.user)
        context.update({"product": product, "wallet": wallet})
        context.update(detect_leader(self.request.user))
        return context


class RankingView(TemplateView):
    template_name = "manage_currency/ranking.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        wallets = (
            Wallet.objects.select_related("user").filter(user__is_present=True).order_by("-cash")
        )
        stars = Star.objects.select_related("user").filter(user__is_present=True).order_by("-star")
        context.update(
            {
                "wallets": wallets,
                "stars": stars,
            }
        )
        return context
