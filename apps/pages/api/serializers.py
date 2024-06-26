from rest_framework import serializers

from apps.medicine.api.serializers import ProductSerializer
from apps.medicine.models import Product
from apps.pages.models import StaticPage, Banner, Partner, DiscountInfo


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ['title', 'slug', 'content', 'image', 'created_at', 'updated_at']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'image', 'link']


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'image', 'link']


class DiscountInfoSerializer(serializers.ModelSerializer):
    discounted_products = serializers.SerializerMethodField()

    class Meta:
        model = DiscountInfo
        fields = ['image', 'title', 'text', 'discounted_products']

    def get_discounted_products(self, obj):
        discounted_products = Product.objects.filter(discount_percent__gt=0)
        return ProductSerializer(discounted_products, many=True).data
