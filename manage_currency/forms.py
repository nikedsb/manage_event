from dataclasses import field
from pyexpat import model
from click import option
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import request
from .models import Member, QuizOption, Transaction
from django.core.validators import MaxValueValidator, MinValueValidator


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
    trade_with = forms.ModelChoiceField(queryset=Member.objects.all())
    star = forms.IntegerField(validators=[MinValueValidator(0)])
    cash = forms.IntegerField(validators=[MinValueValidator(0)])
    is_sender = forms.BooleanField()

    def clean(self):
        self.cleaned_data = super().cleaned_data()
        # Validation Error を発生させる。
        # star cash 両方0の時バリデーション
        # trade_with の値でTransactionがすでに存在してるか確認してvalidationエラー（self.request.userとか使って）
        return self.cleaned_data
