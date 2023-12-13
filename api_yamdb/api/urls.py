from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (SignupAPIView, TitlesViewSet, CategoriesViewSet,
                       GenresVieewSet, TokenAPIView, UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'titles', TitlesViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresVieewSet)
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignupAPIView.as_view()),
    path('v1/auth/token/', TokenAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
