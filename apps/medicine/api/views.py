# views.py
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from apps.medicine.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from apps.medicine.tasks import add

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        result = add.delay(4, 4)
        print(result.get())  # Должен вывести 8
        return super(ProductListView, self).get_queryset()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
