from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SignupAPIView

app_name = 'api'

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', SignupAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
]
