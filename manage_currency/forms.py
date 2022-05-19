from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member


class SignUpForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "job")


class QuizForm(forms.Form):
    option = forms.ChoiceField(label="選択肢")

    def __init__(self, options=None, *args, **kwargs):
        # base_filedにフィールドが入っていて、インスタンスごとにコピーされる→Bseformのコンストラクタで
        # 動的な選択肢の受け渡し
        self.base_fields["option"].choices = options
        super().__init__(self, *args, **kwargs)
