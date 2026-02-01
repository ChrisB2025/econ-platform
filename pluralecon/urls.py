"""
URL configuration for pluralecon project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, FileResponse, Http404
from django.views.static import serve
import os


def health_check(request):
    """Simple healthcheck endpoint for Railway."""
    return JsonResponse({'status': 'ok'})


def serve_media(request, path):
    """Serve media files in production with caching headers."""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        response = FileResponse(open(file_path, 'rb'))
        # Set content type for audio files
        if path.endswith('.mp3'):
            response['Content-Type'] = 'audio/mpeg'
        # Cache for 1 day
        response['Cache-Control'] = 'public, max-age=86400'
        return response
    raise Http404("Media file not found")


urlpatterns = [
    path('health', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('', include('topics.urls')),
]

# Serve media files (both development and production)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Production: serve media files with caching
    urlpatterns += [
        path('media/<path:path>', serve_media, name='serve_media'),
    ]
