from django.urls import path

from .views import (ProductListView, CategoryListView, ProductDetailView, RecentlyViewedListView,
                    FavoriteToggleView, FavoriteListView, ProductOfTheDayListView)
from .views import ProductListView, CategoryListView, ProductDetailView, FavoriteToggleView, FavoriteListView, \
    ProductDocumentViewSet

router = DefaultRouter()
router.register(r'product-search', ProductDocumentViewSet, basename='productdocument')
urlpatterns = [
    path('', include(router.urls)),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('favorites/toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
]
