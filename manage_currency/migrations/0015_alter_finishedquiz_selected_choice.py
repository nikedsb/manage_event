# Generated by Django 4.0.4 on 2022-05-20 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_currency', '0014_remove_finishedquiz_quizes_finishedquiz_quiz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finishedquiz',
            name='selected_choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_choice', to='manage_currency.quizoption'),
        ),
    ]
