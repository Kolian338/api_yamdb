import random
import datetime
import statistics

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.utils import send_code_to_email, get_tokens_for_user
from reviews.models import (User,
                            Review,
                            Comment,
                            Categories,
                            Genres,
                            Titles)


class AuthorMixin(metaclass=serializers.SerializerMetaclass):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    raiting = serializers.SerializerMethodField(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Titles
        fields = ('id',
                  'name',
                  'year',
                  'raiting',
                  'description',
                  'genre',
                  'category')

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Год выпуска произведения должен'
                                              ' быть не больше текущего года')
        return value

    def get_raiting(self, obj):
        list_raiting = obj.reviews.all().values_list('score', flat=True)
        try:
            raiting = statistics.mean(list_raiting)
        except statistics.StatisticsError:
            return 0
        return round(raiting, 0)


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

    def validate(self, data):
        """
        Если переданный код(пароль) неверный выбрасывается ошибка валидации.
        """
        username = data.get('username')

        if data.get('password') != self.get_user(username).password:
            raise serializers.ValidationError('Не верный код!')
        return data

    def to_representation(self, value):
        return {
            'token': self.get_token(value).get('access')
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователей.
    """

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('password',)


class ReviewSerializer(AuthorMixin, serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date', 'title',
        )
        model = Review
        read_only_fields = ('pub_date', 'id', 'title',)
    
    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Repeated reviews are not allowed'
            )
        return data

    def validate_score(self, value):
        if 0 > value > 10:
            return serializers.ValidationError(
                'Enter number between 0 and 10.'
            )
        return value


class CommentSerializer(AuthorMixin, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'pub_date', 'id')
