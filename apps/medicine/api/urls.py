from django.urls import path

from .views import ProductListView, CategoryListView, ProductDetailView, FavoriteToggleView, FavoriteListView, \
    search_products

#,ProductDocumentView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),

    path('favorites/toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('search/', search_products, name='api_search_products'),

]
