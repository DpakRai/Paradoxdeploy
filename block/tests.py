from rest_framework.test import APIClient
from django.urls import reverse
from block.models import Block

from users.models import UserProfile, Review
import pytest



@pytest.fixture
def user():
    return UserProfile.objects.create(username="test",email="test@email.com")


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client



@pytest.fixture
def reviews(user):
    review1 = Review.objects.create(user=user, title="Test Review 1")
    review2 = Review.objects.create(user=user, title="Test Review 2")
    review_list = [review1, review2]
    return review_list

@pytest.fixture
def block(user, reviews):
    instance = Block.objects.create(
        title="Test Block", 
        description_block="Test Description", 
        average_rating=5, 
        user=user
        )
    
    for review in reviews:
        instance.reviews.add(review)

    return instance


@pytest.mark.django_db
def test_get_block_list(api_client):
    response = api_client.get("/block/")
    assert response.status_code == 200
    
@pytest.mark.django_db
def test_get_block_detail(api_client,block,user):
    response = api_client.get("/block/1/")
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["title"] == block.title
    assert response.data["description_block"] == block.description_block
    assert response.data["average_rating"] == block.average_rating
    assert response.data["reviews"] == [review.id for review in block.reviews.all()]


@pytest.mark.django_db
def test_create_block(api_client,user, reviews):
    response = api_client.post(
        "/block/",
        {"title": "Test Block", "description_block": "Test Description", "average_rating": "5", "user":user.email, "reviews":reviews[0].id},
    )
    assert response.status_code == 201
    assert response.data["user"] == user.id
    assert response.data["title"] == "Test Block"
    assert response.data["description_block"] == "Test Description"
    assert response.data["average_rating"] == 5
    assert response.data["reviews"] == [reviews[0].id]

@pytest.mark.django_db
def test_delete_block(api_client,block):
    response = api_client.delete("/block/1/")
    assert response.status_code == 204