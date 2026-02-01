from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Chatbot API
    path('api/chat/', views.chatbot_api, name='chatbot_api'),
    path('api/chat/status/', views.chatbot_status, name='chatbot_status'),

    # Topic hub (e.g., /topics/inflation/)
    path('topics/<slug:topic_slug>/', views.topic_hub, name='topic_hub'),

    # Comparisons tool (e.g., /topics/inflation/compare/) - must come before school_slug
    path('topics/<slug:topic_slug>/compare/', views.comparisons, name='comparisons'),

    # Teaching materials list (e.g., /topics/inflation/materials/) - must come before school_slug
    path('topics/<slug:topic_slug>/materials/', views.materials, name='materials'),

    # Single material detail (e.g., /topics/inflation/materials/1/)
    path('topics/<slug:topic_slug>/materials/<int:material_id>/', views.material_detail, name='material_detail'),

    # Material downloads
    path('topics/<slug:topic_slug>/materials/<int:material_id>/download/', views.material_download, name='material_download'),
    path('topics/<slug:topic_slug>/materials/<int:material_id>/download/<str:format>/', views.material_download, name='material_download_format'),
    path('topics/<slug:topic_slug>/materials/download-all/', views.all_materials_download, name='all_materials_download'),

    # School explanation (e.g., /topics/inflation/neoclassical/) - generic slug last
    path('topics/<slug:topic_slug>/<slug:school_slug>/', views.explanation_detail, name='explanation'),
]
