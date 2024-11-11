from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Category, Product, Supplier, Customer, Order, Review, Shipping, Payment, Staff, Promotion
from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer, SupplierSerializer, 
    CustomerSerializer, OrderSerializer, ReviewSerializer, ShippingSerializer, 
    PaymentSerializer, StaffSerializer, PromotionSerializer, RegisterSerializer
)
from .permissions import IsAdmin, IsAdminOrManager, IsManager, IsCustomer

class RegisterView(APIView):    
    permission_classes = [AllowAny]  # Allow anyone to access the registration view
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['role', 'username']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']
    permission_classes = [IsAdmin]  # Only Admin can manage users

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    permission_classes = [IsAdmin]  # Admin or Manager can manage categories

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name', 'price', 'categories']
    ordering_fields = ['name', 'price']
    ordering = ['name']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage products

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage suppliers

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['user', 'phone']
    ordering_fields = ['user', 'phone']
    ordering = ['user']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage customers

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['customer', 'order_date', 'total_amount']
    ordering_fields = ['order_date', 'total_amount']
    ordering = ['order_date']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage orders

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['customer', 'product', 'rating']
    ordering_fields = ['review_date', 'rating']
    ordering = ['review_date']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage reviews

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['order', 'shipped_date']
    ordering_fields = ['shipped_date']
    ordering = ['shipped_date']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage shipping

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['order', 'payment_date', 'amount']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['payment_date']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage payments

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['user', 'phone']
    ordering_fields = ['user', 'phone']
    ordering = ['user']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage staff

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['product', 'discount_percent']
    ordering_fields = ['discount_percent']
    ordering = ['discount_percent']
    permission_classes = [IsAdminOrManager]  # Admin or Manager can manage promotions
