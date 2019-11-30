from django.db import models
from crawling.models import Category
from django.conf import settings
# Create your models here.

class Product(models.Model):
    objects = models.Manager()
    feature = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE )
    size = models.CharField(max_length=5)
    fit = models.CharField(max_length=5, default='보통')
    url = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    thumbnail = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        
    # def __str__(self):
    #     return self.url

class Outer(Product):
    bust = models.FloatField(default=0)
    shoulder = models.FloatField(default=0)
    armhole = models.FloatField(default=0)
    sleeve = models.FloatField(default=0)
    sleevewidth = models.FloatField(default=0)
    length = models.FloatField(default=0)

class Top(Product):
    bust = models.FloatField(default=0)
    shoulder = models.FloatField(default=0)
    armhole = models.FloatField(default=0)
    sleeve = models.FloatField(default=0)
    sleevewidth = models.FloatField(default=0)
    length = models.FloatField(default=0)

class Skirt(Product):
    waist = models.FloatField(default=0)
    hip = models.FloatField(default=0)
    hem = models.FloatField(default=0)
    length = models.FloatField(default=0)

class Ops(Product):
    waist = models.FloatField(default=0)
    shoulder = models.FloatField(default=0)
    armhole = models.FloatField(default=0)
    sleeve = models.FloatField(default=0)
    sleevewidth = models.FloatField(default=0)
    hip = models.FloatField(default=0)
    length = models.FloatField(default=0)

class Pants(Product):
    waist = models.FloatField(default=0)
    hip = models.FloatField(default=0)
    thigh = models.FloatField(default=0)
    hem = models.FloatField(default=0)
    crotch_rise = models.FloatField(default=0)
    length = models.FloatField(default=0)