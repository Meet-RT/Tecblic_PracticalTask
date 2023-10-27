from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from test_app.models import Personal_Profile
from test_app.exception import UserNotExists, UserAlreadyExists
from test_app.permissions import Is_AdminUser, Is_Solution_ProviderUser, Is_Solution_SeekerUser
from test_app.serializer import UserRegistrationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, UserProfileSerializer
from test_app.utils import generate_otp, send_email_otp,send_forgot_password_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


User = get_user_model()

class UserRegistration_APIView(APIView):
    """UserRegistration in system. """
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'User registered successfully in system.'},status=status.HTTP_200_OK,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""Logic for login in system with OTP verification"""
class Login_APIView(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_email_otp(email, otp)

        return Response({'msg': 'Please check your email for OTP'}, status=status.HTTP_200_OK)

"""OTP verification in system"""
class OTP_ValidationAPIView(APIView):
    
    def post(self, request):
        user_email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == str(otp):
            user.otp = None
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'username':user.username,'access_token': str(refresh.access_token),'refresh_token': str(refresh),},status=status.HTTP_200_OK,)
        else:
            return Response({'msg': 'Your OTP is invalid please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [Is_AdminUser| Is_Solution_ProviderUser| Is_Solution_SeekerUser | IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = Personal_Profile.objects.all()
    model = Personal_Profile
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    """create user profile"""
    def perform_create(self, serializer):
        if Personal_Profile.objects.filter(user=self.request.user):
            raise UserAlreadyExists('User profile already exist,')
        serializer.save(user=self.request.user)

    """update user profile data"""
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            raise UserNotExists('Requested user profile is not found.')


class ResetPassword_APIView(APIView):
    permission_classes = [Is_AdminUser| Is_Solution_ProviderUser| Is_Solution_SeekerUser,]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            if not user.check_password(current_password):
                return Response({'msg': 'Current Password is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(new_password) == user.check_password(current_password):
                return Response({'msg': 'Current password and New password are same please enter different password or try login with Current password you entered.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if new_password != confirm_password:
                return Response({'msg': 'Please enter same New password and Confirm Password.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'msg': 'Password changed successfully in system.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword_APIView(APIView):
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return Response({'msg': 'User with this email address does not exists.'}, status=status.HTTP_404_NOT_FOUND)
            
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                reset_link = f'http://127.0.0.1:5000/reset-password/{uid}/{token}/'
                send_forgot_password_email(reset_link,user_email)

                return Response({'msg': 'Please check your email for reset password link.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



