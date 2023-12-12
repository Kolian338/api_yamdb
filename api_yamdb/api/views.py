from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import SignupSerializer
from api.utils import send_mail, send_code_to_email
from reviews.models import User


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
