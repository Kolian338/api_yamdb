import random

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.utils import send_code_to_email, get_tokens_for_user
from reviews.models import User, CHOICES


class TitlesSerializer(serializers.ModelSerializer):
    pass


class CategoriesSerializer(serializers.ModelSerializer):
    pass


class GenresSerializer(serializers.ModelSerializer):
    pass


class SignupSerializer(serializers.Serializer):
    """
    Сериализатор для создания юзера и отправки кода подтверждения.
    """

    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]+$")
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!'
            )

        return value

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(username=username, email=email).exists():
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такая почта уже используется'
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Такой username уже используется')

        return data

    def create(self, validated_data):
        """
        Создает экземпляр юзера если он не создан. Отправляет код на почту.
        """
        username = validated_data.get('username')
        email = validated_data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.get(username=username, email=email)
            send_code_to_email(user.password, email)
            return user

        validated_data['password'] = random.randint(0000, 9999)
        user = User.objects.create(**validated_data)
        send_code_to_email(user.password, email)
        return user


class TokenSerializer(serializers.Serializer):
    """
    Сериализатор для полуения JWT токена по коду подтверждения.
    """
    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]+$")
    confirmation_code = serializers.CharField(
        source='password', write_only=True
    )

    def get_token(self, validated_data):
        user = self.get_user(validated_data.get('username'))
        token = get_tokens_for_user(user)
        return token

    def get_user(self, username):
        return get_object_or_404(User, username=username)

    def to_representation(self, value):
        return {
            'token': self.get_token(value).get('access')
        }

    def validate(self, data):
        """
        Если переданный код(пароль) неверный выбрасывается ошибка валидации.
        """
        username = data.get('username')

        if data.get('password') != self.get_user(username).password:
            raise serializers.ValidationError('Не верный код!')
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей.
    """

    username = serializers.RegexField(max_length=150, regex=r"^[\w.@+-]+$")

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('password',)
