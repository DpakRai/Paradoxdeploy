import django
django.setup()

from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token

from users.models import UserProfile
from .models import Cart, CartItem, Order, Product
import pytest


@pytest.fixture
def products():
    product1 = Product.objects.create(id=1, name="Test Product", price=900)
    product2 = Product.objects.create(id=2, name="Test Product 2", price=1000)
    product3 = Product.objects.create(id=3, name="Test Product 3", price=1500)
    return [product1, product2, product3]


@pytest.fixture
def user():
    return UserProfile.objects.create(username="test", email="test@email.com")


@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(products, cart):
    return CartItem.objects.create(product=products[0], cart=cart, quantity=1)


@pytest.fixture
def order(cart):
    return Order.objects.create(id=10, cart=cart, user=cart.user)


client = APIClient()


@pytest.mark.django_db
def test_get_product_list():
    response = client.get("/ecommerce/product/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_product_detail(products):
    response = client.get("/ecommerce/product/1/")
    assert response.status_code == 200
    assert response.data["name"] == "Test Product"
    assert response.data["price"] == "900.00"


@pytest.mark.django_db
def test_create_product(db):
    response = client.post(
        "/ecommerce/product/",
        {"name": "Test Product", "price": 1000},
        format="json",
    )
    assert response.status_code == 201
    assert response.data["name"] == "Test Product"
    assert response.data["price"] == "1000.00"


@pytest.mark.django_db
def test_delete_product(products):
    response = client.delete("/ecommerce/product/1/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_get_cart(user, cart):
    
    response = client.get(
        reverse('cart'),
        {'user': user.username}
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_cart(products, user):
    cart_url = reverse("cart")
    response = client.post(
        cart_url,
        {
            "user": user.username,
            "products": [{"product": products[0].id, "quantity": 1}],

        },
        format="json",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",

    )
    assert response.status_code == 200

    cart_item_obj = CartItem.objects.get(cart=1)
    assert cart_item_obj.product.id == products[0].id
    assert cart_item_obj.quantity == 1


@pytest.mark.django_db
def test_update_cart(cart, user, products):
    cart_url = reverse("cart")
    UserProfile.objects.create(username="test2", email="test2@email.com")
    response = client.put(
        cart_url,
        {
            "cart_id": cart.id,
            "user": "test",
            "products": [{"product": products[1].id, "quantity": 1}]
        },
        format="json",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    assert response.status_code == 200

    cart = Cart.objects.get(id=1)
    assert cart.cartitem_set.count() == 1
    assert cart.cartitem_set.first().product.id == products[1].id
    assert cart.cartitem_set.first().quantity == 1


@pytest.mark.django_db
def test_create_order(cart_item):
    order_url = reverse("order")
    response = client.post(
        order_url,
        {
            "user": "test",
            "cart_id": cart_item.cart.id,
        },
        format="json",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    assert response.status_code == 200

    order_obj = Order.objects.get(id=1)
    assert order_obj.get_cart_total == 900


@pytest.mark.django_db
def test_update_order(cart,order):
    order_url = reverse("order")
    response = client.put(
        order_url,
        {
            "user": cart.user.username,
            "order_id": order.id,
        },
        format="json",
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )
    order_obj=Order.objects.get(id=10)
    assert response.status_code == 200
    assert order_obj.canceled == True
