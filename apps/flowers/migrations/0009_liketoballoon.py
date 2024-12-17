# Generated by Django 5.1.2 on 2024-12-17 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0008_balloon_imagesofballoon_balloontranslation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LiketoBalloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('balloon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balloon_like', to='flowers.balloon', verbose_name='Выбрать')),
            ],
            options={
                'verbose_name': 'Лайк за воздушный шар ',
                'verbose_name_plural': 'Лайк за воздушный шар',
                'ordering': ['id'],
            },
        ),
    ]