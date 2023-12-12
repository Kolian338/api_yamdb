from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitlesViewSet, CategoriesViewSet, GenresVieewSet


app_name = 'api'

routerv1 = DefaultRouter()
routerv1.register(r'titles', TitlesViewSet)
routerv1.register(r'categories', CategoriesViewSet)
routerv1.register(r'genres', GenresVieewSet)

urlpatterns = [
    path('v1/', include(routerv1.urls)),
]
