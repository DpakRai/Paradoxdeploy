from django.urls import path
from users.views import (
    Activation, ChangePassword, 
    Delete_Related_User, Get_Related_Users, 
    GetHashedID, Login, Register, ResetPassword, 
    ResetPasswordVerify, SetNewPassword, 
    SocialLogin, get_ip_address, get_user_activity, 
    payment_intent, test_subduration, user_subscription,
    ProfileView
)

urlpatterns = [
    path('test/',test_subduration,name='email_login'),
    path('login/',Login.as_view(),name='user_login'),
    path('register/',Register.as_view(),name='user_register'),
    path('social_login/',SocialLogin,name='social_login'),

    path('activate/<str:token>',Activation),
    path('reset_password/',ResetPassword.as_view(),name='reset_password'),
    path('reset_password_verify/<str:token>',ResetPasswordVerify),
    path('change_password/',ChangePassword.as_view(),name='change_password'),

    path('forgot_password/',SetNewPassword.as_view(),name='forgot_password'),
    path('get_hashed_id/',GetHashedID.as_view(),name='get_hashed_id'),
    path('subscribe/',user_subscription,name='user_subscription'),
    path('payment_intent/',payment_intent,name='payment_intent'),

    path('developer/',Get_Related_Users.as_view(),name='get_related_users'),
    path('profile/<str:username>/',ProfileView.as_view(),name='user_profile'),
    path('developer/<int:id>/',Delete_Related_User.as_view(),name='delete_related_users'),
    path('get_ip/',get_ip_address,name='get_ip'),
    path('get_user_activites/',get_user_activity,name='get_user_activites'),
]