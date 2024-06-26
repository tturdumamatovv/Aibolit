from django.urls import path

from .views import (ProductListView, CategoryListView, ProductDetailView, RecentlyViewedListView,
                    FavoriteToggleView, FavoriteListView, ProductOfTheDayListView)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products-of-the-day/', ProductOfTheDayListView.as_view(), name='product-of-the-day-list'),
    path('recently-viewed/', RecentlyViewedListView.as_view(), name='recently-viewed-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('favorites/toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
]
