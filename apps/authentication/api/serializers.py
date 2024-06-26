from rest_framework import serializers

from apps.authentication.models import User
from apps.authentication.models import UserAddress


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'full_name', 'date_of_birth', 'email')
        read_only_fields = ('full_name', 'date_of_birth', 'email')


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    fcm_token = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    receive_notifications = serializers.BooleanField(required=False, allow_null=True)


class UserRetireeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_retiree']


class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(read_only=True)
    retiree_card_front = serializers.ImageField(required=False, allow_null=True)
    retiree_card_back = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'full_name', 'date_of_birth', 'email', 'first_visit', 'is_retiree',
                  'retiree_card_front', 'retiree_card_back', 'bonus_points')
        read_only_fields = ('is_retiree', 'bonus_points')

    def validate(self, data):
        is_retiree = data.get('is_retiree', self.instance.is_retiree if self.instance else False)
        if is_retiree and not (data.get('retiree_card_front') and data.get('retiree_card_back')):
            raise serializers.ValidationError({"error": "Необходимо загрузить обе стороны карточки пенсионера."})
        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('is_retiree'):
            instance.is_retiree_card_approved = False
            instance.save()
        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'address']  # Include 'is_primary'
        read_only_fields = ['user', 'created_at']


class UserAddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [field.name for field in UserAddress._meta.fields if field.name not in ('id', 'user')]


class UserAddressUpdateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=False)
    is_primary = serializers.BooleanField(required=False)  # Include 'is_primary' as an optional field

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'address', 'is_primary']  # Include 'is_primary'
        read_only_fields = ['user', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    fcm_token = serializers.CharField(max_length=255, required=False)
    receive_notifications = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = User
        fields = ('fcm_token', 'receive_notifications')
