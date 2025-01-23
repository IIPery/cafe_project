import pytest

from core import models, forms, consts


@pytest.mark.django_db
def test_order_form():
    table = models.Table.objects.create(number=1)
    item = models.Item.objects.create(name="test", price=111)
    form_data = {
        'table': table.id,
        'status': consts.STATUS_PENDING,
        'items': [item.id],
    }
    form = forms.Order(data=form_data)

    assert form.is_valid(), f"Форма невалидна: {form.errors}"
    assert 'table' in form.cleaned_data
    assert 'status' in form.cleaned_data
    assert 'items' in form.cleaned_data


@pytest.mark.django_db
def test_table_form():
    form_data = {
        'number': '1',
    }
    form = forms.Table(data=form_data)

    assert form.is_valid(), f"Форма невалидна: {form.errors}"
    table = form.save()
    assert table.number == form_data['number']


@pytest.mark.django_db
def test_item_form():
    form_data = {
        'name': 'test',
        'price': 15,
    }
    form = forms.Item(data=form_data)

    assert form.is_valid(), f"Форма невалидна: {form.errors}"
    item = form.save()
    assert item.name == form_data['name']
    assert item.price == form_data['price']