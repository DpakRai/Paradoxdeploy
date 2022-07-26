from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
import pytest
from .models import Profile, Subscription, UserProfile

client = Client()


def test_login(db):
    user = UserProfile.objects.create(username="test")
    login_url = reverse("user_login")
    response = client.post(
        login_url,
        {
            "uid": user.username,
        },
    )
    assert response.status_code == 200

    response = client.post(login_url, {})
    assert response.status_code == 406

    response = client.post(
        login_url,
        {
            "uid": "RandomUID",
        },
    )
    assert response.status_code == 404


def test_subscription(db):
    user = UserProfile.objects.create(username="test")
    profile = Profile.objects.create(user=user)
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
