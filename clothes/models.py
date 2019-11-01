from django.db import models
from crawling.models import Category
from django.conf import settings
# Create your models here.

class Product(models.Model):
    objects = models.Manager()
    feature = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    size = models.CharField(max_length=5)
    fit = models.CharField(max_length=5)
    url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.url
