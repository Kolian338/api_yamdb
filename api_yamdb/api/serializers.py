import re

from rest_framework import serializers

from reviews.models import User, Reviews, Comments


class AuthorMixin(metaclass=serializers.SerializerMetaclass):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )


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


class ReviewSerializer(AuthorMixin, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ('title', 'pub_date', 'id')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('title', 'user')
            )
        ]

    def validate_score(self, value):
        if 0 > value > 10:
            return serializers.ValidationError(
                'Enter number between 0 and 10.'
            )
        return value


class CommentSerializer(AuthorMixin, serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review', 'pub_date', 'id')
