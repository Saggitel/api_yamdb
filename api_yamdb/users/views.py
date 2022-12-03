from django.contrib.auth.tokens import default_token_generator

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, SignupSerializer, RegistrationSerializer

from .permissions import AdminPermission


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
