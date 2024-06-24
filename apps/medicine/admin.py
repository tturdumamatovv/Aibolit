from django.contrib import admin
from .models import (Category, Product, Purpose, ProductType, Volume, Indication, DosageForm, ProductImage)


class PurposeInline(admin.TabularInline):  # или admin.StackedInline для более детализированного отображения
    model = Purpose
    extra = 0


class ProductTypeInline(admin.TabularInline):
    model = ProductType
    extra = 1


class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 1


class IndicationInline(admin.TabularInline):
    model = Indication
    extra = 1


class DosageFormInline(admin.TabularInline):
    model = DosageForm
    extra = 1


class ImageFormInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sklad', 'ostatok', 'price', 'manufacturer', 'country', 'category')
    search_fields = ('name', 'manufacturer', 'country')
    list_filter = ('category',)
    ordering = ('code',)
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"
    inlines = [ImageFormInline, PurposeInline, ProductTypeInline, VolumeInline, IndicationInline, DosageFormInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'parent_code', 'name', 'folder')
    search_fields = ('name',)
    list_filter = ('folder',)
    ordering = ('code',)
    verbose_name = "Категория"
    verbose_name_plural = "Категории"