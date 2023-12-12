from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


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