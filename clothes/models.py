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

class Outer_Top(Product):
    bust = models.IntegerField(default=0)
    shoulder = models.IntegerField(default=0)
    armhole = models.IntegerField(default=0)
    sleeve = models.IntegerField(default=0)
    sleevewidth = models.IntegerField(default=0)
    length = models.IntegerField(default=0)

class Skirt(Product):
    waist = models.IntegerField(default=0)
    hip = models.IntegerField(default=0)
    hem = models.IntegerField(default=0)
    length = models.IntegerField(default=0)

class Ops(Product):
    waist = models.IntegerField(default=0)
    shoulder = models.IntegerField(default=0)
    armhole = models.IntegerField(default=0)
    sleeve = models.IntegerField(default=0)
    sleevewidth = models.IntegerField(default=0)
    hip = models.IntegerField(default=0)
    length = models.IntegerField(default=0)

class Pants(Product):
    waist = models.IntegerField(default=0)
    hip = models.IntegerField(default=0)
    thigh = models.IntegerField(default=0)
    hem = models.IntegerField(default=0)
    crotch_rise = models.IntegerField(default=0)
    length = models.IntegerField(default=0)