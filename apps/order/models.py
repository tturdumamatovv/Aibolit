import random

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import UserAddress
from apps.medicine.models import Product


class DeliveryConfiguration(models.Model):
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_('Стоимость доставки')
                                        , blank=True, null=True)
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                  verbose_name=_('Порог бесплатной доставки'))

    class Meta:
        verbose_name = _('Конфигурация доставки')
        verbose_name_plural = _('Конфигурации доставки')

    def __str__(self):
        return f'Стоимость доставки: {self.delivery_cost}, Порог бесплатной доставки: {self.free_shipping_threshold}'


class BonusConfiguration(models.Model):
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Минимальная сумма заказа'))
    bonus_points = models.PositiveIntegerField(verbose_name=_('Бонусные баллы'))


    class Meta:
        verbose_name = _('Конфигурация бонусов')
        verbose_name_plural = _('Конфигурации бонусов')

    def __str__(self):
        return f'{self.min_order_amount} - {self.bonus_points} баллов'


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
    used_bonus_points = models.PositiveIntegerField(default=0, verbose_name=_('Использованные бонусные баллы'))

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    def __str__(self):
        return f"Order #{self.id} - {self.user}"

    def use_bonus_points(self, points_to_use):
        if points_to_use <= self.user.bonus_points:
            self.used_bonus_points = points_to_use
            self.user.bonus_points -= points_to_use
            self.user.save()
            return True
        return False

    def complete_order(self):
        if self.status == 'completed':
            for item in self.items.all():
                product = item.product
                product.ostatok -= item.quantity
                product.save()

            self.assign_bonus_points()

            # При завершении заказа также учитываем использованные бонусные баллы
            if self.used_bonus_points > 0:
                self.user.bonus_points -= self.used_bonus_points
                self.user.save()

    def assign_bonus_points(self):
        total_price = sum(item.product.price * item.quantity for item in self.items.all())
        bonus_configurations = BonusConfiguration.objects.filter(min_order_amount__lte=total_price).order_by('-min_order_amount')

        if bonus_configurations.exists():
            bonus_points = bonus_configurations.first().bonus_points
            self.user.bonus_points += bonus_points
            self.user.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if self.pk:  # Если заказ уже существует
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
