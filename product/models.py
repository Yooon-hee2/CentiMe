from django.db import models
from django.conf import settings
from crawling import models   
# Create your models here.

class Product(models.Model):
    objects = models.Manager()
    feature = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default = 0, on_delete=models.CASCADE)
    url = models.CharField(max_length=100)
    fit = models.CharField(max_length=5)
    size = models.CharField(max_length=5)

    def __str__(self):
        return self.url



