from django.contrib import admin

from orders import models


@admin.register(models.Table)
class Table(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


@admin.register(models.Item)
class Item(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


# @admin.register(models.Order)
# class Order(admin.ModelAdmin):
#     list_display = ('id', 'table_number', 'total_price')
#     search_fields = ('id', 'table_number', 'status')
#     readonly_fields = ('total_price',)