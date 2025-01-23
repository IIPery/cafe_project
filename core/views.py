from typing import Dict

from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


from core import models, consts, forms


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        tables = models.Table.objects.all()

        for table in tables:
            table.orders = models.Order.objects.filter(
                table=table,
                status__in=[consts.STATUS_PENDING, consts.STATUS_READY]
            )

        context['tables'] = tables
        return context


class Table(ListView):
    model = models.Table
    template_name = 'tables.html'
    context_object_name = 'tables'

    def post(self, request, *args, **kwargs) -> HttpResponse:
        if 'add_table' in request.POST:
            form = forms.Table(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Стол № {form.cleaned_data["number"]} успешно добавлен!')
            else:
                messages.error(request, 'Ошибка при добавлении стола!')

        elif 'delete_table' in request.POST:
            table_id = request.POST.get('table_id')
            try:
                table = models.Table.objects.get(id=table_id)
                table.delete()
                messages.success(request, f'Стол № {table.number} успешно удален!')
            except models.Table.DoesNotExist:
                messages.error(request, 'Стол не найден!')

        return redirect('core:tables')


class Item(ListView):
    model = models.Item
    template_name = 'items.html'
    context_object_name = 'items'

    def post(self, request, *args, **kwargs) -> HttpResponse:
        if 'add_item' in request.POST:
            form = forms.Item(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Позиция "{form.cleaned_data["name"]}" успешно добавлена!')
            else:
                messages.error(request, 'Ошибка при добавлении позиции!')


        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(models.Item, id=item_id)
            item.delete()

        elif 'edit_item' in request.POST:
            form = forms.Item(request.POST, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, f'Позиция "{form.cleaned_data["name"]}" успешно обновлена!')
            else:
                messages.error(request, 'Ошибка при обновлении позиции!')

        return redirect('core:items')


class Order(ListView):
    model = models.Order
    template_name = 'orders.html'
    context_object_name = 'orders'
    ordering = ['-id']

    def get_queryset(self) -> QuerySet[models.Order]:
        queryset = super().get_queryset()

        search_table_number = self.request.GET.get('search_table_number', '')
        search_status = self.request.GET.get('search_status', '')

        if search_table_number:
            queryset = queryset.filter(table__number__icontains=search_table_number)
        if search_status:
            queryset = queryset.filter(status=search_status)

        return queryset

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)

        total_revenue = sum(order.total_price for order in context['orders'] if order.status == 'оплачено')

        context['total_revenue'] = total_revenue
        return context


class OrderDetail(DetailView):
    model = models.Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['tables'] = models.Table.objects.all()
        context['items'] = models.Item.objects.all()
        context['status_choices'] = consts.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        order = self.get_object()

        if 'delete_order' in request.POST:
            order.delete()
            return redirect('core:orders')

        form = forms.Order(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(request, 'Заказ успешно обновлен!')
            return redirect('core:orders')
        else:
            messages.error(request, 'Ошибка при обновлении заказа!')
            return self.render_to_response({'form': form})


class OrderCreate(CreateView):
    model = models.Order
    template_name = 'order_create.html'
    form_class = forms.Order
    success_url = reverse_lazy('core:index')

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['tables'] = models.Table.objects.all()
        context['items'] = models.Item.objects.all()
        context['status_choices'] = consts.STATUS_CHOICES

        table_id = self.request.GET.get('table_id')
        if table_id:
            context['form'].fields['table'].initial = get_object_or_404(models.Table, id=table_id)

        return context