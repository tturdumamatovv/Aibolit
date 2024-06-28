from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.medicine.models import Product


class StaticPage(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Заголовок'))
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_('Слаг'))
    content = models.TextField(verbose_name=_('Контент'))
    image = models.ImageField(upload_to='static_pages/', blank=True, null=True, verbose_name=_('Изображение'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Время создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Время обновления'))

    class Meta:
        verbose_name = _('Статическая страница')
        verbose_name_plural = _('Статические страницы')


class Banner(models.Model):
    image = models.FileField(upload_to='banners/', verbose_name=_('Изображение'))
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name=_('Продукт'), blank=True, null=True)

    class Meta:
        verbose_name = _('Баннер')
        verbose_name_plural = _('Баннеры')

    def __str__(self):
        return f'Баннер {self.id}'


class Partner(models.Model):
    image = models.FileField(upload_to='partners/', verbose_name=_('Изображение'))
    link = models.URLField(verbose_name=_('Ссылка'))

    class Meta:
        verbose_name = _('Партнёр')
        verbose_name_plural = _('Партнёры')

    def __str__(self):
        return f'Партнёр {self.id}'


class DiscountInfo(models.Model):
    image = models.ImageField(upload_to='discount_info/', verbose_name=_("Изображение"))
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    text = models.TextField(verbose_name=_("Текст"))

    class Meta:
        verbose_name = _("Информация о скидках")
        verbose_name_plural = _("Информация о скидках")

    def __str__(self):
        return f'Информация о скидках {self.id}'
