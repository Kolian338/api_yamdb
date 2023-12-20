import random
import datetime

from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.utils import send_code_to_email, get_tokens_for_user
from reviews.models import (
    Review,
    Comment,
    Categories,
    Genre,
    Title
)
from users.models import User


class AuthorMixin(metaclass=serializers.SerializerMetaclass):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class BaseTilesSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if not isinstance(value, int):
            raise serializers.ValidationError('Проверьте формат года '
                                              'выпуска произведения')
        if value > current_year:
            raise serializers.ValidationError('Год выпуска произведения должен'
                                              ' быть не больше текущего года')
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError('Наименование произведения не '
                                              'должно превышать 256 символов')
        return value


class TitlesListSerializer(BaseTilesSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)


class TitlesSerializer(BaseTilesSerializer):
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(),
                                            slug_field='slug')

    def create(self, validated_data):
        genre_list = validated_data.pop('genre')
        title_obj = Title(**validated_data)
        title_obj.save()
        title_obj.genre.set(genre_list)
        return title_obj

    def update(self, instance, validated_data):
        category = validated_data.get('category', instance.category)
        ganres = validated_data.get('genre')
        name = validated_data.get('name', instance.name)
        year = validated_data.get('year', instance.year)
        description = validated_data.get('description', instance.description)
        instance.name = name
        instance.year = year
        instance.description = description
        instance.category = category
        instance.name = name
        instance.save()
        if ganres:
            instance.genre.set(ganres)
        return instance


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

        if User.objects.filter(
            Q(username=username) | Q(email=email)
        ).exists():
            raise serializers.ValidationError(
                'Такая почта или username уже используются'
            )

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
        Если переданный пароль неверный выбрасывается ошибка валидации.
        """
        username = data.get('username')

        if data.get('password') != self.get_user(username).password:
            raise serializers.ValidationError('Не верный пароль!')
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
        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Repeated reviews are not allowed'
            )
        return data


class CommentSerializer(AuthorMixin, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'pub_date', 'id')
