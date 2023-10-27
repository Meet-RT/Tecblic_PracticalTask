from rest_framework import serializers
from test_app.models import Personal_Profile
from django.contrib.auth import get_user_model

User = get_user_model()

"""User Registration serializer"""
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,write_only=True)
    first_name = serializers.CharField(max_length=200,required=True,allow_blank=False, allow_null=False)
    middle_name = serializers.CharField(max_length=200,required=False,allow_blank=True, allow_null=True)
    last_name = serializers.CharField(max_length=200,required=True,allow_blank=False, allow_null=False)
    role = serializers.CharField(max_length=200,required=True,allow_blank=False, allow_null=False)
    email = serializers.EmailField(max_length=200,required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'middle_name', 'last_name', 'role', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user
    
"""User Profile Details serializer"""
class UserProfileSerializer(serializers.ModelSerializer):
    user_bio = serializers.CharField(required=False,allow_null=True)
    mobile_number = serializers.CharField(required=False,allow_null=True)
    profile_photo = serializers.ImageField(required=False,allow_null=True)

    class Meta:
        model = Personal_Profile
        fields = ('id', 'user_bio', 'mobile_number', 'profile_photo',)
        
"""Change password serializer"""
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=200,required=True)
    new_password = serializers.CharField(max_length=200,required=True)
    confirm_password = serializers.CharField(max_length=200,required=True)
    
    class Meta:
        fields = ('old_password','new_password','confirm_password')

"""Forgot password serializer"""
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    class Meta:
        fields = ('email')

