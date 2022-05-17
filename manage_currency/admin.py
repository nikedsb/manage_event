from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import response
from .models import (
    Member,
    Team,
    Wallet,
    Star,
    Product,
    Purchase,
    Transaction,
    Answer,
    Quiz,
    QuizOption,
    FinishedQuiz,
)
from .create_team import culc_team_num, create_team

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # 編集時の画面のフィールド
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "job",
                    "is_present",
                    "is_employee",
                    "group",
                    "is_late",
                )
            },
        ),
    )
    # データベースに追加時のフィールド
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "job",
                    "is_present",
                    "is_employee",
                    "group",
                    "is_late",
                )
            },
        ),
    )
    list_display = ["username", "is_employee", "job", "group", "is_present", "is_late"]
    list_filter = ("is_present", "is_employee", "is_staff", "is_superuser")


class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "cash"]


class StarAdmin(admin.ModelAdmin):
    list_display = ["user", "star"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "is_delivered"]
    list_filter = ("is_delivered",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "requested_by",
        "trade_with",
        "send_from",
        "send_to",
        "star",
        "cash",
        "is_done",
    ]


class TeamAdmin(admin.ModelAdmin):
    list_display = ["leader", "score"]

    def changelist_view(self, request, extra_context=None):
        if request.method == "POST" and request.POST.getlist("create_team"):
            # チーム分け処理
            # エンジニア
            # print(culc_team_num("Engineer"))
            # print(culc_team_num("Designer"))
            print(create_team(culc_team_num("Engineer")))

        return super().changelist_view(request)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["quiz", "correct_option"]


class QuizOptionAdmin(admin.ModelAdmin):
    list_display = ["quiz", "option"]


class QuizAdmin(admin.ModelAdmin):
    list_display = ["content", "answer", "primary", "is_active"]


class FinishedQuizAdmin(admin.ModelAdmin):
    list_display = ["team"]


admin.site.register(Member, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Star, StarAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizOption, QuizOptionAdmin)
admin.site.register(FinishedQuiz, FinishedQuizAdmin)
