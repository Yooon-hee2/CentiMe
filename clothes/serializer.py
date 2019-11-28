from .models import Product, Ops, Outer, Top, Skirt, Pants
from crawling.models import Category
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ops
        fields = '__all__'

class OuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outer
        fields = '__all__'

class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top
        fields = '__all__'

class PantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pants
        fields = '__all__'

class SkirtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pants
        fields = '__all__'

