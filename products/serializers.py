from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from .models import *


class ProductsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    image= serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    # category = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = Product
        fields = ['id','name', 'price', 'description',
                  'tags', 'category', 'discount_amount', 'image','quantity']
        
    def get_image(self, obj):
        request = self.context.get('request')
        image = obj.images.all().first()
        if image:
            return request.build_absolute_uri(image.image.url)
        else:
            return None

    
    def get_tags(self, obj):
        current_time = timezone.now()
        days_passed = (current_time - obj.created_at).days

        tags = []
        if days_passed < 5:
            tags.append('NEW')
        if obj.discount_amount>0:
            tags.append(f'{obj.discount_amount}% OFF')
        if obj.only_at_razer:
            tags.append('ONLY AT RAZER')
        if obj.gift:
            tags.append('GIFT WITH PURCHASE')
        return tags
        

class ProductSerializer(serializers.ModelSerializer):
    is_new = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    gift = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only= True)

    class Meta:
        model = Product
        exclude = ['created_at', 'is_active']

    def get_is_new(self, obj):
        current_time = timezone.now()
        days_passed = (current_time - obj.created_at).days

        if days_passed < 5:
            return True
        return False
    
    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        image_urls=[]
        for image in images:
            image_urls.append(request.build_absolute_uri(image.image.url))
        return image_urls
    
    def get_gift(self, obj):
        request = self.context.get('request')
        gift = obj.gift
        return ProductsSerializer(instance=gift, context={
            'request': request}).data


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image_url', ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'



