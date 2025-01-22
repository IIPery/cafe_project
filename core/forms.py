from django import forms

from core import models, consts


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['table', 'status', 'items']

    table = forms.ModelChoiceField(queryset=models.Table.objects.all(), required=True)
    items = forms.ModelMultipleChoiceField(queryset=models.Item.objects.all(), required=False)
    status = forms.ChoiceField(choices=consts.STATUS_CHOICES, required=True)


class TableForm(forms.ModelForm):
    class Meta:
        model = models.Table
        fields = ['number']


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ['name', 'price']
