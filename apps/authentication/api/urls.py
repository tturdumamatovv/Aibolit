from django.urls import path

from apps.authentication.api.views import (
    UserLoginView,
    VerifyCodeView,
    UserProfileUpdateView,
    UserAddressCreateAPIView,
    UserAddressUpdateAPIView,
    UserAddressDeleteAPIView,
    UserDeleteAPIView,
    NotificationSettingsAPIView,
    UpdateUserRetireeStatusAPIView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_registration'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('user/update-retiree-status/', UpdateUserRetireeStatusAPIView.as_view(), name='update-retiree-status'),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),
    path('addresses/', UserAddressCreateAPIView.as_view(), name='create_address'),
    path('addresses/<int:pk>/update/', UserAddressUpdateAPIView.as_view(), name='update_address'),
    path('addresses/<int:pk>/delete/', UserAddressDeleteAPIView.as_view(), name='delete_address'),
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('notification-settings/', NotificationSettingsAPIView.as_view(), name='notification-settings'),
]
