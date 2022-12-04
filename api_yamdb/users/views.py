from django.contrib.auth.tokens import default_token_generator
from .models import ADMIN
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, CreateTokenSerializer, RegistrationSerializer
from .send_email import send_code
from .permissions import AdminPermission, OwnerOrAdminPermission


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    permission_classes = (OwnerOrAdminPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, created = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email')
        )
        if not (request.user.is_authenticated
            and (request.user.role == ADMIN
                 or request.user.is_superuser)):
            confirmation_code = default_token_generator.make_token(user)
            send_code(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
