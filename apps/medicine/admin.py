from django.contrib import admin

from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'parent_code', 'name', 'folder')
    search_fields = ('name',)
    list_filter = ('folder',)
    ordering = ('code',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sklad', 'ostatok', 'price', 'manufacturer', 'country', 'category')
    search_fields = ('name', 'manufacturer', 'country')
    list_filter = ('category',)
    ordering = ('code',)
