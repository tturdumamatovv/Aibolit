# views.py
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from django_filters import rest_framework as filters

from apps.medicine.models import Product, Category
from .filters import ProductFilter
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
