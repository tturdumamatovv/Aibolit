import random

from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.authentication.models import UserAddress
from apps.medicine.models import Product



class Order(models.Model):
    DELIVERY_CHOICES = (
        ('courier', 'Курьер'),
        ('pickup', 'Самовывоз'),
    )

    PAYMENT_CHOICES = (
        ('online', 'Онлайн'),
        ('on_delivery', 'При доставке'),
    )

    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    )

    DELIVERY_TIME_CHOICES = (
        ('immediate', 'Как можно скорее'),
        ('scheduled', 'Запланированная доставка'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, verbose_name=_("Способ доставки"))
    delivery_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL,
                                         null=True, blank=True, verbose_name=_("Адрес доставки"))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name=_("Способ оплаты"))
    delivery_time_choice = models.CharField(max_length=20, choices=DELIVERY_TIME_CHOICES, default='immediate',
                                           verbose_name=_("Выбор времени доставки"))
    scheduled_delivery_time = models.DateTimeField(null=True, blank=True, verbose_name=_("Дата и время доставки"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_("Статус"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    order_number = models.CharField(max_length=6, unique=True, verbose_name=_("Номер заказа"))

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

    def complete_order(self):
        if self.status == 'completed':
            for item in self.items.all():
                product = item.product
                product.ostatok -= item.quantity
                product.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if self.pk:  # Если заказ уже существует (не новое создание)
            old_order = Order.objects.get(pk=self.pk)
            if old_order.status != 'completed' and self.status == 'completed':
                self.complete_order()
        super().save(*args, **kwargs)

    @transaction.atomic
    def generate_order_number(self):
        while True:
            number = f"{random.randint(100000, 999999)}"
            if not Order.objects.filter(order_number=number).exists():
                return number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_("Заказ"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Продукт"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Количество"))

    class Meta:
        verbose_name = _("Элемент заказа")
        verbose_name_plural = _("Элементы заказа")
