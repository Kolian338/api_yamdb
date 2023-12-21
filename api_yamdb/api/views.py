import datetime as dt

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import status, viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import (
    IsAdmin, IsSuperUser,
    IsAuthenticatedUser, IsModerator, ReadOnly
)
from api.serializers import (TitlesSerializer,
                             TitlesListSerializer,
                             CategoriesSerializer,
                             GenresSerializer,
                             SignupSerializer,
                             TokenSerializer,
                             UserSerializer,
                             ReviewSerializer,
                             CommentSerializer)
from reviews.models import (Title,
                            Categories,
                            Genre,
                            Review)
from users.models import User
from api.filters import GanreFilter


class BaseViewSetFromGenresCategories(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      viewsets.GenericViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | ReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GanreFilter
    filterset_fields = ('name', 'genre', 'year', 'category')
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesListSerializer
        return TitlesSerializer

    def get_queryset(self):
        return (
            Title
            .objects
            .annotate(rating=Avg('reviews__score'))
            .order_by('id')
        )


class CategoriesViewSet(BaseViewSetFromGenresCategories):
    queryset = Categories.objects.order_by('id')
    serializer_class = CategoriesSerializer


class GenresViewSet(BaseViewSetFromGenresCategories):
    queryset = Genre.objects.order_by('id')
    serializer_class = GenresSerializer


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для пользователя.
    """

    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin | IsSuperUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get'], detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        """Создает маршрут /me"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(role=serializer.instance.role)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedUser | IsModerator | IsAdmin,)
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
    permission_classes = (IsAuthenticatedUser | IsModerator | IsAdmin,)
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
