# Generated by Django 5.1.2 on 2024-12-01 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Электронная почта')),
                ('username', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Фамилия')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватар')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
