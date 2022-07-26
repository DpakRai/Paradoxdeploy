from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
import jwt
from Appstore.decorator import check_token
from users.api.serializers import (
    ResetPasswordSerializer,
    ReviewSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from users.models import Review, Subscription, SubscriptionType, UserProfile
from users.utils import generate_access_token, generate_refresh_token, token_verify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

def test_subduration(request):
    if request.method == "GET":
        user = UserProfile(
            username="admin",
            email="admin@admin.com",
            is_staff="True",
            is_superuser="True",
            is_active="True",
        )
        user.set_password("root")
        user.save()
        UserProfile.objects.create(
            username="admin",
            email="admin@admin.com",
            password="root",
            is_staff="True",
            is_superuser="True",
            is_active="True",
        )
        print(UserProfile.objects.all())
        return HttpResponse("success")


def create_payment_intent(price, meta_data=None):
    import stripe

    stripe.api_key = "sk_test_51KTMNcSJ7XYjnhJesJFzKbx7t16uAhjIq9xPOCyRxy7u0ZppNYWwx4ah8H3YzfQoMKKm8K1SkhQwQZyrErYlvLjG003I5HezGI"
    return stripe.PaymentIntent.create(
        amount=int(price * 10),
        currency="usd",
        payment_method_types=["card"],
        metadata=meta_data,
    )


def confirm_payment(id):
    import stripe

    stripe.api_key = "sk_test_51KTMNcSJ7XYjnhJesJFzKbx7t16uAhjIq9xPOCyRxy7u0ZppNYWwx4ah8H3YzfQoMKKm8K1SkhQwQZyrErYlvLjG003I5HezGI"
    intent = stripe.PaymentIntent.retrieve(id)
    status = intent.get("status")
    if status != "succeeded":
        raise Exception("Payment Incomplete")
    return intent


class Login(APIView):
    @swagger_auto_schema(
        query_serializer=UserSerializer,
        responses={200: "access token, refresh_token"},
    )
    def post(self, request, *args, **kwargs):
        '''
        Login user by providing email and password
        '''
        email = request.data.get("email")
        password = request.data.get("password")
        response = Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")

        user = UserProfile.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return response


class Register(APIView):
    
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        query_serializer=UserRegisterSerializer,
        responses={200: "User successfully created"},
    )
    def post(self, request, *args, **kwargs):

        # Check if user is affliated with any admin
        if request.headers.get('Admin') and request.data.get("is_admin") is None:

            token=request.headers['Admin']
            data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            admin = UserProfile.objects.filter(id=data.get("user")).first()
            if admin is None:
                raise exceptions.AuthenticationFailed("Admin not found")
            if not admin.is_admin:
                raise exceptions.AuthenticationFailed("Admin not found")

        data = request.data
        email = request.data.get("email")
        username = request.data.get("username")

        if UserProfile.objects.filter(email=email).first():
            raise exceptions.NotAcceptable("Email already in use.")

        if UserProfile.objects.filter(username=username).first():
            raise exceptions.NotAcceptable("Username already in use.")

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):

            instance = serializer.save()
            instance.set_password(request.data.get("password"))
            instance.is_active = False
            try:
                instance.related_admin = admin
            except UnboundLocalError:
                pass
            instance.save()
            try:
                user = UserProfile.objects.get(id=instance.id)
            except UserProfile.DoesNotExist:
                return Response({"message": "User not found"}, status=404)

            user.send_confirmation_email()
            return Response({"User successfully created"})
        else:
            raise exceptions.ValidationError("User validation Error")


def SocialLogin(request):
    response = Response()

    access_token = generate_access_token(request.user)
    refresh_token = generate_refresh_token(request.user)

    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    response.data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    # return response
    return JsonResponse(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


def Activation(request, token):
    id = token_verify(token)
    user = UserProfile.objects.get(id=id)
    if user:
        user.is_active = True
        user.save()
        return True
    return HttpResponse("Activation Successful")


class ResetPassword(APIView):

    @swagger_auto_schema(
        responses={200: "Reset Password Email Sent"},
    )
    @check_token
    def post(self, request, *args, **kwargs):
        user = request.user
        user.send_reset_password_email()
        return Response({"message": "Reset Password Email Sent"})


def ResetPasswordVerify(request, token):
    token_verify(token)
    return HttpResponse("Token Verified")


class SetNewPassword(APIView):
    @check_token
    def post(self, request, *args, **kwargs):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if new_password != confirm_password:
            raise exceptions.AuthenticationFailed("Password not matched")
        user = request.user
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password saved successfully"})


class ChangePassword(APIView):
    @swagger_auto_schema(
        query_serializer=ResetPasswordSerializer,
        responses={200: "Password changed successfully"},
    )
    @check_token
    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if new_password != confirm_password:
            raise exceptions.AuthenticationFailed("Password not matched")
        user = request.user
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Wrong Password")
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"})


# @csrf_exempt
# def create_user_using_firestore_uid(request):
#     if request.method == "POST":
#         uid=request.POST.get("uid")
#         user = auth.get_user(uid)

#         user_instance,created = UserProfile.objects.get_or_create(email=user.email,username=user.uid)
#         if created:
#             user.is_active=not user.disabled,
#             user_instance.set_password("defaultpassword")
#             user_instance.save()

#             profile = Profile(
#             user=user_instance,
#             name=user.display_name,
#             avatar=user.photo_url,)

#             profile.save()
#             return HttpResponse("{} profile created.".format(Profile))
#         else:
#             return HttpResponse("{} user exists.".format(user_instance))

# def user_subscription(request):
#     if request.method == "POST":
#         uid=request.POST.get("uid")
#         profile = Profile.objects.get(user=UserProfile.objects.get(username=uid))
#         profile.subscribe('premium')
#         return HttpResponse("{} subscription created.".format(profile))


@api_view(["POST"])
def payment_intent(request):

    subscription = request.POST.get("subscription")
    if subscription:
        if subscription == "community":
            pass
        subscription_obj = get_object_or_404(
            Subscription, type=SubscriptionType[subscription].value
        )
        intent = create_payment_intent(
            subscription_obj.price, {"subscription": subscription}
        )
        return Response(
            {"message": "payment intent created", "secret": intent.client_secret}
        )
    else:
        return HttpResponseBadRequest("subscription required")


@api_view(["POST"])
def user_subscription(request):
    if request.method == "POST":
        uid = request.POST.get("uid")
        secret = request.POST.get("id")
        intent = confirm_payment(secret)
        metadata = intent.get("metadata")
        if metadata:
            profile = get_object_or_404(UserProfile, username=uid)
            profile.subscribe(metadata.get("subscription"))
            return HttpResponse("{} subscription created.".format(profile))


# # The url where the google oauth should redirect
# # after a successful login.
# REDIRECT_URI = 'https://localhost:8000/users/google/callback/'
# # REDIRECT_URI = 'exp://192.168.1.73:19000'

# import os
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# # Authorization scopes required
# SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', "openid"]

# JSON_FILEPATH = os.path.join(os.getcwd(), 'google_auth.json')

# def RedirectGoogleSignin(request):
#     oauth_url = google_apis_oauth.get_authorization_url(
#         JSON_FILEPATH, SCOPES, REDIRECT_URI)
#     return HttpResponseRedirect(oauth_url)

# def CallbackGoogleSignin(request):
#     try:
#         credentials = google_apis_oauth.get_crendentials_from_callback(
#             request,
#             JSON_FILEPATH,
#             SCOPES,
#             REDIRECT_URI
#         )
#         stringified_token = google_apis_oauth.stringify_credentials(
#             credentials)
#         stringified_token = json.loads(stringified_token)
#         response = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={stringified_token['token']}")
#         jsonData = response.json()
#         print(jsonData)
#         if jsonData['email']:
#             profileData = {
#                 "avatar": jsonData["picture"]
#             }
#             user, userExist = UserProfile.objects.get_or_create(email=jsonData["email"], username=str(jsonData["email"]).split("@")[0])
#             user.save()
#             profile, _ = Profile.objects.get_or_create(user=user)
#             profile.__dict__.update(profileData)
#             profile.save()
#             user.backend = settings.AUTH_PASSWORD_VALIDATORS[0]['NAME']
#             login(request, user)
#             access_token = generate_access_token(user)
#             refresh_token = generate_refresh_token(user)
#             return HttpResponse(f"access_token={access_token}&refresh_token={refresh_token}")
#         return HttpResponseBadRequest("Login Failed")
#     except google_apis_oauth.InvalidLoginException:
#         return HttpResponseBadRequest("Login Failed")


class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class GetHashedID(APIView):
    @check_token
    def get(self, request, *args, **kwargs):
        return Response({"hashed_id": request.user.hashed_id})