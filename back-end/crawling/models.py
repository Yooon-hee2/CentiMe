from django.db import models

# Create your models here.
class Category(models.Model):
    dic = (
        ('TOP', 'top'),
        ('OUTER', 'outer'),
        ('PANTS', 'pants'),
        ('SKIRT', 'skirt'),
        ('OPS', 'ops'),
    )
    category = models.CharField(max_length=6, choices=dic)

    def __str__(self):
        return self.category

