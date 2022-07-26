from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from . import models as models


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = models.UserProfile
        fields = ('email','username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.UserProfile
        fields = ('email','username')
