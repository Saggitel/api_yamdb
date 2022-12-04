from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title, Review, Comment
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    CategorySerializer, GenreSerializer, TitleGETSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__name', 'genre__name', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # добавить ограничение на кол-во постов
    permission_classes = [IsAuthenticatedOrReadOnly & IsAdminOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            # Не уверен насчет 'or self.request.user.is_admin'
            author=self.request.user or self.request.user.is_admin, title_id=self.kwargs.get('post_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAdminOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            # Не уверен насчет 'or self.request.user.is_admin'
            author=self.request.user or self.request.user.is_admin, review_id=self.kwargs.get('post_id')
        )


# class RatingViewSet(viewsets.ModelViewSet)