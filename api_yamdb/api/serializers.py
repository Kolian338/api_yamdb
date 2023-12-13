import re

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.utils import send_code_to_email
from reviews.models import User


class TitlesSerializer(serializers.ModelSerializer):
    pass


class CategoriesSerializer(serializers.ModelSerializer):
    pass


class GenresSerializer(serializers.ModelSerializer):
    pass


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == 'me':
            return serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!'
            )
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            return serializers.ValidationError(
                f'Не соответствует паттерну {pattern}'
            )

        return value

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if not User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError('Нет такого юзера')

        send_code_to_email(
            User.objects.get(username=username, email=email).password,
            list(email)
        )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(source='password')

    class Meta:
        model = User
        fields = ('username', 'confirmation_code',)
