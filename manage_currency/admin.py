from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Member, Team, Wallet, Star, Product, Purchase, Transaction

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # 編集時の画面のフィールド
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "job",
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
                    "is_employee",
                    "group",
                    "is_late",
                )
            },
        ),
    )


admin.site.register(Member, CustomUserAdmin)
admin.site.register(Wallet, admin.ModelAdmin)
admin.site.register(Star, admin.ModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Purchase, admin.ModelAdmin)
admin.site.register(Transaction, admin.ModelAdmin)
