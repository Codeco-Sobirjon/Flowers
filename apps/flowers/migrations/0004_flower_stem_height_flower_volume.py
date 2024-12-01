# Generated by Django 5.1.2 on 2024-12-01 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0003_alter_imagesofflower_flower'),
    ]

    operations = [
        migrations.AddField(
            model_name='flower',
            name='stem_height',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Высота стебля'),
        ),
        migrations.AddField(
            model_name='flower',
            name='volume',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Объём'),
        ),
    ]
