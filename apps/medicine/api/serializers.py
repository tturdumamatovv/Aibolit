from rest_framework import serializers
from apps.medicine.models import Product, Category, ProductImage

from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'main')



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'ostatok', 'price', 'discount_percent', 'discounted_price', 'images')

    def to_representation(self, instance):
        main_image = instance.images.filter(main=True).first()
        if not main_image:
            main_image = instance.images.first()

        representation = super().to_representation(instance)
        if main_image:
            full_url = self.context['request'].build_absolute_uri(f"{settings.MEDIA_URL}{main_image.image}")
            representation['image'] = full_url
        else:
            representation['image'] = None

        # Remove images field as we already handled it
        representation.pop('images', None)

        # Only include discounted_price if it exists
        if instance.discounted_price is None:
            representation.pop('discounted_price', None)

        if instance.discount_percent is None or "0.00":
            representation.pop('discount_percent', None)

        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'discount_percent', 'discounted_price', 'price',
                  'storage_rules', 'manufacturer', 'country', 'expiration_date', 'dosage',
                  'category', 'dosage_form', 'packaging', 'composition', 'contraindications',
                  'indications', 'side_effects', 'images')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        main_image = instance.images.filter(main=True).first()
        if not main_image:
            main_image = instance.images.first()

        # Add all image URLs
        representation['images'] = [self.context['request'].build_absolute_uri(f"{settings.MEDIA_URL}{img.image}") for img in instance.images.all()]

        # Only include discounted_price if it exists
        if instance.discounted_price is None:
            representation.pop('discounted_price', None)

        # Only include discount_percent if it exists
        if instance.discount_percent is None or "0.00":
            representation.pop('discount_percent', None)

        return representation
