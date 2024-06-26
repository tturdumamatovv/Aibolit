from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.medicine.models import (
    Product,
    Category,
    Favorite,
    RecentlyViewedProduct
)
from .filters import ProductFilter
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    FavoriteSerializer,
    RecentlyViewedSerializer
)


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


def admin_change_category(request):
    ids = request.GET.get("ids", "").split(",")
    action = request.GET.get("action", "change")
    items = Product.objects.filter(id__in=ids)

    if request.method == "POST":
        category = request.POST.get("category")
        if action == "add":
            if category:
                for item in items:
                    item.category = Category.objects.get(id=category)
                    item.save()
                    messages.success(request, f"Added categories to {len(items)} product(s).")
        else:
            for item in items:
                item.category = Category.objects.get(id=category)
                item.save()
            messages.success(request, f"Changed the category of {len(items)} product(s).")

        next_url = request.GET.get("next", "/admin/medicine/product/")
        return HttpResponseRedirect(next_url)

    categories = Category.objects.all()
    return render(request, "admin/change_category.html", {"items": items, "categories": categories, "action": action})
