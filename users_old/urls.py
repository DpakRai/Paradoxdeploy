from django.urls import path, include, re_path
from rest_framework import routers
from users.views import Activation, ChangePassword, GetHashedID, Login, Register, ResetPassword, ResetPasswordVerify, ReviewView, SetNewPassword, SocialLogin, payment_intent, test_subduration, user_subscription

router = routers.DefaultRouter()

router.register('review',ReviewView)

urlpatterns = [
    path('', include(router.urls)),
    path('test/',test_subduration,name='email_login'),
    path('login/',Login.as_view(),name='user_login'),
    path('register/',Register.as_view(),name='user_register'),
    path('social_login/',SocialLogin,name='social_login'),
    path('subscribe/',user_subscription,name='user_subscription'),
    path('payment_intent/',payment_intent,name='payment_intent'),
    path('activate/<str:token>',Activation),
    path('reset_password/',ResetPassword.as_view(),name='reset_password'),
    path('reset_password_verify/<str:token>',ResetPasswordVerify),
    path('change_password/',ChangePassword.as_view(),name='change_password'),
    path('forgot_password/',SetNewPassword.as_view(),name='forgot_password'),
    path('get_hashed_id/',GetHashedID.as_view(),name='get_hashed_id'),

]