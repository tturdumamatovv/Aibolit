from django.utils import timezone
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from decimal import Decimal

from apps.authentication.models import UserAddress
from apps.medicine.models import Product
from apps.order.models import Order, OrderItem, BonusConfiguration, DeliveryConfiguration


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.ostatok:
            raise serializers.ValidationError(
                f"Доступное количество продукта '{product.name}' на складе: {product.ostatok}")

        return data

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)


class UserAddressDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'address']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    delivery_method = serializers.ChoiceField(choices=Order.DELIVERY_CHOICES)
    delivery_address = serializers.PrimaryKeyRelatedField(queryset=UserAddress.objects.all(), required=False,
                                                          allow_null=True)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    delivery_time_choice = serializers.ChoiceField(choices=Order.DELIVERY_TIME_CHOICES, default='immediate')
    scheduled_delivery_time = serializers.DateTimeField(required=False, allow_null=True, format='%Y-%m-%dT%H:%M:%S')
    total_price = serializers.SerializerMethodField(read_only=True)
    total_price_after_bonus = serializers.SerializerMethodField(read_only=True)
    delivery_cost = serializers.SerializerMethodField(read_only=True)
    used_bonus_points = serializers.IntegerField(required=False, default=0)
    bonus_points_earned = serializers.SerializerMethodField(read_only=True)
    total_to_pay = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Order
        fields = ['items', 'delivery_method', 'delivery_address', 'payment_method', 'delivery_time_choice',
                  'scheduled_delivery_time', 'total_price', 'total_price_after_bonus', 'used_bonus_points',
                  'bonus_points_earned', 'delivery_cost', 'total_to_pay']

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_total_price(self, obj):
        total = Decimal('0.00')
        for item in obj.items.all():
            product = item.product
            if product.discounted_price:
                total += product.discounted_price * Decimal(item.quantity)
            else:
                total += product.price * Decimal(item.quantity)
        return total

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_total_price_after_bonus(self, obj):
        total_price = self.get_total_price(obj)
        used_bonus_points = obj.used_bonus_points
        total_price -= used_bonus_points
        return total_price

    @extend_schema_field(serializers.IntegerField())
    def get_bonus_points_earned(self, obj):
        total_price = sum(item.product.price * Decimal(item.quantity) for item in obj.items.all())
        bonus_configurations = BonusConfiguration.objects.filter(min_order_amount__lte=total_price).order_by('-min_order_amount')

        if bonus_configurations.exists():
            return bonus_configurations.first().bonus_points
        return 0

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_delivery_cost(self, obj):
        total_price = self.get_total_price(obj)
        delivery_configurations = DeliveryConfiguration.objects.all()

        if delivery_configurations.exists():
            delivery_configuration = delivery_configurations.first()
            free_shipping_threshold = delivery_configuration.free_shipping_threshold
            if free_shipping_threshold and total_price >= free_shipping_threshold:
                return Decimal('0.00')  # доставка бесплатна
            return delivery_configuration.delivery_cost
        return Decimal('0.00')

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2))
    def get_total_to_pay(self, obj):
        total_to_pay = self.get_total_price_after_bonus(obj) + self.get_delivery_cost(obj)
        return total_to_pay

    def validate_delivery_address(self, value):
        user = self.context['request'].user
        if value not in user.addresses.all():
            raise serializers.ValidationError({"error": "Вы можете выбирать только из своих адресов доставки."})
        return value

    def validate_items(self, value):
        for item in value:
            product = item['product']
            quantity = item['quantity']

            if quantity > product.ostatok:
                raise serializers.ValidationError(
                    f"Доступное количество продукта '{product.name}' на складе: {product.ostatok}")

        return value

    def validate_scheduled_delivery_time(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Нельзя указывать прошедшее время для запланированной доставки.")
        return value

    def validate_used_bonus_points(self, value):
        user = self.context['request'].user
        if value > user.bonus_points:
            raise serializers.ValidationError("У вас недостаточно бонусных баллов для использования.")
        return value


    def create(self, validated_data):
        items_data = validated_data.pop('items')
        delivery_method = validated_data.get('delivery_method')
        delivery_address = validated_data.get('delivery_address')
        delivery_time_choice = validated_data.get('delivery_time_choice')
        scheduled_delivery_time = validated_data.get('scheduled_delivery_time')
        used_bonus_points = validated_data.pop('used_bonus_points', 0)  # извлечение использованных бонусных баллов

        if delivery_method == 'courier' and not delivery_address:
            raise serializers.ValidationError("Для доставки курьером необходимо указать адрес доставки.")

        if delivery_time_choice == 'scheduled' and not scheduled_delivery_time:
            raise serializers.ValidationError("Если выбрали заплнированную доставку нужно указать дату и время.")

        order = Order(**validated_data)
        order.order_number = order.generate_order_number()  # Генерация уникального номера заказа

        # Учет использованных бонусных баллов при создании заказа
        order.used_bonus_points = used_bonus_points

        order.save()

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.delivery_address is None:
            representation.pop('delivery_address', None)
        if instance.scheduled_delivery_time is None:
            representation.pop('scheduled_delivery_time', None)
        return representation


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)
#     delivery_address = UserAddressDisplaySerializer()
#     total_price = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'delivery_address', 'delivery_method',
#                   'payment_method', 'delivery_time_choice',
#                   'scheduled_delivery_time', 'status', 'total_price']
#
#     def get_total_price(self, obj):
#         total = 0
#         for item in obj.items.all():
#             product = item.product
#             if product.discounted_price:
#                 total += product.discounted_price * item.quantity
#             else:
#                 total += product.price * item.quantity
#         return total
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if instance.delivery_address is None:
#             representation.pop('delivery_address', None)
#         if instance.scheduled_delivery_time is None:
#             representation.pop('scheduled_delivery_time', None)
#         return representation


class UserOrderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S', read_only=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_number', 'created_at', 'total_items', 'status']

    @extend_schema_field(serializers.IntegerField())
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
