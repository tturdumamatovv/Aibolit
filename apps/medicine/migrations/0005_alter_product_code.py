# Generated by Django 4.2 on 2024-07-02 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0004_alter_productimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Код'),
        ),
    ]
