import django_filters
from reviews.models import Title


class GanreFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(name='genre__slug',
                                      lookup_type='exact')

    class Meta:
        model = Title
        fields = ('genre',)
