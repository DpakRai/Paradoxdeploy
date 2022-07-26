from rest_framework import serializers
from ecommerce.models import Order, Product

from users.api.serializers import UserSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
