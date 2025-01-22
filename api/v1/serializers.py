from rest_framework import serializers

from core import models


class Table(serializers.ModelSerializer):
    class Meta:
        model = models.Table
        fields = '__all__'


class Item(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class Order(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'

