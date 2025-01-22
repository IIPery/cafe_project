from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]
