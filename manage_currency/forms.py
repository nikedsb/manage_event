from itertools import product
from django import forms
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.core.exceptions import ObjectDoesNotExist
from .models import Member, Purchase, QuizOption, Transaction, Star, Wallet


class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "job")
        labels = {"job": "分類"}
        help_texts = {
            "username": "",
        }


class QuizForm(forms.Form):
    class QuizChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.option

    option = QuizChoiceField(queryset=QuizOption.objects.all(), label="選択肢")

    # def __init__(self, option=None, *args, **kwargs):
    #     # base_filedにフィールドが入っていて、インスタンスごとにコピーされる→Bseformのコンストラクタで
    #     # 動的な選択肢の受け渡し
    #     self.base_fields["option"].choices = option
    #     print()
    #     super().__init__(**kwargs)

    # def clean_option(self):
    #     return self.cleaned_data["option"]

    # def clean(self, *args, **kwargs):
    #     self.cleaned_data = super().clean(**kwargs)
    #     return self.cleaned_data


class TradeForm(forms.Form):
    # trade_with = forms.ModelChoiceField(queryset=Member.objects.all())
    trade_with = forms.IntegerField(validators=[MinValueValidator(1)], label="取引相手のID")
    star = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(200)], label="DeMiStar"
    )
    cash = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)], label="DeMiCash"
    )
    is_sender = forms.BooleanField(required=False, label="送信者はチェックをつけてください。")

    def clean(self):
        self.cleaned_data = super().clean()
        # Validation Error を発生させる。
        # star cash 両方0の時バリデーション
        # trade_with の値でTransactionがすでに存在してるか確認してvalidationエラー（self.request.userとか使って）
        key_list = list(self.cleaned_data.keys())
        if "star" in key_list and "cash" in key_list:
            if self.cleaned_data["star"] == 0 and self.cleaned_data["cash"] == 0:
                self.add_error(None, "DeMiStarかDeMiCashを送信(受信)してください。")
        try:
            trade_with = self.cleaned_data["trade_with"]
            if self.cleaned_data["is_sender"]:
                sender = self.oneself
                receiver = Member.objects.get(id=trade_with.id)
            else:
                sender = Member.objects.get(id=trade_with.id)
                receiver = self.oneself

            # 自分からは複数の取引を申請できない add errorはcleand_dataから削除する
            transaction = Transaction.objects.filter(
                is_canceled=False, is_done=False, requested_by=self.oneself
            )
            print("自分自身", self.oneself)
            if transaction.exists():
                self.add_error("trade_with", "すでに申請している取引があります。先に取引をキャンセルしてください。")
            self.cleaned_data.update({"sender": sender, "receiver": receiver})
        except:
            return self.cleaned_data
        return self.cleaned_data

    def clean_trade_with(self, *args, **kwargs):
        trade_with_id = self.cleaned_data.get("trade_with")
        try:
            trade_with = Member.objects.get(id=trade_with_id, is_present=True, is_superuser=False)
            if trade_with == self.oneself:
                raise ValidationError("自分自身は指定できません")
            return trade_with
        except ObjectDoesNotExist:
            raise ValidationError("指定したIDのユーザーは存在しません。")

    def clean_star(self, *args, **kwargs):
        key_list = list(self.cleaned_data.keys())
        is_sender = self.is_sender
        star_limit = Star.objects.get(user=self.oneself).star
        if "star" in key_list:
            star = self.cleaned_data["star"]
            if is_sender and star > star_limit:
                raise ValidationError("保有数を超える量は送信できません。")
        return star

    def clean_cash(self, *args, **kwargs):
        key_list = list(self.cleaned_data.keys())
        is_sender = self.is_sender
        cash_limit = Wallet.objects.get(user=self.oneself).cash
        if "cash" in key_list:
            cash = self.cleaned_data["cash"]
            if is_sender and cash > cash_limit:
                raise ValidationError("保有数を超える量は送信できません。")

        return cash

    def __init__(self, oneself=None, is_sender=None, *args, **kwargs):
        self.oneself = oneself
        self.is_sender = is_sender
        return super().__init__(*args, **kwargs)


class PurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=30, label="購入数")

    def __init__(self, oneself=None, quantity=None, product=None, *args, **kwargs):
        self.oneself = oneself
        self.quantity = quantity
        self.product = product
        return super().__init__(*args, **kwargs)

    def clean_quantity(self):
        price_sum = self.product.price * self.quantity
        wallet = Wallet.objects.get(user=self.oneself)
        if wallet.cash < price_sum:
            self.add_error("quantity", "保有額より高額な購入はできません")
        if self.quantity > self.product.stock:
            self.add_error("quantity", "購入量分の在庫がありません")
        self.cleaned_data["price_sum"] = price_sum
        return self.quantity
