import datetime as dt

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import (
    IsAdminOrReadOnly, IsAdminOrSuperUser, IsAdminModeratorOrAuthenticatedUser
)
from api.serializers import (TitlesSerializer,
                             TitlesListSerializer,
                             CategoriesSerializer,
                             GenresSerializer,
                             SignupSerializer,
                             TokenSerializer,
                             UserSerializer,
                             ReviewSerializer,
                             CommentSerializer
                             )
from reviews.models import (Title,
                            Categories,
                            Genre,
                            User,
                            Review)
from api.filters import GanreFilter


class BaseViewSetFromGenresCategories(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GanreFilter
    filterset_fields = ('name', 'genre', 'year', 'category')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesListSerializer
        return super().get_serializer_class()


class CategoriesViewSet(BaseViewSetFromGenresCategories):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(BaseViewSetFromGenresCategories):
    queryset = Genre.objects.all()
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
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOrAuthenticatedUser,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            pub_date=dt.datetime.now(),
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOrAuthenticatedUser,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            pub_date=dt.datetime.now(),
            review=self.get_review()
        )
