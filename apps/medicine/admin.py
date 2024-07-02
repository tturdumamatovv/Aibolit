from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from apps.medicine.forms import CategoryAdminForm
from .models import (
    Category,
    Product,
    Purpose,
    ProductType,
    Volume,
    Indication,
    DosageForm,
    ProductImage
)
from .tasks import load_products_from_api


class PurposeInline(admin.TabularInline):
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
    readonly_fields = ['display_image']

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', obj.image.url)
        return format_html('<span style="color: red;">Нет изображения</span>')

    display_image.short_description = 'Изображение'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('related_products', 'similar_products')
    list_display = ('id', 'name', 'ostatok', 'price', 'manufacturer',
                    'country', 'category', 'is_product_of_the_day', 'display_image')
    search_fields = ('name', 'manufacturer', 'country')
    list_filter = ('category',)
    ordering = ('id',)
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"
    inlines = [ImageFormInline, PurposeInline, ProductTypeInline, VolumeInline, IndicationInline, DosageFormInline]
    actions = ['load_products_action', 'change_category_action']
    list_editable = ['is_product_of_the_day']

    def get_fields(self, request, obj=None):
        if obj:
            # При просмотре деталей конкретного товара
            return ('name', 'ostatok', 'price', 'manufacturer', 'country', 'category', 'is_product_of_the_day')
        else:
            # При просмотре списка товаров
            return ('name', 'ostatok', 'price', 'manufacturer', 'country', 'category', 'is_product_of_the_day', 'display_image')

    def get_fieldsets(self, request, obj=None):
        if obj:
            # При просмотре деталей конкретного товара
            return [
                (None, {'fields': ('name', 'ostatok', 'price', 'manufacturer', 'country', 'category', 'is_product_of_the_day')}),
            ]
        else:
            # При просмотре списка товаров
            return [
                (None, {'fields': ('name', 'ostatok', 'price', 'manufacturer', 'country', 'category', 'is_product_of_the_day', 'display_image')}),
            ]

    readonly_fields = ['display_image']  # Указываем поле, которое будет только для чтения

    def display_image(self, obj):
        main_image = obj.images.filter(main=True).first()
        if not main_image:
            main_image = obj.images.first()  # Если основное изображение не установлено, берем первое изображение

        if main_image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />', main_image.image.url)
        else:
            return format_html('<span style="color: red;">Нет изображений</span>')  # Если изображения отсутствуют

    display_image.short_description = 'Основное изображение'  # Название колонки в админке


    @admin.action(description='Загрузить товары из API')
    def load_products_action(modeladmin, request, queryset):
        load_products_from_api()
        modeladmin.message_user(request, "Задача на загрузку товаров была успешно поставлена в очередь.",
                                messages.SUCCESS)
        return HttpResponseRedirect(request.get_full_path())

    @admin.action(description="Изменить категории")
    def change_category_action(modeladmin, request, queryset):
        selected = request.POST.getlist("_selected_action")
        return HttpResponseRedirect(
            f"/admin/change_category/?ids={','.join(selected)}&action=change&next={request.get_full_path()}"
        )


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    form = CategoryAdminForm
    list_display = [
        "tree_actions",
        "indented_name",
        "parent",
    ]
    list_display_links = ("indented_name",)
    list_filter = [
        "parent"
    ]
    search_fields = ["id", 'name']
    list_select_related = ["parent"]
    mptt_level_indent = 20

    @admin.display(description="Название")
    def indented_name(self, instance):
        return mark_safe(
            '<div style="text-indent: {}px">{}</div>'.format(
                instance._mpttfield('level') * self.mptt_level_indent,
                instance.name
            )
        )
