# Generated by Django 4.2.11 on 2024-05-16 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0004_homepage_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='tags',
        ),
    ]
