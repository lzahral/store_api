from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers

from orders.models import OrderItem
from .models import *


class ProductsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    image= serializers.SerializerMethodField()
    gift = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Product
        fields = ['id','name', 'price', 'description',
                  'tags', 'category','gift', 'discount_amount', 'image','quantity']
        
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
        total_quantity = OrderItem.objects.filter(
            product=obj, order__is_paid=True).aggregate(total=models.Sum('quantity'))['total']
        if not total_quantity:
            total_quantity=0

        tags = []
        if days_passed < 5:
            tags.append('NEW')
        if obj.discount_amount>0:
            tags.append(f'{obj.discount_amount}% OFF')
        if obj.only_at_razer:
            tags.append('ONLY AT RAZER')
        if obj.fresh_off_the_line:
            tags.append('FRESH OFF THE LINE')
        if obj.final_round_gear:
            tags.append('FINAL ROUND GEAR')
        if obj.gift:
            tags.append('GIFT WITH PURCHASE')
        if total_quantity > 20:
            tags.append('BEST SELLERS')
        return tags
        

def get_total_quantity_of_product(product_id):
    total_quantity = OrderItem.objects.filter(
        product_id=product_id).aggregate(total=models.Sum('quantity'))['total']
    return total_quantity if total_quantity is not None else 0

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



