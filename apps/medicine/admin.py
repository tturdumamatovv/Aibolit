from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from mptt.admin import DraggableMPTTAdmin

from apps.medicine.forms import CategoryAdminForm
from .models import (Category, Product, Purpose, ProductType, Volume, Indication, DosageForm, ProductImage)
from .tasks import load_products_from_api


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
    filter_horizontal = ('related_products', 'similar_products')
    list_display = ('code', 'name', 'sklad', 'ostatok', 'price', 'manufacturer',
                    'country', 'category', 'is_product_of_the_day')
    search_fields = ('name', 'manufacturer', 'country')
    list_filter = ('category',)
    ordering = ('id',)
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"
    inlines = [ImageFormInline, PurposeInline, ProductTypeInline, VolumeInline, IndicationInline, DosageFormInline]
    actions = ['load_products_action', 'change_category_action']
    list_editable = ['is_product_of_the_day']

    @admin.action(description='Загрузить товары из API')
    def load_products_action(modeladmin, request, queryset):
        load_products_from_api.delay()
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
