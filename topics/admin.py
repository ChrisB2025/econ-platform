from django.contrib import admin
from .models import (
    School, Topic, Explanation, ComparisonQuestion,
    SchoolPosition, TeachingMaterial, AudioContent
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'color']
    list_editable = ['order', 'color']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']


class ExplanationInline(admin.TabularInline):
    model = Explanation
    extra = 0
    fields = ['school', 'title', 'tier']
    readonly_fields = ['school']


class ComparisonQuestionInline(admin.TabularInline):
    model = ComparisonQuestion
    extra = 0
    fields = ['question', 'order']


class TeachingMaterialInline(admin.TabularInline):
    model = TeachingMaterial
    extra = 0
    fields = ['title', 'material_type', 'tier']


class AudioContentInline(admin.TabularInline):
    model = AudioContent
    extra = 0
    fields = ['title', 'audio_type', 'duration_seconds']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_published', 'tier', 'updated_at']
    list_filter = ['is_published', 'tier']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'introduction']
    inlines = [ExplanationInline, ComparisonQuestionInline, TeachingMaterialInline, AudioContentInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_published')
        }),
        ('Content', {
            'fields': ('introduction', 'tier'),
        }),
    )


@admin.register(Explanation)
class ExplanationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'topic', 'school', 'tier', 'updated_at']
    list_filter = ['topic', 'school', 'tier']
    search_fields = ['title', 'content', 'core_idea']
    fieldsets = (
        (None, {
            'fields': ('topic', 'school', 'title', 'tier')
        }),
        ('Main Content', {
            'fields': ('content', 'core_idea'),
        }),
        ('Structured Sections', {
            'fields': ('key_figures', 'strengths', 'limitations'),
            'classes': ('collapse',),
        }),
    )


class SchoolPositionInline(admin.TabularInline):
    model = SchoolPosition
    extra = 0
    fields = ['school', 'position_summary']


@admin.register(ComparisonQuestion)
class ComparisonQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'topic', 'order']
    list_filter = ['topic']
    list_editable = ['order']
    search_fields = ['question', 'description']
    inlines = [SchoolPositionInline]
    fieldsets = (
        (None, {
            'fields': ('topic', 'question', 'order')
        }),
        ('Details', {
            'fields': ('description', 'points_of_agreement', 'key_divergence'),
        }),
    )


@admin.register(SchoolPosition)
class SchoolPositionAdmin(admin.ModelAdmin):
    list_display = ['school', 'question', 'position_summary']
    list_filter = ['school', 'question__topic']
    search_fields = ['position_summary', 'detailed_position']


@admin.register(TeachingMaterial)
class TeachingMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'material_type', 'tier', 'updated_at']
    list_filter = ['topic', 'material_type', 'tier']
    search_fields = ['title', 'description', 'content']
    fieldsets = (
        (None, {
            'fields': ('topic', 'title', 'material_type', 'tier')
        }),
        ('Content', {
            'fields': ('description', 'content'),
        }),
        ('File', {
            'fields': ('file',),
            'classes': ('collapse',),
        }),
    )


@admin.register(AudioContent)
class AudioContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'audio_type', 'duration_display', 'tier']
    list_filter = ['topic', 'audio_type', 'tier']
    search_fields = ['title', 'description', 'script']
    readonly_fields = ['duration_display']
    fieldsets = (
        (None, {
            'fields': ('topic', 'title', 'audio_type', 'tier')
        }),
        ('Content', {
            'fields': ('description', 'script'),
        }),
        ('Audio File', {
            'fields': ('audio_file', 'duration_seconds', 'duration_display'),
        }),
    )

    def duration_display(self, obj):
        return obj.duration_display or "—"
    duration_display.short_description = "Duration"
