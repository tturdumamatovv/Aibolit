from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from apps.medicine.models import Product, Category, Favorite, RecentlyViewedProduct
from .filters import ProductFilter
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, FavoriteSerializer, RecentlyViewedSerializer


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

    def get_object(self):
        obj = super().get_object()
        # Создаем или обновляем запись RecentlyViewedProduct для текущего пользователя и просматриваемого товара
        if self.request.user.is_authenticated:
            RecentlyViewedProduct.objects.get_or_create(user=self.request.user, product=obj)
        return obj


class FavoriteToggleView(generics.GenericAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        product = serializer.validated_data['product_id']

        try:
            favorite = Favorite.objects.get(user=user, product=product)
            favorite.delete()
            return Response({"message": "Товар удален из избранного"}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            Favorite.objects.create(user=user, product=product)
            return Response({"message": "Товар добавлен в избранное"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')


class RecentlyViewedListView(generics.ListAPIView):
    queryset = RecentlyViewedProduct.objects.all()
    serializer_class = RecentlyViewedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecentlyViewedProduct.objects.filter(user=self.request.user).order_by('-viewed_at')


class ProductOfTheDayListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Product.objects.filter(is_product_of_the_day=True).order_by('?')
