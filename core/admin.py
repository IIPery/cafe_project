from django.contrib import admin

from core import models


@admin.register(models.Table)
class Table(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


@admin.register(models.Item)
class Item(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


@admin.register(models.Order)
class Order(admin.ModelAdmin):
    list_display = ('id', 'table', 'get_total_price', 'status')
    search_fields = ('table__number', 'status')
    list_filter = ('table', 'status')
    filter_horizontal = ('items',)

    @admin.display(description='сумма')
    def get_total_price(self, instance: models.Order) -> int:
        return instance.total_price