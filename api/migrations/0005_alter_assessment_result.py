# Generated by Django 5.1.4 on 2025-01-11 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_question_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='result',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
