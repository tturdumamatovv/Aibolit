from django.contrib import admin

from .models import Banner, Partner, DiscountInfo, StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'content', 'image', 'created_at', 'updated_at']
    list_display_links = ['title', 'slug']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'link']
    list_display_links = ['image']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'link']
    list_display_links = ['image']


@admin.register(DiscountInfo)
class DiscountInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'title', 'text']
    list_display_links = ['image']
