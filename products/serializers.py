from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    # comments = serializers.SerializerMethodField()
    # type = serializers.PrimaryKeyRelatedField( queryset=ProductType.objects.all())
    class Meta:
        model = Product
        exclude = ['type',]
    
    # def get_comments(self, obj):
    #     type = obj.type
    #     return ProductTypeSerializer(instance=type)
        

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields ='__all__'
