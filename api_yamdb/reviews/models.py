from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


class User(AbstractUser):
    email = models.EmailField('Почта', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль',
        max_length=20, choices=CHOICES, default=CHOICES[2][0]
    )

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 related_name='titles_category',
                                 null=True,
                                 blank=True)

    genre = models.ManyToManyField(Genre, through='GenreTitles')

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='repeated_review'
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
