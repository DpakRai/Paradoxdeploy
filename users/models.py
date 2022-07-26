from datetime import datetime, timedelta, timezone
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import get_object_or_404
from users.utils import encrypt, smtp


from . import manager as user_manager


class SubscriptionType(Enum):
    community = 1
    professional = 2
    business = 3


class Subscription(models.Model):
    type = models.IntegerField(
        choices=((_.value, _.name) for _ in SubscriptionType), default=1
    )
    duration_day = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:

        return SubscriptionType(self.type).name


class UserProfile(AbstractUser):
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    objects = user_manager.UserProfileManager()

    subscription = models.ForeignKey(
        Subscription,
        related_name="user_subscription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    subscribed_date = models.DateTimeField(null=True, blank=True)
    age = models.IntegerField(
        validators=[MinValueValidator(5), MaxValueValidator(60)],
        null=True,
        blank=True,
    )
    address = models.TextField(max_length=30, null=True, blank=True)
    avatar = models.FileField(null=True, blank=True,upload_to='avatar/')
    name = models.TextField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    related_admin = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="related_users",
    )

    def __str__(self):
        if self.email:
            return self.email
        else:
            return self.username

    @property
    def subscription_remaining(self):

        subscription_duration = timedelta(days=self.subscription.duration_day)
        if subscription_duration == 99999:
            return "Unlimited"
        time_remaining = (subscription_duration + self.subscribed_date) - datetime.now(
            timezone.utc
        )
        return time_remaining

    def subscribe(self, sub):
        self.subscription = get_object_or_404(
            Subscription, type=SubscriptionType[sub].value
        )
        self.subscribed_date = datetime.now(timezone.utc)
        self.save()

    def send_reset_password_email(self, request):

        token = encrypt(
            {
                "user": self.id,
                "exp": datetime.utcnow() + timedelta(days=7),
                "iat": datetime.utcnow(),
            }
        )
        domain = request.META['HTTP_HOST']
        smtp(
            subject="Password reset",
            message=f"Please click here to reset your account password {domain}/users/reset_password_verify/{token}",
            recepient=self.email,
        )

    def send_confirmation_email(self, request):

        token = encrypt(
            {
                "user": self.id,
                "exp": datetime.utcnow() + timedelta(days=7),
                "iat": datetime.utcnow(),
            }
        )
        domain = request.META['HTTP_HOST']
        smtp(
            subject="Account activation",
            message=f"Please click here to activate your account {domain}/users/activate/{token}",
            recepient=self.email,
        )

    @property
    def hashed_id(self):
        hashed_id = encrypt({"user": self.id})
        return hashed_id


class Review(models.Model):
    title = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class UserActivity(models.Model):
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_activity",
    )
    device = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.created_at)
