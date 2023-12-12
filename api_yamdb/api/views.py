from django.shortcuts import render
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (TitlesSerializer,
                          CategoriesSerializer,
                          GenresSerializer)
from reviews.models import (Titles,
                            Categories,
                            Genres)
from .permissions import IsAdminOrReadOnly


class BaseViewSetFromGenresCategories(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class CategoriesViewSet(BaseViewSetFromGenresCategories):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresVieewSet(BaseViewSetFromGenresCategories):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
