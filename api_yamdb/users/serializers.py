from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from .send_email import send_code


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('недопустимое имя пользователя')
        return value

    # def validate(self, data):
    #     if (
    #         User.objects.filter(email=data.get('email')).exists()
    #         or User.objects.filter(username=data.get('username')).exists()
    #     ):
    #         raise serializers.ValidationError('Такой email уже существует')


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        user = get_object_or_404(
            User, username=self.validated_data['username'])
        confirmation_code = self.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            return str(AccessToken.for_user(user))
