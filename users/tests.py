from django.test.client import Client
from django.urls import reverse
import pytest
from .models import  Subscription, UserProfile

client = Client()


def test_login(db):
    user = UserProfile.objects.create_user(username="test", email='test@email.com', password='testing123')
    login_url = reverse("user_login")
    response = client.post(
        login_url,
        {
            "email": user.email,
            "password": "testing123"
        },
    )
    assert response.status_code == 200

    response = client.post(login_url, {})
    assert response.status_code == 403
    assert response.data.get('detail') == "email and password required"

    response = client.post(
        login_url,
        {
            "email": "RandomUID",
            "password": "RandomPassword"
        },
    )
    assert response.status_code == 403
    assert response.data.get('detail') == "user not found"


def test_subscription(db):
    user = UserProfile.objects.create(username="test")
    Subscription.objects.create(type=2, price=1000, duration_day=30)
    intent_url = reverse("payment_intent")
    response = client.post(
        intent_url,
        {
            "subscription": "professional",
        },
    )
    assert response.status_code == 200
    intent_id = response.data.get("secret")
    intent_id = str(intent_id).split("_secret_")[0]

    subscription_url = reverse("user_subscription")
    # response = client.post(
    #     subscription_url,{
    #         'uid':user.username,
    #         "id":intent_id,
    #         })
    with pytest.raises(Exception) as e:
        client.post(
                subscription_url,
                {
                    "uid": user.username,
                    "id": intent_id,
                },
            )
        assert str(e.value) == "Payment Incomplete"
