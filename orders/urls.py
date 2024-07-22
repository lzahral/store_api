from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# router.register(r"^(?P<order_id>\d+)/order-items", OrderItemViewSet)
# router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('get-cart/', view=GetCart.as_view()),
    path('add-item/', view=AddItem.as_view()),

]
