from django.db import models

# Create your models here.


class StaticPage(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name=_('Заголовок'))
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name=_('Слаг'))
    content = models.TextField(verbose_name=_('Контент'))
    image = models.ImageField(upload_to='static_pages/', blank=True, null=True, verbose_name=_('Изображение'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Время создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Время обновления'))