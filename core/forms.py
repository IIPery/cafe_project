from django import forms

from core import models, consts


class Order(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['table', 'status', 'items']

    table = forms.ModelChoiceField(queryset=models.Table.objects.all(), required=True)
    items = forms.ModelMultipleChoiceField(queryset=models.Item.objects.all(), required=False)
    status = forms.ChoiceField(choices=consts.STATUS_CHOICES, required=True)


class Table(forms.ModelForm):
    class Meta:
        model = models.Table
        fields = ['number']


class Item(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['name', 'price']
