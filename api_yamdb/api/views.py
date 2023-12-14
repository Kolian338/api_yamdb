from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (TitlesSerializer,
                             CategoriesSerializer,
                             GenresSerializer,
                             SignupSerializer,
                             TokenSerializer, UserSerializer,
                             )
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAdminOrReadOnly,)

    @action(
        methods=['get', 'patch'], detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        """Создает маршрут /me и действие для него."""
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(role=serializer.instance.role)
                return Response(
                    serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
