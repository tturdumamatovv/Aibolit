from django.urls import path

from .views import (
    ProductListView,
    CategoryListView,
    ProductDetailView,
    FavoriteToggleView,
    FavoriteListView,
    RecentlyViewedListView,
    ProductOfTheDayListView,
    search_products

)


urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('favorites/toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),

    path('recently-viewed/', RecentlyViewedListView.as_view(), name='recently-viewed'),
    path('product-of-the-day/', ProductOfTheDayListView.as_view(), name='recently-viewed'),
    path('search/', search_products, name='api_search_products'),
]
