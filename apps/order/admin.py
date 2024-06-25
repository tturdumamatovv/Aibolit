from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'delivery_method', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'delivery_method', 'payment_method']
    search_fields = ['user__username', 'user__email', 'id']
    readonly_fields = ['created_at', 'updated_at', 'user']
    fieldsets = (
        (None, {
            'fields': ('user', 'delivery_method', 'delivery_address', 'payment_method')
        }),
        ('Статус заказа', {
            'fields': ('status',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    list_filter = ['order__status']
    search_fields = ['order__user__username', 'order__user__email', 'product__name']
    readonly_fields = ['order', 'product']  # Поля, которые будут только для чтения
    list_editable = ['quantity']  # Поля, которые можно редактировать прямо из списка

    def has_add_permission(self, request):
        return False