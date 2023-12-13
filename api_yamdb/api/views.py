from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (TitlesSerializer,
                             CategoriesSerializer,
                             GenresSerializer,
                             SignupSerializer,
                             TokenSerializer,
                             )
from api.utils import send_code_to_email, get_tokens_for_user
from reviews.models import (Titles,
                            Categories,
                            Genres,
                            User)
from api.permissions import IsAdminOrReadOnly


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


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data.get('password')
            token = get_tokens_for_user(
                get_object_or_404(
                    User, username=serializer.validated_data.get('username'),
                    password=confirmation_code
                )
            )
            return Response({'token': token.get('access')},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
