from django.urls import path
from .views import *

urlpatterns = [
    path('get-cart/', view=GetCart.as_view()),
    path('add-item/', view=AddItem.as_view()),
    path('checkout/', view=Checkout.as_view()),
    path('delete-cart/', view=DeleteCart.as_view()),
    path('delete-item/<int:pk>/', view=DeleteItem.as_view()),

]
