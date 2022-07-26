from datetime import date
from urllib import response
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
import pycountry
import requests
from Appstore.decorator import check_token
from users.api.serializers import (
    ResetPasswordSerializer,
    UserActivityReturnSerializer,
    UserRegisterSerializer,
    UserReturnSerializer,
    UserSerializer,
)
from users.models import (
    Subscription,
    SubscriptionType,
    UserActivity,
    UserProfile,
)
from users.utils import generate_access_token, generate_refresh_token, token_verify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import exceptions

from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from rest_framework import status


def login_activity(user, device):
    activity, created = UserActivity.objects.get_or_create(
        created_at=date.today(), user=user, device = device
    )
    activity.save()


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
        
        if not user.is_active:
            try:
                user.send_confirmation_email(request)
            except Exception as e:
                data = {
                    'message': "Email was not sent",
                    'error': str(e)
                }
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            return Response({
                'message': "Activate your account first. The confirmation email has been sent to your email."
            })

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
            instance.save()
            try:
                user = UserProfile.objects.get(id=instance.id)
            except UserProfile.DoesNotExist:
                return Response({"message": "User not found"}, status=404)

            try:
                user.send_confirmation_email(request)
            except Exception as e:
                data = {
                'message': 'Email was not sent',
                'error': str(e)
                }
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'User is successfully created'})
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
        return HttpResponse("Activation Successful")
    return HttpResponseBadRequest("User not found!")


class ResetPassword(APIView):
    @swagger_auto_schema(
        responses={200: "Reset Password Email Sent"},
    )
    @check_token
    def post(self, request, *args, **kwargs):
        user = request.user
        response = Response()
        try:
            user.send_reset_password_email()
        except Exception as e:
            data = {
                'message': 'Email was not sent',
                'error': str(e)
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message':"Reset Password Email Sent"})


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



class ProfileView(APIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserReturnSerializer

    def get(self, request, username, *args, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            serializer = UserReturnSerializer(user)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            data = {
                "message": "User does not exist"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(check_token, name="dispatch")
    def put(self, request, username, *args, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return Response({'message':'User does not exit'},status=status.HTTP_404_NOT_FOUND)  
        if user == request.user:
            serializer = UserReturnSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({'message':"You are not allowed to update other user's detail"}, status=status.HTTP_403_FORBIDDEN)


class GetHashedID(APIView):
    @check_token
    def get(self, request, *args, **kwargs):
        return Response({"hashed_id": request.user.hashed_id})


class Allow_Access(APIView):
    @check_token
    def get(self, request):
        return JsonResponse({"detail": "success"})


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
        secret = request.POST.get("secret")
        intent = confirm_payment(secret)
        metadata = intent.get("metadata")
        if metadata:
            profile = get_object_or_404(UserProfile, username=uid)
            profile.subscribe(metadata.get("subscription"))
            return HttpResponse("{} subscription created.".format(profile))


class Get_Related_Users(APIView):

    @method_decorator(check_token, name="dispatch")
    def get(self, request, id, *args, **kwargs):
        user = request.user
        related_users = user.related_users.all()
        serializer = UserReturnSerializer(related_users, many=True)
        return Response(serializer.data)

    @method_decorator(check_token, name="dispatch")
    def post(self, request, *args, **kwargs):
        admin_user = request.user

        email = request.data.get("email")
        username = request.data.get("username")
        if not email:
            return Response({"detail": "Email is required"}, status=400)
        if not username:
            return Response({"detail": "Username is required"}, status=400)
        UserProfile.objects.create(
            email=email, username=username, related_admin=admin_user
        )

        return Response({"detail": "success"})


class Delete_Related_User(APIView):
    @method_decorator(check_token, name="dispatch")
    def delete(self, request, *args, **kwargs):
        admin = request.user
        try:
            user = UserProfile.objects.get(id=kwargs["id"], related_admin=admin)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User does not exist"}, status=404)
        user.delete()
        return Response({"detail": "success"})


def get_country_name(ip_address):
    endpoint = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(endpoint, verify=True)

    if response.status_code != 200:
        return exceptions("Status:", response.status_code, "Problem with the request.")

    data = response.json()
    if data.get("country"):
        country = pycountry.countries.get(alpha_2=data["country"])

        return country.name


def get_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return HttpResponse(ip)


@check_token
def group_users_by_country(request, **kwargs):
    if request.method == "GET" and request.user.is_admin:
        countries = {}
        for user in UserProfile.objects.filter(related_admin=request.user):
            country = user.country

            if country:
                if country in list(countries.keys()):
                    countries[country] += 1
                else:
                    countries[country] = 1
        return countries


@check_token
def get_user_activity(request, **kwargs):
    if request.method == "GET":
        users = UserProfile.objects.filter(related_admin=request.user)
        activity = []
        for user in users:
            user_activity = user.user_activity.all()

            if user_activity:
                if activity:
                    activity + list(user.user_activity.all())
                else:
                    activity = list(user.user_activity.all())

        activity_qs = UserActivity.objects.filter(
            id__in=[object.id for object in activity]
        )

        # device_count = activity_qs.values("created_at").annotate(count=Count("created_at")).values("device").annotate(Count("device"))
        # print(device_count)
        results = UserActivityReturnSerializer(
            activity_qs.values("device","created_at").annotate(device_count=Count("device"),count=Count("created_at")),
            many=True
        ).data
        return JsonResponse(results, safe=False)
