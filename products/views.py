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
    serializer_class = ProductsSerializer

    def get(self, req):
        products = Product.objects.filter(is_active=True, quantity__gt=0)
        srz_data = ProductsSerializer(instance=products, many=True, context={
                                     'request': req}).data
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
    
class ProductDetail(APIView):
    serializer_class = ProductSerializer

    def get(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        srz_data = ProductSerializer(instance=product, context={
                                     'request': req})
        return Response(srz_data.data, status=status.HTTP_200_OK)
    

class DeleteProduct(APIView):

    def delete(self, req, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'message': 'product deleted'}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    def list(self, request):
        data = ProductCategory.objects.all()
        srz_data = ProductCategorySerializer(
            instance=data, many=True, context={'request': request})
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        srz_data = ProductCategorySerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        category = get_object_or_404(ProductCategorySerializer, pk=pk)
        category.delete()
        return Response({'message': 'productCategory deleted'}, status=status.HTTP_200_OK)
