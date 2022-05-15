from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Team(models.Model):
    leader = models.ForeignKey("Member", on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0)])


class Member(AbstractUser):
    class Job(models.TextChoices):
        ENGINEER = "Engineer", "エンジニア"
        DESIGINER = "Designer", "デザイナー"

    # オフィスメンバーかどうか
    is_staff = models.BooleanField()
    job = models.CharField(max_length=10, choices=Job.choices)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)


class Transaction(models.Model):
    # トレード申請について(以下の二つは一意)
    requested_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    trade_with = models.ForeignKey(Member, on_delete=models.CASCADE)
    # 財移動の方向
    send_from = models.ForeignKey(Member, on_delete=models.CASCADE)
    send_to = models.ForeignKey(Member, on_delete=models.CASCADE)
    # やり取りされる財の数量
    star = models.IntegerField(validators=[MinValueValidator(0)])
    cash = models.IntegerField(validators=[MinValueValidator(0)])
    # 完了のフラグ
    is_done = models.BooleanField()


class Wallet(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    cash = models.IntegerField(validators=[MinValueValidator(0)])


class Star(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    star = models.IntegerField(validators=[MinValueValidator(0)])


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(validators=[MinValueValidator(0)])


class Purchase(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_delivered = models.BooleanField()


# class Quiz(models.Model):
#     answer=models.OneToOneField("Answer", on_delete=models.CASCADE)
#     option=

# class Answer(models.Model):
#     quiz=models.OneToOneField(Quiz, on_delete=models.CASCADE)
#     correct_option=


# class QuizOption(models.Model):
#     quiz=
