import pytest

from core import models, consts

@pytest.mark.django_db
def test_table_model():
    table = models.Table.objects.create(number="1")

    assert table.id is not None
    assert table.number == "1"
    assert str(table) == "стол № 1"


@pytest.mark.django_db
def test_item_model():
    item = models.Item.objects.create(name="test", price=111)

    assert item.id is not None
    assert item.name == "test"
    assert item.price == 111
    assert str(item) == "test"


@pytest.mark.django_db
def test_order_model():
    table = models.Table.objects.create(number="1")
    item1 = models.Item.objects.create(name="test1", price=111)
    item2 = models.Item.objects.create(name="test2", price=222)

    order = models.Order.objects.create(table=table, status=consts.STATUS_PENDING)
    order.items.set([item1, item2])

    assert order.id is not None
    assert order.table == table
    assert order.status == consts.STATUS_PENDING
    assert str(order) == f'Заказ {order.id}'
    assert order.total_price == 333