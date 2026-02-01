import json
import markdown
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Topic, School, Explanation, ComparisonQuestion, TeachingMaterial, AudioContent
from .services import chatbot_service


def render_markdown(text):
    """Convert markdown text to HTML."""
    if not text:
        return ''
    return markdown.markdown(
        text,
        extensions=['tables', 'fenced_code', 'toc', 'nl2br']
    )


def home(request):
    """Home page showing available topics."""
    topics = Topic.objects.filter(is_published=True)
    return render(request, 'topics/home.html', {
        'topics': topics,
    })


def topic_hub(request, topic_slug):
    """
    Topic hub page showing introduction and school navigation.
    This is the main entry point for a topic like 'inflation'.
    """
    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    schools = School.objects.all()
    explanations = topic.explanations.select_related('school').all()

    # Create a mapping of school -> explanation for easy template access
    school_explanations = {exp.school.slug: exp for exp in explanations}

    return render(request, 'topics/topic_hub.html', {
        'topic': topic,
        'schools': schools,
        'explanations': explanations,
        'school_explanations': school_explanations,
        'introduction_html': render_markdown(topic.introduction),
        'chatbot_enabled': chatbot_service.is_configured(),
    })


def explanation_detail(request, topic_slug, school_slug):
    """
    Display a specific school's explanation of a topic.
    """
    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    school = get_object_or_404(School, slug=school_slug)
    explanation = get_object_or_404(Explanation, topic=topic, school=school)

    # Get all schools for navigation
    schools = School.objects.all()
    explanations = topic.explanations.select_related('school').all()

    return render(request, 'topics/explanation.html', {
        'topic': topic,
        'school': school,
        'explanation': explanation,
        'schools': schools,
        'explanations': explanations,
        'content_html': render_markdown(explanation.content),
        'chatbot_enabled': chatbot_service.is_configured(),
    })


def comparisons(request, topic_slug):
    """
    Display comparison tool for a topic.
    """
    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    schools = School.objects.all()
    questions = topic.comparison_questions.prefetch_related(
        'positions', 'positions__school'
    ).all()

    # Get selected schools from query params (default: all)
    selected_slugs = request.GET.getlist('schools')
    if selected_slugs:
        selected_schools = School.objects.filter(slug__in=selected_slugs)
    else:
        selected_schools = schools

    return render(request, 'topics/comparisons.html', {
        'topic': topic,
        'schools': schools,
        'selected_schools': selected_schools,
        'questions': questions,
        'chatbot_enabled': chatbot_service.is_configured(),
    })


def materials(request, topic_slug):
    """
    Display teaching materials for a topic.
    """
    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    materials_list = topic.materials.all()
    audio_content = topic.audio_content.all()

    return render(request, 'topics/materials.html', {
        'topic': topic,
        'materials': materials_list,
        'audio_content': audio_content,
        'chatbot_enabled': chatbot_service.is_configured(),
    })


def material_detail(request, topic_slug, material_id):
    """
    Display a single teaching material.
    """
    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    material = get_object_or_404(TeachingMaterial, id=material_id, topic=topic)

    return render(request, 'topics/material_detail.html', {
        'topic': topic,
        'material': material,
        'content_html': render_markdown(material.content),
        'chatbot_enabled': chatbot_service.is_configured(),
    })


@require_http_methods(["POST"])
def chatbot_api(request):
    """
    API endpoint for the teaching chatbot.

    Expects JSON body with:
    - messages: list of {role: "user"|"assistant", content: "..."}
    - topic_context: optional string describing current page context

    Returns JSON with:
    - success: boolean
    - response: assistant message (if success)
    - error: error message (if not success)
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON in request body'
        }, status=400)

    messages = data.get('messages', [])
    topic_context = data.get('topic_context', None)

    if not messages:
        return JsonResponse({
            'success': False,
            'error': 'No messages provided'
        }, status=400)

    # Validate message format
    for msg in messages:
        if 'role' not in msg or 'content' not in msg:
            return JsonResponse({
                'success': False,
                'error': 'Each message must have "role" and "content" fields'
            }, status=400)
        if msg['role'] not in ('user', 'assistant'):
            return JsonResponse({
                'success': False,
                'error': 'Message role must be "user" or "assistant"'
            }, status=400)

    # Get response from chatbot service
    result = chatbot_service.get_response(messages, topic_context)

    if result['success']:
        return JsonResponse({
            'success': True,
            'response': result['response']
        })
    else:
        return JsonResponse({
            'success': False,
            'error': result['error']
        }, status=500)


def chatbot_status(request):
    """Check if the chatbot is configured and available."""
    return JsonResponse({
        'configured': chatbot_service.is_configured()
    })


def material_download(request, topic_slug, material_id, format='md'):
    """
    Download a teaching material as a file.

    Supports formats:
    - md: Markdown format
    - txt: Plain text format
    """
    from django.http import HttpResponse
    from django.utils.text import slugify

    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    material = get_object_or_404(TeachingMaterial, id=material_id, topic=topic)

    # If there's an uploaded file and user wants that, serve it
    if material.file and format == 'file':
        response = HttpResponse(material.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{material.file.name.split("/")[-1]}"'
        return response

    # Generate filename
    filename_base = slugify(f"{topic.name}-{material.title}")

    if format == 'txt':
        # Plain text - strip markdown formatting
        import re
        content = material.content
        # Remove markdown headers but keep text
        content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
        # Remove bold/italic markers
        content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
        content = re.sub(r'\*(.+?)\*', r'\1', content)
        # Remove links but keep text
        content = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', content)

        response = HttpResponse(content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename_base}.txt"'
    else:
        # Markdown format (default)
        # Add header with metadata
        header = f"""# {material.title}

**Topic:** {topic.name}
**Type:** {material.get_material_type_display()}
**Source:** Pluralist Economics Platform

---

"""
        content = header + material.content

        response = HttpResponse(content, content_type='text/markdown; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename_base}.md"'

    return response


def all_materials_download(request, topic_slug):
    """
    Download all materials for a topic as a single markdown file.
    """
    from django.http import HttpResponse
    from django.utils.text import slugify

    topic = get_object_or_404(Topic, slug=topic_slug, is_published=True)
    materials_list = topic.materials.all()

    if not materials_list:
        return HttpResponse("No materials available.", status=404)

    # Build combined document
    content = f"""# {topic.name} - Teaching Materials

**Source:** Pluralist Economics Platform
**Total Materials:** {materials_list.count()}

---

"""

    for material in materials_list:
        content += f"""
## {material.title}

**Type:** {material.get_material_type_display()}

{material.content}

---

"""

    filename = slugify(f"{topic.name}-all-materials")
    response = HttpResponse(content, content_type='text/markdown; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}.md"'
    return response
