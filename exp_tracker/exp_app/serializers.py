from rest_framework import serializers
from .models import CustomUser, Income
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'fullname', 'username', 'email', 'contact']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['fullname', 'username', 'email', 'contact', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['fullname'] = user.fullname
        token['email'] = user.email
        token['contact'] = user.contact
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user fields to the response
        data['user'] = {
            "id": self.user.id,
            "fullname": self.user.fullname,
            "username": self.user.username,
            "email": self.user.email,
            "contact": self.user.contact
        }

        return data


class IncomeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = Income
        fields = ['id', 'username', 'income_amount', 'date']
