# Generated by Django 4.2 on 2024-06-24 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0009_productimage_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='indications',
            field=models.TextField(blank=True, null=True, verbose_name='Показания к применению'),
        ),
    ]
