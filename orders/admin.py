from django.contrib import admin

from orders import models


# @admin.register(models.Order)
# class Order(admin.ModelAdmin):
#     list_display = ('id', 'table_number', 'total_price')
#     search_fields = ('id', 'table_number', 'status')
#     readonly_fields = ('total_price',)