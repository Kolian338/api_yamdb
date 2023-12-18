from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    SignupAPIView,
    TitlesViewSet,
    CategoriesViewSet,
    GenresViewSet,
    ReviewViewSet,
    CommentViewSet,
    TokenAPIView,
    UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(r'titles', TitlesViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresViewSet)
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignupAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
