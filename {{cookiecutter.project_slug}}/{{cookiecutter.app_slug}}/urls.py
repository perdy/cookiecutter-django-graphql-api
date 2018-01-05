"""
URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path(r'backend/', admin.site.urls),
    path(r'favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path(r'health_check/', include('health_check.urls', namespace='health_check')),
    path(r'', include('core.urls', namespace='core')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
