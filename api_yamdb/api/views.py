import datetime as dt
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
from rest_framework import status, viewsets, mixins, filters, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (TitlesSerializer,
                             CategoriesSerializer,
                             GenresSerializer,
                             SignupSerializer,
                             ReviewSerializer,
                             CommentSerializer)
from api.utils import send_code_to_email
from reviews.models import (Titles,
                            Categories,
                            Genres,
                            User,
                            Reviews)
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
            email = serializer.validated_data.get('email')
            code = get_object_or_404(
                User, username=serializer.validated_data.get('username'),
                email=email
            ).password
            send_code_to_email(code, list(email))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestroyUpdateMixin:
    allowed_roles = ['moderator', 'admin']

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user or (
            self.request.user.role not in self.allowed_roles
        ):
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(serializer)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user or (
            self.request.user.role not in self.allowed_roles
        ):
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)


class ReviewViewSet(DestroyUpdateMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            pub_date=dt.datetime.now(),
            title=self.get_title()
        )


class CommentViewSet(DestroyUpdateMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            pub_date=dt.datetime.now(),
            review=self.get_review()
        )
