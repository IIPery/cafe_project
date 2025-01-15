from django.db import models


class Table(models.Model):
    number = models.CharField('номер стола', max_length=100, db_index=True )

    class Meta:
        verbose_name = 'стол'
        verbose_name_plural = 'столы'
        ordering = ('id',)



# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'в ожидании'),
#         ('ready', 'готово'),
#         ('paid', 'оплачено'),
#     ]
#
#     table_number = models.IntegerField('номер стола', blank=False)
#     items = models.JSONField('заказы',max_length=255, db_index=True, blank=True)
#     total_price = models.IntegerField('к оплате', blank=True)
#     status = models.CharField('статус', max_length=255, choices=STATUS_CHOICES, default='pending')
#
#     class Meta:
#         verbose_name = 'заказ'
#         verbose_name_plural = 'заказы'
#         ordering = ('id',)
#
#     def __str__(self) -> str:
#         return f'Заказ {self.id} - Стол {self.table_number}'
#
#     def save(self, *args, **kwargs) -> None:
#         self.total_price = sum(item['price'] for item in self.items)
#         super().save(*args, **kwargs)
