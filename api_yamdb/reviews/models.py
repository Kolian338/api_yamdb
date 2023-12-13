from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


class User(AbstractUser):
    email = models.EmailField('Почта', unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=20, choices=CHOICES, default=CHOICES[2][0]
    )


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    year = models.DateField()
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 related_name='titles_category',
                                 null=True,
                                 blank=True)
    genre = models.ForeignKey(Genres,
                              on_delete=models.SET_NULL,
                              related_name='titles_genre',
                              null=True,
                              blank=True)
    genre = models.ManyToManyField(Genres, through='GenreTitles')

    def __str__(self):
        return self.name


class GenreTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Reviews(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
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


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)

