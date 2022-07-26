from itertools import product
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from ecommerce.models import Cart, CartItem, Order, Product
from ecommerce.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework import serializers
from users.models import UserProfile
from users.views import create_payment_intent
from drf_yasg.utils import swagger_auto_schema


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(APIView):
    class OutSerializer(serializers.Serializer):
        product = ProductSerializer(many=False)
        quantity = serializers.IntegerField()

    def get(self, request):
        data = request.GET
        """Get cart"""
        user=get_object_or_404(UserProfile, username=data.get("user"))
        try:
            cart = Cart.objects.get(user=user,active=True)
            return Response(
            {
                "cart_id": cart.id,
                "products": self.OutSerializer(cart.cartitem_set.all(), many=True).data,
                "total_price": cart.total_price,
            }
        )
        except Cart.DoesNotExist:
            return Response({"detail": "No active cart"},status=400)
        
    # @swagger_auto_schema(
    #     query_serializer=OutSerializer,
    #     responses={200: "access token, refresh_token"},
    # )
    def post(self, request):
        data = request.data
        """Get list of products with quantity and create cart with cartitems"""
        products = data.get("products")
        cart = Cart.objects.create(
            user=get_object_or_404(UserProfile, username=data.get("user"))
        )

        for product in list(products):
            CartItem.objects.create(
                cart=cart,
                product=get_object_or_404(Product, id=product.get("product")),
                quantity=product.get("quantity"),
            )
        return Response("Success")

    def put(self, request):
        data = request.data
        """Update cart """

        cart = get_object_or_404(
            Cart,
            id=data.get("cart_id"),
            user=get_object_or_404(UserProfile, username=data.get("user")),
        )
        # Delete all related cartitems
        cart.cartitem_set.all().delete()

        for product in list(data.get("products")):
            CartItem.objects.create(
                cart=cart,
                product=get_object_or_404(Product, id=product.get("product")),
                quantity=product.get("quantity"),
            )
        return Response("Success")

    def delete(self, request):
        data = request.data
        """Delete cart"""
        cart = get_object_or_404(
            Cart,
            id=data.get("cart"),
            user=get_object_or_404(UserProfile, username=data.get("user")),
        )
        cart.delete()
        return Response("Success")


class OrderView(APIView):
    class OutSerializer(serializers.Serializer):
        product = ProductSerializer(many=False)
        quantity = serializers.IntegerField()

    def get(self, request):
        data = request.data
        order_id = data.get("order_id")
        """Get order"""
        if order_id:
            order = get_object_or_404(
                Order,
                id=order_id,
                user=get_object_or_404(UserProfile, username=data.get("user")),
            )
            return Response(
                {
                    "order": order.id,
                    "total_price": order.cart.total_price,
                    "products": self.OutSerializer(
                        order.cart.cartitem_set.all(), many=True
                    ).data,
                }
            )
        else:
            order_response_list = []
            orders = get_list_or_404(
                Order,
                user=get_object_or_404(UserProfile, username=data.get("user")),
            )
            for order in orders:
                order_response_list.append(
                    {
                        "order_id": order.id,
                        "total_price": order.cart.total_price,
                        "complete": order.complete,
                        "products": self.OutSerializer(
                            order.cart.cartitem_set.all(), many=True
                        ).data,
                    }
                )
            return Response(order_response_list)

    def post(self, request):
        """Get cart and create order"""
        data = request.data
        user = get_object_or_404(UserProfile, username=data.get("user"))
        cart = get_object_or_404(Cart, id=data.get("cart_id"), user=user)
        Order.objects.create(cart=cart, user=user)
        cart.active = False
        cart.save()
        intent = create_payment_intent(cart.total_price)
        return Response(
            {"message": "payment intent created", "secret": intent.client_secret}
        )

    def put(self, request):
        """Update order"""
        data = request.data
        order = get_object_or_404(
            Order,
            id=data.get("order_id"),
            user=get_object_or_404(UserProfile, username=data.get("user")),
        )
        order.canceled = True
        order.save()
        return Response("Success")

    def delete(self, request):
        data = request.data
        """Delete order"""
        order = get_object_or_404(
            Order,
            id=data.get("order_id"),
            user=get_object_or_404(UserProfile, username=data.get("user")),
        )
        order.delete()
        return Response("Success")
