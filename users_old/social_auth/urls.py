from django.urls import path, include

from users.social_auth.social_auth import GithubLogin

urlpatterns = [
    path('social/github/',GithubLogin,name='github_login '),
    
]