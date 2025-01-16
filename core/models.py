from django.db import models

from core import consts


class Table(models.Model):
    number = models.CharField('номер стола', max_length=255, db_index=True )

    class Meta:
        verbose_name = 'стол'
        verbose_name_plural = 'столы'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'стол № {self.number}'


class Item(models.Model):
    name = models.CharField('наименование', max_length=255, db_index=True)
    price = models.IntegerField('цена', default=0)

    class Meta:
        verbose_name = 'позиция'
        verbose_name_plural = 'позиции'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    table = models.ForeignKey(
        'core.Table',
        verbose_name='стол',
        on_delete=models.CASCADE,
    )
    items = models.ManyToManyField('core.Item', verbose_name='позиции', blank=True)
    status = models.CharField(
        'статус',
        max_length=255,
        choices=consts.STATUS_CHOICES,
        default=consts.STATUS_PENDING,
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'Заказ {self.id}'

    @property
    def total_price(self) -> int:
        return 0 or sum(self.items.values_list('price', flat=True))