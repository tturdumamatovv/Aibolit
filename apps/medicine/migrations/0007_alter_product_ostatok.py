# Generated by Django 4.2 on 2024-07-02 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0006_alter_product_ostatok'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ostatok',
            field=models.FloatField(verbose_name='Остаток'),
        ),
    ]
