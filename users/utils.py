import datetime
import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail

def generate_access_token(user):

    access_token_payload = {
        'user': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, minutes=5),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'uid': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token

@api_view(['POST'])
@csrf_exempt
def refresh_token_view(request):
    from users.models import UserProfile
    
    refresh_token = request.data.get('refresh_token')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed(
            {"message":'Refresh token error, please try again.', 
            "statusCode": 106})
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            {"message":'expired refresh token, please login again.', 
            "statusCode": 106}
            )

    user = UserProfile.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')


    access_token = generate_access_token(user)
    return Response({'access_token': access_token})

def decrypt(token):
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return data["user"]

def encrypt(payload):
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token

def token_verify(token):
    try:
        id = decrypt(bytes(token, "utf-8"))
    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed("Token Error")
    except jwt.ExpiredSignatureError:
        raise Exception("Token Expired", status_code=403)
    return id

def smtp(subject,message, recepient):
    send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[recepient],fail_silently=False)
