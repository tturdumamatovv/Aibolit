from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.medicine.models import (
    Product,
    Category,
    Favorite,
    RecentlyViewedProduct, ProductImage
)
from apps.medicine.forms import ProductImageForm
from .filters import ProductFilter
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    CategorySerializer,
    FavoriteSerializer,
    RecentlyViewedSerializer
)
# from ..documents import ProductDocument
from ..documents import ProductDocument


class CustomPagination(PageNumberPagination):
    page_size = 20


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


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
    pagination_class = CustomPagination

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')


class RecentlyViewedListView(generics.ListAPIView):
    queryset = RecentlyViewedProduct.objects.all()
    serializer_class = RecentlyViewedSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return RecentlyViewedProduct.objects.filter(user=self.request.user).order_by('-viewed_at')


class ProductOfTheDayListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

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


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('q')
    if query:
        search_results = ProductDocument.search().query("match", name=query)
    else:
        search_results = ProductDocument.search()

    products = [hit.to_dict() for hit in search_results]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def change_image_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Если основное изображение, то сначала сбросим флаг у всех остальных изображений продукта
            if form.cleaned_data.get('main'):
                ProductImage.objects.filter(product=product).update(main=False)

            # Сохраняем новое изображение
            new_image = form.save(commit=False)
            new_image.product = product
            new_image.save()

            return JsonResponse({'status': 'success', 'image_url': new_image.image.url})
    return JsonResponse({'status': 'error'})