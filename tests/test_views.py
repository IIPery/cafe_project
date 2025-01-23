import pytest
from django.urls import reverse

from core import models, consts


@pytest.mark.django_db
def test_index_view(client):
    table1 = models.Table.objects.create(number="1")
    table2 = models.Table.objects.create(number="2")

    order1 = models.Order.objects.create(table=table1, status=consts.STATUS_PENDING)
    order2 = models.Order.objects.create(table=table1, status=consts.STATUS_READY)
    order3 = models.Order.objects.create(table=table2, status=consts.STATUS_PAID)

    url = reverse('core:index')
    response = client.get(url)
    assert response.status_code == 200

    tables = response.context['tables']
    assert len(tables) == 2

    table1_orders = tables[0].orders
    table2_orders = tables[1].orders
    assert len(table1_orders) == 2
    assert len(table2_orders) == 0
    assert order1 in table1_orders
    assert order2 in table1_orders


@pytest.mark.django_db
def test_table_view(client):
    data = {
        'add_table': True,
        'number': '3',
    }
    response = client.post(reverse('core:tables'), data)

    assert models.Table.objects.filter(number='3').exists()
    assert response.status_code == 302


@pytest.mark.django_db
def test_item_view(client):
    data = {
        'add_item': True,
        'name': 'test',
        'price': 111,
    }
    response = client.post(reverse('core:items'), data)

    assert models.Item.objects.filter(name='test').exists()
    assert response.status_code == 302


@pytest.mark.django_db
def test_order_view(client):
    table1 = models.Table.objects.create(number='1')
    table2 = models.Table.objects.create(number='2')
    item = models.Item.objects.create(name='test', price=111)

    order1 = models.Order.objects.create(
        table=table1,
        status=consts.STATUS_PAID
    )
    order1.items.add(item)

    order2 = models.Order.objects.create(
        table=table2,
        status=consts.STATUS_PENDING
    )
    order2.items.add(item)

    response = client.get(reverse('core:orders'))
    assert response.status_code == 200
    assert len(response.context['orders']) == 2

    response = client.get(reverse('core:orders'), {'search_table_number': '1'})
    assert len(response.context['orders']) == 1

    response = client.get(reverse('core:orders'), {'search_status': 'оплачено'})
    assert len(response.context['orders']) == 1

    assert 'total_revenue' in response.context
    assert response.context['total_revenue'] == 111
