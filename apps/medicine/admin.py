from django.contrib import admin
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
# from .tasks import load_products_from_api

from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'parent_code', 'name', 'folder')
    search_fields = ('name',)
    list_filter = ('folder',)
    ordering = ('code',)


@admin.action(description='Загрузить товары из API')
def load_products_action(modeladmin, request, queryset):
    # load_products_from_api.delay()
    modeladmin.message_user(request, "Задача на загрузку товаров была успешно поставлена в очередь.", messages.SUCCESS)
    return HttpResponseRedirect(request.get_full_path())

class ProductAdmin(admin.ModelAdmin):
    actions = [load_products_action]

admin.site.register(Product, ProductAdmin)