# Generated by Django 4.2 on 2024-06-24 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0010_product_indications'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='related_products',
            field=models.ManyToManyField(blank=True, to='medicine.product', verbose_name='Другие варианты этого продукта'),
        ),
    ]