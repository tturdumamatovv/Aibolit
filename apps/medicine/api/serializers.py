# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from django.conf import settings
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

# from apps.medicine.documents import ProductDocument
from apps.medicine.models import Product, Category, ProductImage, Favorite, RecentlyViewedProduct


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

        representation.pop('images', None)

        if instance.discounted_price is None:
            representation.pop('discounted_price', None)

        if instance.discount_percent is None or instance.discount_percent == 0.00:
            representation.pop('discount_percent', None)

        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    related_products = serializers.SerializerMethodField()
    similar_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'discount_percent', 'discounted_price', 'price',
                  'storage_rules', 'manufacturer', 'country', 'expiration_date', 'dosage',
                  'category', 'dosage_form', 'packaging', 'composition', 'contraindications',
                  'indications', 'side_effects', 'images', 'related_products', 'similar_products')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        main_image = instance.images.filter(main=True).first()
        if not main_image:
            main_image = instance.images.first()

        # Add all image URLs
        representation['images'] = [
            {
                'image': self.context['request'].build_absolute_uri(f"{settings.MEDIA_URL}{img.image}"),
                'main': img.main  # Include 'main' field
            }
            for img in instance.images.all()
        ]

        # Only include discounted_price if it exists
        if instance.discounted_price is None:
            representation.pop('discounted_price', None)

        # Only include discount_percent if it exists and not "0.00"
        if instance.discount_percent is None or instance.discount_percent == 0.00:
            representation.pop('discount_percent', None)

        return representation

    def get_related_products(self, instance):
        # Serialize related products
        related_products = instance.related_products.all()
        serializer = ProductSerializer(related_products, many=True, context=self.context)
        return serializer.data

    def get_similar_products(self, instance):
        # Serialize related products
        related_products = instance.related_products.all()
        serializer = ProductSerializer(related_products, many=True, context=self.context)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product_id']
        favorite, created = Favorite.objects.get_or_create(user=user, product=product)
        return favorite


class RecentlyViewedSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = RecentlyViewedProduct
        fields = ('id', 'product', 'viewed_at')


# class ProductDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document = ProductDocument
#         fields = (
#             'name',
#         )
