from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Team(models.Model):
    leader = models.ForeignKey("Member", on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.leader.username + "チーム"


class Member(AbstractUser):
    class Job(models.TextChoices):
        ENGINEER = "Engineer", "エンジニア"
        DESIGINER = "Designer", "デザイナー"

    # オフィスメンバーかどうか
    is_employee = models.BooleanField(default=False)
    job = models.CharField(max_length=10, choices=Job.choices, default=Job.ENGINEER)
    group = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    # 遅刻したかどうか→遅刻した場合はキャッシュ配布の時最小単位を配布
    is_present = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Transaction(models.Model):
    # トレード申請について(以下の二つは一意)
    requested_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="requested_by")
    trade_with = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="trade_width")
    # 財移動の方向
    send_from = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="send_from")
    send_to = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="send_to")
    # やり取りされる財の数量
    star = models.IntegerField(validators=[MinValueValidator(0)])
    cash = models.IntegerField(validators=[MinValueValidator(0)])
    # 完了のフラグ
    is_done = models.BooleanField()


class Wallet(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    cash = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.user.username + "'s Cash"


class Star(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    star = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.user.username + "'s Star"


class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="product_images")
    price = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Purchase(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_delivered = models.BooleanField()

    def __str__(self):
        if self.is_delivered:
            is_done = "受け渡し済み"
        else:
            is_done = "未受け渡し"
        return self.user.username + ":" + self.product.name + " " + is_done


# class Quiz(models.Model):
#     answer=models.OneToOneField("Answer", on_delete=models.CASCADE)
#     option=

# class Answer(models.Model):
#     quiz=models.OneToOneField(Quiz, on_delete=models.CASCADE)
#     correct_option=


# class QuizOption(models.Model):
#     quiz=
