from django.db import models
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField
from mptt.models import MPTTModel, TreeForeignKey
from unidecode import unidecode
from django.utils.text import slugify

from apps.authentication.models import User


class Category(MPTTModel, models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name=_('Слаг'))
    image = models.ImageField(null=True, blank=True, verbose_name=_('Изображение'))
    background_color = ColorField(default='#FF0000', null=True, verbose_name=_('Фоновый цвет'))
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                            related_name="children", verbose_name=_("Родительская категория"))
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True, verbose_name=_('Порядок'))

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['tree_id', 'lft']

    class MPTTMeta:
        order_insertion_by = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name))
            unique_slug = base_slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    code = models.IntegerField(unique=True, verbose_name=_("Код"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    sklad = models.CharField(max_length=255, verbose_name=_("Склад"))
    ostatok = models.IntegerField(verbose_name=_("Остаток"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    manufacturer = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Производитель"))
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Страна производства"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Категория"))
    expiration_date = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Срок годности"))
    dosage = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Дозировка"))
    dosage_form = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Форма выпуска"))
    packaging = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("В упаковке"))
    composition = models.TextField(blank=True, null=True, verbose_name=_("Состав"))
    contraindications = models.TextField(blank=True, null=True, verbose_name=_("Противопоказания"))
    indications = models.TextField(blank=True, null=True, verbose_name=_("Показания к применению"))
    side_effects = models.TextField(blank=True, null=True, verbose_name=_("Побочные действия"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание"))
    storage_rules = models.TextField(blank=True, null=True, verbose_name=_("Правила хранения"))
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                           verbose_name=_("Скидка, %"))
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                           verbose_name=_("Цена со скидкой"))
    related_products = models.ManyToManyField('self', blank=True, verbose_name=_("Другие варианты этого продукта"))
    similar_products = models.ManyToManyField('self', blank=True, verbose_name=_("Похожие продукты"))
    is_product_of_the_day = models.BooleanField(default=False, verbose_name=_("Товар дня"))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.discount_percent:
            self.discounted_price = self.price * (1 - self.discount_percent / 100)
        else:
            self.discounted_price = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("Продукт"))
    image = models.ImageField(upload_to='product_images', verbose_name=_("Картинка"))
    main = models.BooleanField(default=False, verbose_name=_("Основное изображение"))

    def __str__(self):
        return f"Изображение для {self.product.name}"

    class Meta:
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображения продуктов")


class Purpose(models.Model):
    PRODUCT_PRESCRIPTION = 'prescription'
    PRODUCT_NON_PRESCRIPTION = 'non_prescription'

    PRODUCT_CHOICES = [
        (PRODUCT_PRESCRIPTION, _('По назначению врача')),
        (PRODUCT_NON_PRESCRIPTION, _('Без рецепта')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_purposes', verbose_name=_("Продукт"))
    purpose_type = models.CharField(max_length=20, choices=PRODUCT_CHOICES, verbose_name=_("Тип назначения"))

    def __str__(self):
        return self.purpose_type

    class Meta:
        verbose_name = _("Назначение")
        verbose_name_plural = _("Назначения")


class ProductType(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_types', verbose_name=_("Продукт"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Вид товара")
        verbose_name_plural = _("Виды товаров")


class Volume(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_volumes', verbose_name=_("Продукт"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Объем")
        verbose_name_plural = _("Объемы")


class Indication(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_indications', verbose_name=_("Продукт"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Показание")
        verbose_name_plural = _("Показания")


class DosageForm(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_dosage_forms', verbose_name=_("Продукт"))
    name = models.CharField(max_length=255, verbose_name=_("Название"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Форма выпуска")
        verbose_name_plural = _("Формы выпуска")


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name=_("Пользлватель"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name=_("Продукт"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата добавления"))

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = _("Избранное")
        verbose_name_plural = _("Избранные товары")

    def __str__(self):
        return f"{self.user} - {self.product.name}"


class RecentlyViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'product')
