from django.urls import path

from .views import ProductListView, CategoryListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
