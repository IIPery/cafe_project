from rest_framework import viewsets

from core import models
from api.v1 import serializers


class Table(viewsets.ModelViewSet):
    queryset = models.Table.objects.all()
    serializer_class = serializers.Table


class Item(viewsets.ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.Item


class Order(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.Order