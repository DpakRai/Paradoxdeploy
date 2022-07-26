from rest_framework.test import APIClient
from django.urls import reverse
from extensions.models import Extension

from users.utils import generate_access_token
from users.models import UserProfile, Review
import pytest



@pytest.fixture
def user(db):
    return UserProfile.objects.create(username="test",email="test@email.com")
    

@pytest.fixture
def api_client(user):
    access_token = generate_access_token(user)
    client = APIClient(HTTP_AUTHORIZATION='Token {}'.format(access_token))
    return client

@pytest.fixture
def review(db,user):
    return Review.objects.create(title="Test Review", user=user, rating=5)

@pytest.fixture
def extension(db,user, review):
    instance = Extension.objects.create(id=1, title="Test Extension",user=user, download=10)
    instance.reviews.add(review)
    instance.save()
    return instance

@pytest.mark.django_db
def test_get_extension_list(api_client, extension):

    response = api_client.get("/extensions/"
    )
    assert response.status_code == 200
    assert response.data["count"] == 1
    
@pytest.mark.django_db
def test_get_extension_detail(api_client, extension,user):
    response = api_client.get("/extensions/1/")
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["title"] == extension.title
    assert response.data["average_rating"] == response.data["average_rating"]
    assert response.data["download"] == extension.download


@pytest.mark.django_db
def test_create_extension(api_client, db, user, review):
    response = api_client.post(
        "/extensions/",
        {"title": "Test Extension", "average_rating": "5", "download": 10, "user":user.email, "reviews":review.id},
    )
    assert response.status_code == 201
    assert response.data["user"] == 1
    assert response.data["title"] == "Test Extension"
    assert response.data["average_rating"] == 5
    assert response.data["download"] == 10

@pytest.mark.django_db
def test_delete_extention(api_client, extension):
    response = api_client.delete("/extensions/1/")
    assert response.status_code == 204