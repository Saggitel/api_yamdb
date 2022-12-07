from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Category, Genre, Review, Title
from users.models import ADMIN, User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (AdminPermission, IsAdminOrReadOnly,
                          IsUserAdminModeratorOrReadOnly)
from .send_email import send_code
from .serializers import (CategorySerializer, CommentSerializer,
                          CreateTokenSerializer, GenreSerializer,
                          ReviewSerializer, TitleGETSerializer,
                          TitleSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    permission_classes = (AdminPermission,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class GetPatchUserViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        print('!!!', AdminPermission)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            if request.user.role != ADMIN:
                user = serializer.save(role=request.user.role)
            else:
                user = serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.data.get('username'),
            email=serializer.data.get('email')
        )
        confirmation_code = default_token_generator.make_token(user)
        send_code(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsUserAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsUserAdminModeratorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(
            author=self.request.user,
            review=review
        )
