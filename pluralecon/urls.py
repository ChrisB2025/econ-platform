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
    """Serve media files in production with Range request support."""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        raise Http404("Media file not found")

    # Get file size
    file_size = os.path.getsize(file_path)

    # Determine content type
    content_type = 'application/octet-stream'
    if path.endswith('.mp3'):
        content_type = 'audio/mpeg'

    # Handle Range requests (required for audio seeking)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    if range_header and range_header.startswith('bytes='):
        # Parse range
        range_spec = range_header[6:]
        if '-' in range_spec:
            start_str, end_str = range_spec.split('-', 1)
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
        else:
            start = 0
            end = file_size - 1

        # Ensure valid range
        end = min(end, file_size - 1)
        length = end - start + 1

        # Open file and seek to start
        f = open(file_path, 'rb')
        f.seek(start)

        response = FileResponse(f, content_type=content_type, status=206)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Content-Length'] = length
    else:
        # Full file response
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Content-Length'] = file_size

    response['Accept-Ranges'] = 'bytes'
    response['Cache-Control'] = 'public, max-age=86400'
    return response


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
