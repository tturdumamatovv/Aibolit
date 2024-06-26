# Generated by Django 4.2 on 2024-06-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Слаг')),
                ('content', models.TextField(verbose_name='Контент')),
                ('image', models.ImageField(blank=True, null=True, upload_to='static_pages/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
            ],
        ),
    ]
