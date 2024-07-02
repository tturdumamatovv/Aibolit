from django.urls import path

from .views import OrderCreateView, UserOrderListView

urlpatterns = [
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    # path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/', UserOrderListView.as_view(), name='user-orders'),
]
