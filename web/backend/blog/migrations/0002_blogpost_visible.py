# Generated by Django 4.2.11 on 2024-09-26 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
