from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from reviews.models import Category, Genre, Title
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdminOrReadOnly

from .serializers import (
    CategorySerializer, GenreSerializer, TitleGETSerializer, TitleSerializer

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
    filter_backends = (SearchFilter,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
