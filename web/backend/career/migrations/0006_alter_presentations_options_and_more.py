# Generated by Django 4.2.11 on 2024-05-25 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0005_presentations_publications'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentations',
            options={'verbose_name': 'Presentations', 'verbose_name_plural': 'Presentations'},
        ),
        migrations.AlterModelOptions(
            name='publications',
            options={'verbose_name': 'Publications', 'verbose_name_plural': 'Publications'},
        ),
        migrations.AlterField(
            model_name='presentations',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='presentation/', verbose_name='presentation_image'),
        ),
        migrations.AlterField(
            model_name='publications',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='publication/', verbose_name='publication_image'),
        ),
    ]
