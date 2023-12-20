from django.contrib import admin

from reviews.models import (
    Title,
    Genre,
    Review,
    Comment,
    Categories
)

admin.site.register(Title)
admin.site.register(Categories)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
