from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.order.models import Order
from .serializers import OrderCreateSerializer, UserOrderSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class OrderListView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)


class UserOrderListView(generics.ListAPIView):
    serializer_class = UserOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
