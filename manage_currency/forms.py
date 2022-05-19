from click import option
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member, QuizOption


class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "job")


class QuizForm(forms.Form):
    # option = forms.ChoiceField(label="選択肢")
    option = forms.ModelChoiceField(
        queryset=QuizOption.objects.all(),
        required=False,
    )
    # name = forms.CharField(max_length=29)

    # def __init__(self, option=None, *args, **kwargs):
    #     # base_filedにフィールドが入っていて、インスタンスごとにコピーされる→Bseformのコンストラクタで
    #     # 動的な選択肢の受け渡し
    #     self.base_fields["option"].choices = option
    #     print()
    #     super().__init__(**kwargs)

    # def clean_option(self):
    #     return self.cleaned_data["option"]

    # def clean(self):

    #     return None
