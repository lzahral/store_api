from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *


class ProductsList(APIView):
    serializer_class = ProductSerializer

    def get(self, req):
        products = Product.objects.all()
        srz_data = ProductSerializer(instance=products, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class CreateProduct(APIView):
    serializer_class = ProductSerializer

    def post(self, req):
        srz_data = ProductSerializer(data=req.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProduct(APIView):
    serializer_class = ProductSerializer

    def put(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        srz_data = ProductSerializer(instance=product, data=req.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteProduct(APIView):
    serializer_class = ProductSerializer

    def delete(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'message': 'product deleted'}, status=status.HTTP_200_OK)


class TypeViewSet(viewsets.ViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    def list(self, request):
        data = ProductType.objects.all()
        srz_data = ProductTypeSerializer(instance=data, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        srz_data = ProductTypeSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        type = get_object_or_404(ProductTypeSerializer, pk=pk)
        type.delete()
        return Response({'message': 'productType deleted'}, status=status.HTTP_200_OK)
