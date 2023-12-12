from django.db import models


class Reviews(models.Model):
    author = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        'Titles', on_delete=models.CASCADE, related_name='reviews')
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
        'User', on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(
        'Titles', on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
