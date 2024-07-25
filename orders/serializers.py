from rest_framework import serializers

from products.models import Product
from .models import Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url',
                  'description', 'price', 'discount_amount']

    def get_image_url(self, obj):
        request = self.context.get('request')
        image = obj.images.first()
        return request.build_absolute_uri(image.image.url)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']
        extra_kwargs = {'id': {'read_only': True}, }

    def validate(self, validated_data):
        user = self.context['user']
        product = validated_data.get("product")
        order_quantity = validated_data.get("quantity")
        product_quantity = product.quantity

        if order_quantity > product_quantity:
            raise serializers.ValidationError(
                {"quantity": "Ordered quantity is more than the stock."})

        order = Order.objects.filter(user=user, is_paid=False).last()

        if order:
            if OrderItem.objects.filter(order=order, product=product).exists():
                raise serializers.ValidationError(
                    {"product": "Product already exists in your order."})

        return validated_data

    def create(self, validated_data):
        user = self.context['user']
        order = Order.objects.filter(user=user, is_paid=False).last()

        if not order:
            order = Order.objects.create(user=user)

        validated_data['order'] = order
        product = validated_data['product']

        if product.gift:
            OrderItem.objects.create(
                order=order, product=product.gift, price=0, quantity=1)
            # product.gift.quantity -= 1
            # product.gift.save()

        validated_data['price'] = (
            product.price * (1 - product.discount_amount / 100)
            if product.discount_amount > 0
            else product.price
        )
        # product.quantity -= validated_data['quantity']
        # product.save()
        return super().create(validated_data)
    

class OrderListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        extra_kwargs = {'id': {'read_only': True}, }



class OrderSerializer(serializers.ModelSerializer):
    items = OrderListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items']
