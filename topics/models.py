from django.db import models


class ContentTier(models.IntegerChoices):
    """Content provenance tiers as defined in PROJECT_BRIEF.md"""
    TIER_1 = 1, "Approved Reference Content"
    TIER_2 = 2, "Resource-Informed Platform Content"
    TIER_3 = 3, "Generative On-Demand Content"


class School(models.Model):
    """A school of economic thought (e.g., Neoclassical, Post-Keynesian, MMT)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(
        help_text="Brief description of this school's approach (1-2 sentences)"
    )
    color = models.CharField(
        max_length=7,
        default="#3498db",
        help_text="Hex color code for UI display"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower = first)"
    )

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Topic(models.Model):
    """A topic hub (e.g., Inflation) containing explanations from multiple schools"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    introduction = models.TextField(
        help_text="Neutral introduction to this topic (Tier 2 content)"
    )
    tier = models.IntegerField(
        choices=ContentTier.choices,
        default=ContentTier.TIER_2
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Explanation(models.Model):
    """A school's explanation of a topic (the main content)"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='explanations'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='explanations'
    )
    title = models.CharField(
        max_length=300,
        help_text="e.g., 'The Neoclassical View: Inflation as a Demand and Expectations Problem'"
    )
    content = models.TextField(
        help_text="Full explanation in Markdown format"
    )
    core_idea = models.TextField(
        blank=True,
        help_text="Brief summary of the core argument"
    )
    key_figures = models.TextField(
        blank=True,
        help_text="Notable economists associated with this view"
    )
    strengths = models.TextField(
        blank=True,
        help_text="Acknowledged strengths of this perspective"
    )
    limitations = models.TextField(
        blank=True,
        help_text="Acknowledged limitations and critiques"
    )
    tier = models.IntegerField(
        choices=ContentTier.choices,
        default=ContentTier.TIER_2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['school__order']
        unique_together = ['topic', 'school']

    def __str__(self):
        return f"{self.school.name} on {self.topic.name}"


class ComparisonQuestion(models.Model):
    """A question/dimension for comparing schools (e.g., 'What causes inflation?')"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='comparison_questions'
    )
    question = models.CharField(
        max_length=300,
        help_text="The comparison question, e.g., 'What causes inflation?'"
    )
    description = models.TextField(
        blank=True,
        help_text="Additional context about this comparison dimension"
    )
    points_of_agreement = models.TextField(
        blank=True,
        help_text="What schools agree on regarding this question"
    )
    key_divergence = models.TextField(
        blank=True,
        help_text="The main points of disagreement"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class SchoolPosition(models.Model):
    """A school's position on a comparison question"""
    question = models.ForeignKey(
        ComparisonQuestion,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    position_summary = models.CharField(
        max_length=300,
        help_text="Short summary for comparison tables"
    )
    detailed_position = models.TextField(
        blank=True,
        help_text="Longer explanation of this school's position"
    )
    critique_of_others = models.TextField(
        blank=True,
        help_text="This school's critique of other perspectives"
    )

    class Meta:
        unique_together = ['question', 'school']
        ordering = ['school__order']

    def __str__(self):
        return f"{self.school.name} on '{self.question.question}'"


class MaterialType(models.TextChoices):
    """Types of teaching materials"""
    LESSON_PLAN = 'lesson_plan', 'Lesson Plan'
    DISCUSSION = 'discussion', 'Discussion Questions'
    FLASHCARDS = 'flashcards', 'Flashcards'
    ASSESSMENT = 'assessment', 'Assessment'
    SLIDES = 'slides', 'Slides'
    INFOGRAPHIC = 'infographic', 'Infographic'


class TeachingMaterial(models.Model):
    """Downloadable teaching and learning resources"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    title = models.CharField(max_length=200)
    material_type = models.CharField(
        max_length=20,
        choices=MaterialType.choices
    )
    description = models.TextField(blank=True)
    content = models.TextField(
        help_text="Content in Markdown format (for web display)"
    )
    file = models.FileField(
        upload_to='materials/',
        blank=True,
        null=True,
        help_text="Optional downloadable file (PDF, etc.)"
    )
    tier = models.IntegerField(
        choices=ContentTier.choices,
        default=ContentTier.TIER_2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['material_type', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"


class AudioType(models.TextChoices):
    """Types of audio content"""
    OVERVIEW = 'overview', 'Overview'
    DEBATE = 'debate', 'Debate'
    LECTURE = 'lecture', 'Lecture'


class AudioContent(models.Model):
    """Pre-generated audio content (overviews, debates)"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='audio_content'
    )
    title = models.CharField(max_length=200)
    audio_type = models.CharField(
        max_length=20,
        choices=AudioType.choices
    )
    description = models.TextField(blank=True)
    script = models.TextField(
        help_text="The text script used to generate this audio"
    )
    audio_file = models.FileField(
        upload_to='audio/',
        blank=True,
        null=True,
        help_text="Generated audio file"
    )
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration in seconds"
    )
    tier = models.IntegerField(
        choices=ContentTier.choices,
        default=ContentTier.TIER_2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['audio_type', 'title']
        verbose_name_plural = "Audio content"

    def __str__(self):
        return f"{self.title} ({self.get_audio_type_display()})"

    @property
    def duration_display(self):
        """Return duration in mm:ss format"""
        if not self.duration_seconds:
            return None
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        return f"{minutes}:{seconds:02d}"
