# Generated by Django 4.2 on 2024-06-24 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_category_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.IntegerField(unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='category',
            name='folder',
            field=models.BooleanField(default=False, verbose_name='Папка'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='Родительский код'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicine.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.IntegerField(unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='product',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Страна производства'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ostatok',
            field=models.IntegerField(verbose_name='Остаток'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sklad',
            field=models.CharField(max_length=255, verbose_name='Склад'),
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volumes', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Объем',
                'verbose_name_plural': 'Объемы',
            },
        ),
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose_type', models.CharField(choices=[('prescription', 'По назначению врача'), ('non_prescription', 'Без рецепта')], max_length=20, verbose_name='Тип назначения')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purposes', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Назначение',
                'verbose_name_plural': 'Назначения',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_types', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Вид товара',
                'verbose_name_plural': 'Виды товаров',
            },
        ),
        migrations.CreateModel(
            name='Indication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indications', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Показание',
                'verbose_name_plural': 'Показания',
            },
        ),
        migrations.CreateModel(
            name='DosageForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dosage_forms', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Форма выпуска',
                'verbose_name_plural': 'Формы выпуска',
            },
        ),
    ]
