import re

from rest_framework import serializers

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
        max_length=150,
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
 