from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User


class GetCart(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        # user = request.user
        user = User.objects.get(id=1)
        cart = Order.objects.filter(is_paid=False, user=user)
        if cart:
            srz_data = OrderSerializer(instance=cart).data
            return Response(srz_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class AddItem(APIView):
    serializer_class = OrderItemSerializer

    def post(self, request):
        srz_data = OrderItemSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     # permission_classes = [permissions.IsAuthenticated]

#     # def get_queryset(self):
#     #     return self.queryset.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         order = serializer.save(user=self.request.user)
#         items = self.request.data.get('items', [])
#         for item_data in items:
#             OrderItem.objects.create(order=order, **item_data)
#         return order


#     @action(detail=True, methods=['post'])
#     def mark_paid(self, request, pk=None):
#         order = self.get_object()
#         order.is_paid = True
#         order.save()
#         return Response(OrderSerializer(order).data)


# class OrderItemViewSet(viewsets.ModelViewSet):
#     """
#     CRUD order items that are associated with the current order id.
#     """

#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
#     # permission_classes = [IsOrderItemByBuyerOrAdmin]

#     def get_queryset(self):
#         res = super().get_queryset()
#         order_id = self.kwargs.get("order_id")
#         return res.filter(order__id=order_id)

#     def perform_create(self, serializer):
#         order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
#         serializer.save(order=order)

#     # def get_permissions(self):
#     #     if self.action in ("create", "update", "partial_update", "destroy"):
#     #         self.permission_classes += [IsOrderItemPending]

#     #     return super().get_permissions()
