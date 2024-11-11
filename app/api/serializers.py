# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Category, Product, Supplier, Customer, Order, Review, Shipping, Payment, Staff, Promotion

User = get_user_model()


# User Serializer for Authentication and Registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'rating', 'categories')


class SupplierSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Supplier
        fields = ('id', 'name', 'products')


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'phone')


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'products', 'order_date', 'total_amount')


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer()

    class Meta:
        model = Review
        fields = ('id', 'customer', 'product', 'rating', 'comment', 'review_date')


class ShippingSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Shipping
        fields = ('id', 'order', 'address', 'shipped_date')


class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = Payment
        fields = ('id', 'order', 'payment_date', 'amount')


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = ('id', 'user', 'phone')


class PromotionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Promotion
        fields = ('id', 'product', 'discount_percent', 'start_date', 'end_date')
