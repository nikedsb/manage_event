from logging import raiseExceptions
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.core.exceptions import ObjectDoesNotExist
from .models import Member, QuizOption, Transaction


class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "job")


class QuizForm(forms.Form):
    class QuizChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.option

    option = QuizChoiceField(
        queryset=QuizOption.objects.all(),
    )

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
    trade_with = forms.IntegerField(validators=[MinValueValidator(1)])
    star = forms.IntegerField(validators=[MinValueValidator(0)])
    cash = forms.IntegerField(validators=[MinValueValidator(0)])
    is_sender = forms.BooleanField(required=False)

    def clean(self):
        self.cleaned_data = super().clean()
        # Validation Error を発生させる。
        # star cash 両方0の時バリデーション
        # trade_with の値でTransactionがすでに存在してるか確認してvalidationエラー（self.request.userとか使って）
        key_list = list(self.cleaned_data.keys())
        if "star" in key_list and "cash" in key_list:
            if self.cleaned_data["star"] == 0 and self.cleaned_data["cash"] == 0:
                raise ValidationError("DeMiStarかDeMiCashを送信(受信)してください。")

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

    def __init__(self, oneself, star_limit, cash_limit, *args, **kwargs):

        star_validator = self.base_fields["star"].validators
        cash_validators = self.base_fields["cash"].validators
        if len(star_validator) == 1:
            star_validator.append(MaxValueValidator(star_limit))
        if len(cash_validators) == 1:
            cash_validators.append(MaxValueValidator(cash_limit))
        self.oneself = oneself
        return super().__init__(*args, **kwargs)
