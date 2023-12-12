from django.shortcuts import render
from rest_framework import viewsets

from .serializers import (TitlesSerializer,
                          CategoriesSerializer,
                          GenresSerializer)
from reviews.models import (Titles,
                            Categories,
                            Genres)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()


class GenresVieewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()