# Generated by Django 4.2 on 2024-06-26 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True, verbose_name='Код')),
                ('parent_code', models.IntegerField(blank=True, null=True, verbose_name='Родительский код')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('folder', models.BooleanField(default=False, verbose_name='Папка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('sklad', models.CharField(max_length=255, verbose_name='Склад')),
                ('ostatok', models.IntegerField(verbose_name='Остаток')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Производитель')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Страна производства')),
                ('expiration_date', models.CharField(blank=True, max_length=255, null=True, verbose_name='Срок годности')),
                ('dosage', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дозировка')),
                ('dosage_form', models.CharField(blank=True, max_length=255, null=True, verbose_name='Форма выпуска')),
                ('packaging', models.CharField(blank=True, max_length=255, null=True, verbose_name='В упаковке')),
                ('composition', models.TextField(blank=True, null=True, verbose_name='Состав')),
                ('contraindications', models.TextField(blank=True, null=True, verbose_name='Противопоказания')),
                ('indications', models.TextField(blank=True, null=True, verbose_name='Показания к применению')),
                ('side_effects', models.TextField(blank=True, null=True, verbose_name='Побочные действия')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('storage_rules', models.TextField(blank=True, null=True, verbose_name='Правила хранения')),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Скидка, %')),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена со скидкой')),
                ('is_product_of_the_day', models.BooleanField(default=False, verbose_name='Товар дня')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='medicine.category', verbose_name='Категория')),
                ('related_products', models.ManyToManyField(blank=True, to='medicine.product', verbose_name='Другие варианты этого продукта')),
                ('similar_products', models.ManyToManyField(blank=True, to='medicine.product', verbose_name='Похожие продукты')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_volumes', to='medicine.product', verbose_name='Продукт')),
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
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_purposes', to='medicine.product', verbose_name='Продукт')),
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
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images', verbose_name='Картинка')),
                ('main', models.BooleanField(default=False, verbose_name='Основное изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Изображение продукта',
                'verbose_name_plural': 'Изображения продуктов',
            },
        ),
        migrations.CreateModel(
            name='Indication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_indications', to='medicine.product', verbose_name='Продукт')),
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
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_dosage_forms', to='medicine.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Форма выпуска',
                'verbose_name_plural': 'Формы выпуска',
            },
        ),
        migrations.CreateModel(
            name='RecentlyViewedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicine.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recently_viewed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-viewed_at'],
                'unique_together': {('user', 'product')},
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='medicine.product', verbose_name='Продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользлватель')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные товары',
                'unique_together': {('user', 'product')},
            },
        ),
    ]