from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, ProductViewSet, SupplierViewSet, CustomerViewSet,
    OrderViewSet, ReviewViewSet, ShippingViewSet, PaymentViewSet, StaffViewSet,
    PromotionViewSet, RegisterView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'shippings', ShippingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'staffs', StaffViewSet)
router.register(r'promotions', PromotionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
