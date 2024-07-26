from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404

from accounts.serializers import UserSerializer

class Register(APIView):
    serializer_class = UserSerializer

    def post(self, req):
        srz_data = UserSerializer(data=req.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
