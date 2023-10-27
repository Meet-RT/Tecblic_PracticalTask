from django.urls import path,include
from .views import UserRegistration_APIView, Login_APIView, OTP_ValidationAPIView, ResetPassword_APIView, ForgotPassword_APIView, UserProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'user_profile', UserProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('user_registration/', UserRegistration_APIView.as_view(), name='user_registration'),
    path('email_otp/', Login_APIView.as_view(), name='email_otp'),
    path('otp_validation/', OTP_ValidationAPIView.as_view(), name='otp_validation'),
    path('reset_password/', ResetPassword_APIView.as_view(), name='reset_password'),
    path('forgot_password/', ForgotPassword_APIView.as_view(), name='forgot_password'),
    
]