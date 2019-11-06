from django.urls import path, include
from .views import checkout, charge

urlpatterns = [
    path('', checkout, name='checkout'),
    path('charge', charge, name='charge')
]