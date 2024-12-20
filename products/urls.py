from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
    path('list/', view=ProductsList.as_view()),
    path('create/', view=CreateProduct.as_view()),
    path('edit/<int:pk>/', view=UpdateProduct.as_view()),
    path('detail/<int:pk>/', view=ProductDetail.as_view()),
    path('delete/<int:pk>/', view=DeleteProduct.as_view()),
]

router = routers.SimpleRouter()
router.register('productCategory', viewset=CategoryViewSet)
urlpatterns += router.urls
