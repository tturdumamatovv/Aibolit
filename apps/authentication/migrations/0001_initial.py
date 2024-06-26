# Generated by Django 4.2 on 2024-06-26 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=13, unique=True, verbose_name='Номер телефона')),
                ('code', models.CharField(blank=True, max_length=4, null=True, verbose_name='Код')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Работник')),
                ('full_name', models.CharField(blank=True, max_length=255, verbose_name='Полное имя')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Имейл')),
                ('first_visit', models.BooleanField(default=True, verbose_name='Дата первого визита')),
                ('fcm_token', models.CharField(blank=True, max_length=255, null=True, verbose_name='Токен')),
                ('receive_notifications', models.BooleanField(blank=True, default=False, null=True, verbose_name='Получать уведомления')),
                ('is_retiree', models.BooleanField(default=False, verbose_name='Пенсионер')),
                ('retiree_card_front', models.ImageField(blank=True, null=True, upload_to='retiree_cards/', verbose_name='Лицевая сторона карточки пенсионера')),
                ('retiree_card_back', models.ImageField(blank=True, null=True, upload_to='retiree_cards/', verbose_name='Оборотная сторона карточки пенсионера')),
                ('is_retiree_approved', models.BooleanField(default=False, verbose_name='Прошел модерацию')),
                ('bonus_points', models.PositiveIntegerField(default=0, verbose_name='Бонусные баллы')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_primary', models.BooleanField(default=False, verbose_name='Главный')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Адрес пользователя',
                'verbose_name_plural': 'Адреса пользователей',
                'ordering': ['-created_at'],
            },
        ),
    ]
