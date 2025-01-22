from django.urls import path, include
from rest_framework import routers

from api.v1 import views

app_name = 'v1'

router = routers.DefaultRouter()
router.register('tables', views.Table, basename='tables')
router.register('items', views.Item, basename='items')
router.register('orders', views.Order, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
]
