from django.contrib import admin
from .models import Product, Outer, Top, Skirt, Ops, Pants
# Register your models here.
admin.site.register(Product)
admin.site.register(Outer)
admin.site.register(Top)
admin.site.register(Ops)
admin.site.register(Skirt)
admin.site.register(Pants)

