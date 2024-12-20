from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.permissions import IsAuthenticated


class GetCart(APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    def get(self, request):
        user = request.user
        cart = Order.objects.filter(is_paid=False, user=user).last()
        if cart:
            srz_data = OrderSerializer(instance=cart, context={
                'request': request}).data
            return Response(srz_data, status=status.HTTP_200_OK)
        return Response({'message': 'No active cart found.'}, status=status.HTTP_404_NOT_FOUND)


class AddItem(APIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        srz_data = OrderItemSerializer(data=request.data, context={
            'user': request.user})
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class Checkout(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        cart = Order.objects.filter(is_paid=False, user=request.user).last()
        errors = []
        with transaction.atomic():
            for item in cart.items.all():
                product = item.product
                if product.quantity < item.quantity:
                    errors. append(
                        {'id':item.id, f'error': "Stock has changed since cart was created"})
            if errors:
                return Response(errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                for item in cart.items.all():
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()
            cart.is_paid = True
            cart.save()
        return Response({'message': 'Checkout completed successfully.'},status=status.HTTP_200_OK)


class DeleteCart(APIView):
    permission_classes = [IsAuthenticated,]

    def delete(self, request):
        cart = Order.objects.filter(is_paid=False, user=request.user).last()
        # for item in cart.items.all():
        #     item.product.quantity += item.quantity
        #     item.product.save()
        cart.delete()
        return Response({'message': 'cart deleted'}, status=status.HTTP_200_OK)


class DeleteItem(APIView):
    permission_classes = [IsAuthenticated,]

    def delete(self, request, pk):
        item = get_object_or_404(OrderItem, pk=pk)
        order = item.order
        # gift = item.product.gift
        # if gift:
        #     # gift.quantity += 1
        #     # gift.save()
        #     OrderItem.objects.get(order=order, product=gift).delete()
        # item.product.quantity += item.quantity 
        # item.product.save()
        item.delete()
        if not order.items.exists():
            order.delete()
        return Response({'message': 'item deleted'}, status=status.HTTP_200_OK)
