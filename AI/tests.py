from django.urls import reverse
from AI.models import BaseDevice
from rest_framework.test import APIClient


from users.models import UserProfile, Review
import pytest


@pytest.fixture
def user():
    return UserProfile.objects.create(
        username="test",
        email="test@email.com",
        )


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client

@pytest.fixture
def reviews(user):
    review1 = Review.objects.create(user=user, title="Test Review 1", rating=5)
    review2 = Review.objects.create(user=user, title="Test Review 2", rating=3)
    review_list = [review1, review2]
    return review_list


@pytest.fixture
def device(user, reviews):
    instance = BaseDevice.objects.create( 
        title="Test Device", 
        user=user,
        average_rating=5
        )
    for review in reviews:
        instance.reviews.add(review)

    instance.save()

    return instance



@pytest.mark.django_db
def test_get_device_list(api_client):
    response = api_client.get("/ai/")
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_device_detail(api_client, user, device):
    response = api_client.get("/ai/1/")
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["title"] == device.title
    assert response.data["average_rating"] == device.average_rating
    assert response.data["reviews"] == [review.id for review in device.reviews.all()]



@pytest.mark.django_db
def test_create_device(api_client, user, reviews):
    response = api_client.post(
        "/ai/",
        {"title": "Test Device", "average_rating": "5", "user":user.email, "reviews":reviews[0].id},
    )
    assert response.status_code == 201
    assert response.data["user"] == user.id
    assert response.data["title"] == "Test Device"
    assert response.data["average_rating"] == 5
    assert response.data["reviews"] == [reviews[0].id]


@pytest.mark.django_db
def test_delete_device(api_client, device):
    response = api_client.delete("/ai/1/")
    assert response.status_code == 204