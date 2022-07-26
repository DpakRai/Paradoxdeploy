from functools import wraps
from django.contrib.auth import login
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
import jwt
from rest_framework.views import APIView
from users.models import UserProfile
from Appstore import settings
from jwt.exceptions import *
from rest_framework import request

def check_token(function):
    @wraps(function)
    def wrap(request:request, *args, **kwargs):
        try:
            if request.headers.get('Authorization') is None:
                request = args[0]
            token=request.headers['Authorization'].split(' ')[1]
            data=jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return HttpResponse('Token Expired, Please refetch access token',status=406)
        except InvalidSignatureError:
            return HttpResponseForbidden('Token Invalid')
        except IndexError:
            return HttpResponseBadRequest('Token Required')

        try:
            current_user=get_object_or_404(UserProfile,id=data['user'])
            login(request, current_user)
            request.user=current_user
            return function(request, user=current_user, *args, **kwargs)
        except ModuleNotFoundError:
            return HttpResponseForbidden('Token Invalid')
    return wrap

# def check_token(function):
#     @wraps(function)
#     def wrap(request:request, *args, **kwargs):
#         authorization = request.headers.get('Authorization')
#         if not authorization:
#             return HttpResponseForbidden("Access not allowed")
#         res=requests.get(settings.TOKEN_URL, headers={"Authorization":authorization})
#         try:
#             data=json.loads(res.text)
#             print(res.status_code)
#         except json.decoder.JSONDecodeError:
#             return HttpResponseForbidden("Access not allowed")
#         if data.get("detail")=="success":
#             return function(request, *args, **kwargs)
#         else:
#             return HttpResponseForbidden("Access not allowed")
#     return wrap