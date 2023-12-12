from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitlesViewSet, CategoriesViewSet, GenresVieewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitlesViewSet)
router_v1.register(r'categories', CategoriesViewSet)
router_v1.register(r'genres', GenresVieewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
