"""
URL configuration for pluralecon project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    """Simple healthcheck endpoint for Railway."""
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('', include('topics.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
