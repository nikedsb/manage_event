# Generated by Django 4.0.4 on 2022-05-17 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_currency', '0007_answer_quiz_quizoption_finishedquiz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_currency.team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]