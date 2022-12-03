from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from .send_email import send_code


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username',)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)

    def create(self, validated_data):

        return User.objects.get_or_create(
            email=validated_data['email'],
            username=validated_data['username'],
        )


class RegistrationSerializer(serializers.Serializer):
    username = serializers.SlugField()
    email = serializers.EmailField()

    def save(self):
        user = get_object_or_404(
            User, username=self.validated_data['username'])
        send_code(self.validated_data['email'],
                  default_token_generator.make_token(user))


class SignupSerializer(serializers.Serializer):
    username = serializers.SlugField()
    confirmation_code = serializers.CharField()

    # class Meta:
    #     fields = ('username', 'confirmation_code',)

    def save(self):
        user = get_object_or_404(
            User, username=self.validated_data['username'])
        confirmation_code = self.validated_data['confirmation_code']
        print(confirmation_code)
        if default_token_generator.check_token(user, confirmation_code):
            return {'token': str(AccessToken.for_user(user))}
