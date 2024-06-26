from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
# from namito.catalog.admin import ReviewInline
# from namito.orders.admin import OrderHistoryInline
from apps.authentication.models import User, UserAddress


class AddressInline(admin.StackedInline):
    model = UserAddress
    extra = 0


class UserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'email', 'is_staff', 'date_of_birth')
    list_filter = ('is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'bonus_points', 'password')}),
        ('Личная информация', {'fields': ('full_name', 'date_of_birth', 'email',
                                          'is_retiree', 'retiree_card_front', 'retiree_card_back',
                                          'is_retiree_approved')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone_number', 'email')
    ordering = ('phone_number',)
    filter_horizontal = ('groups', 'user_permissions',)
    inlines = [AddressInline]
    # inlines = [ReviewInline, OrderHistoryInline, AddressInline]


admin.site.register(User, UserAdmin)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    list_filter = ('is_primary',)
    search_fields = ('address', 'user__username', 'user__email')
    ordering = ('-created_at',)
