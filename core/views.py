from typing import Dict

from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404


from core import models
from core import consts


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
            if number := request.POST.get('number'):
                models.Table.objects.create(number=number)
                messages.success(request, f'Стол № {number} успешно добавлен!')
            else:
                messages.error(request, 'Номер стола не может быть пустым!')

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
            name = request.POST.get('name')
            price = request.POST.get('price')

            if name and price:
                try:
                    price = int(price)
                    models.Item.objects.create(name=name, price=price)
                except ValueError:
                    pass

        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(models.Item, id=item_id)
            item.delete()

        elif 'edit_item' in request.POST:
            item_id = request.POST.get('item_id')
            name = request.POST.get('name')
            price = request.POST.get('price')

            try:
                item = get_object_or_404(models.Item, id=item_id)
                if name:
                    item.name = name
                if price:
                    item.price = int(price)
                item.save(update_fields=['name', 'price'])
            except ValueError:
                pass

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

        table_id = request.POST.get('table')
        items_ids = request.POST.getlist('items')
        status = request.POST.get('status')

        if table_id:
            order.table_id = table_id

        if items_ids:
            order.items.set(items_ids)
        else:
            order.items.clear()

        if status in dict(consts.STATUS_CHOICES):
            order.status = status

        order.save(update_fields=['table_id', 'status'])
        return redirect('core:orders')


class OrderCreate(CreateView):
    model = models.Order
    template_name = 'order_create.html'
    fields = ['table', 'status', 'items']
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