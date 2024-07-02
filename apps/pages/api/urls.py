from django.urls import path

from apps.pages.api.views import (
    StaticPageDetailView,
    BannerListView,
    PartnerListView,
    DiscountInfoView
)

urlpatterns = [
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('partners/', PartnerListView.as_view(), name='partner-list'),
    path('static-pages/<slug:slug>/', StaticPageDetailView.as_view(), name='static-page-detail'),
    path('static-pages/about-us/', StaticPageDetailView.as_view(), name='about-us-page'),
    path('static-pages/delivery/', StaticPageDetailView.as_view(), name='about-us-page'),
    path('discount-info/', DiscountInfoView.as_view(), name='discount-info'),
]
