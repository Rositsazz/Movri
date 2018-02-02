from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=200)
    reviews_url = models.URLField(blank=True)
    asin = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    positive_reviews = models.TextField(null=True, blank=True)
    negative_reviews = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.asin + ' - ' + self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200)
    rating = models.FloatField(validators=[MinValueValidator(float('0.00')),
                                           MaxValueValidator(float('5.00'))])
    date = models.DateField()

    def __str__(self):
        return self.author + ": " + self.content[:30]
