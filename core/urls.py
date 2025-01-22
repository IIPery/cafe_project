from django.urls import path, include

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('tables/', views.Table.as_view(), name='tables'),
    path('items/', views.Item.as_view(), name='items'),
    path('orders/', views.Order.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('order_create/', views.OrderCreate.as_view(), name='order_create'),
]
