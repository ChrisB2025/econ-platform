"""
Management command to load Inflation topic content from markdown files.

Usage: python manage.py load_inflation_content
"""
from pathlib import Path
from django.core.management.base import BaseCommand
from topics.models import (
    School, Topic, Explanation, ComparisonQuestion,
    SchoolPosition, TeachingMaterial, AudioContent,
    ContentTier, MaterialType, AudioType
)


class Command(BaseCommand):
    help = 'Load Inflation topic content from docs/content/ markdown files'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.content_dir = self.base_dir / 'docs' / 'content'

    def handle(self, *args, **options):
        self.stdout.write('Loading Inflation topic content...')

        # Load introduction and create/update topic
        topic = self.load_topic()

        # Load school explanations
        self.load_explanations(topic)

        # Load comparisons
        self.load_comparisons(topic)

        # Load teaching materials
        self.load_teaching_materials(topic)

        # Load audio scripts
        self.load_audio_content(topic)

        self.stdout.write(self.style.SUCCESS('Successfully loaded all content!'))

    def read_file(self, path):
        """Read a markdown file and return its content."""
        full_path = self.content_dir / path
        if full_path.exists():
            return full_path.read_text(encoding='utf-8')
        self.stdout.write(self.style.WARNING(f'File not found: {full_path}'))
        return ''

    def load_topic(self):
        """Create or update the Inflation topic."""
        intro_content = self.read_file('00-introduction.md')

        topic, created = Topic.objects.update_or_create(
            slug='inflation',
            defaults={
                'name': 'Inflation',
                'introduction': intro_content,
                'tier': ContentTier.TIER_2,
                'is_published': True,
            }
        )

        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  {action} topic: {topic.name}')
        return topic

    def load_explanations(self, topic):
        """Load school explanations from markdown files."""
        school_files = {
            'neoclassical': '01-neoclassical.md',
            'monetarist': '02-monetarist.md',
            'austrian': '03-austrian.md',
            'post-keynesian': '04-post-keynesian.md',
            'mmt': '05-mmt.md',
            'ecological': '06-ecological.md',
        }

        for slug, filename in school_files.items():
            content = self.read_file(filename)
            if not content:
                continue

            try:
                school = School.objects.get(slug=slug)
            except School.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  School not found: {slug}'))
                continue

            # Extract title from first line
            lines = content.split('\n')
            title = lines[0].lstrip('# ').strip() if lines else f'{school.name} View'

            explanation, created = Explanation.objects.update_or_create(
                topic=topic,
                school=school,
                defaults={
                    'title': title,
                    'content': content,
                    'tier': ContentTier.TIER_2,
                }
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} explanation: {school.name}')

    def load_comparisons(self, topic):
        """Load comparison questions and positions from the comparisons file."""
        content = self.read_file('07-comparisons.md')
        if not content:
            return

        # Parse the comparisons - this is simplified; in production you'd want
        # a more robust parser
        comparison_data = [
            {
                'question': 'What Causes Inflation?',
                'order': 1,
                'positions': {
                    'neoclassical': 'Demand exceeding supply; expectations becoming unanchored',
                    'monetarist': 'Money supply growing faster than output',
                    'austrian': 'Credit expansion distorting interest rates and price signals',
                    'post-keynesian': 'Cost pressures and distributional conflict',
                    'mmt': 'Spending exceeding the economy\'s real productive capacity',
                    'ecological': 'Biophysical resource constraints and depletion',
                }
            },
            {
                'question': 'How Should Inflation Be Controlled?',
                'order': 2,
                'positions': {
                    'neoclassical': 'Independent central bank adjusting interest rates',
                    'monetarist': 'Rules-based money supply targeting',
                    'austrian': 'End credit expansion; let markets adjust',
                    'post-keynesian': 'Income policies, wage coordination, industrial policy',
                    'mmt': 'Fiscal policy and taxation; Job Guarantee as wage anchor',
                    'ecological': 'Accept some inflation as real scarcity; transition to steady-state',
                }
            },
            {
                'question': 'The Phillips Curve and NAIRU',
                'order': 3,
                'positions': {
                    'neoclassical': 'Short-run trade-off exists; long-run curve is vertical at NAIRU',
                    'monetarist': 'Natural rate determined by real factors, not monetary policy',
                    'austrian': 'Reject aggregates; focus on capital structure',
                    'post-keynesian': 'NAIRU is a myth; full employment is compatible with price stability',
                    'mmt': 'NAIRU is a policy choice, not a natural constraint',
                    'ecological': 'Secondary concern compared to biophysical constraints',
                }
            },
            {
                'question': 'The Money Supply Question',
                'order': 4,
                'positions': {
                    'neoclassical': 'Mixed—central bank sets rates, which influence credit creation',
                    'monetarist': 'Primarily exogenous—central bank controls money supply',
                    'austrian': 'Focus on credit, which is expanded through banking system',
                    'post-keynesian': 'Endogenous—loans create deposits; money supply responds to demand',
                    'mmt': 'Endogenous—created by government spending and bank lending',
                    'ecological': 'Money questions are secondary to real resource flows',
                }
            },
            {
                'question': 'The 2021-2023 Inflation Episode',
                'order': 5,
                'positions': {
                    'neoclassical': 'Demand recovered faster than supply; some fiscal stimulus excess',
                    'monetarist': 'Massive money creation during COVID (stimulus, QE)',
                    'austrian': 'Years of easy credit created fragility; pandemic revealed malinvestments',
                    'post-keynesian': 'Supply disruptions + profit-push as firms raised markups',
                    'mmt': 'Supply-side shock (COVID, shipping, energy) hitting real capacity',
                    'ecological': 'Energy constraints exposed real limits',
                }
            },
            {
                'question': 'Hyperinflation',
                'order': 6,
                'positions': {
                    'neoclassical': 'Fiscal dominance; money financing of unsustainable deficits',
                    'monetarist': 'Extreme money supply growth from government printing',
                    'austrian': 'Flight from currency as monetary debasement becomes obvious',
                    'post-keynesian': 'Collapse of productive capacity; foreign debt; political breakdown',
                    'mmt': 'Loss of real productive capacity, typically with foreign currency debt',
                    'ecological': 'Collapse of resource base manifesting as monetary breakdown',
                }
            },
            {
                'question': 'The Role of Central Banks',
                'order': 7,
                'positions': {
                    'neoclassical': 'Essential for price stability; independence crucial',
                    'monetarist': 'Useful if following rules; dangerous with discretion',
                    'austrian': 'The problem, not the solution; abolish if possible',
                    'post-keynesian': 'Overrated; may serve class interests; need democratic accountability',
                    'mmt': 'Should coordinate with fiscal policy; independence is mostly theater',
                    'ecological': 'Secondary concern compared to real physical constraints',
                }
            },
        ]

        for comp_data in comparison_data:
            question, created = ComparisonQuestion.objects.update_or_create(
                topic=topic,
                question=comp_data['question'],
                defaults={'order': comp_data['order']}
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} comparison: {comp_data["question"]}')

            for school_slug, position_text in comp_data['positions'].items():
                try:
                    school = School.objects.get(slug=school_slug)
                    SchoolPosition.objects.update_or_create(
                        question=question,
                        school=school,
                        defaults={'position_summary': position_text}
                    )
                except School.DoesNotExist:
                    pass

    def load_teaching_materials(self, topic):
        """Load teaching materials from markdown files."""
        materials = [
            ('teaching-materials/lesson-plan.md', 'Inflation Lesson Plan', MaterialType.LESSON_PLAN),
            ('teaching-materials/discussion-questions.md', 'Discussion Questions', MaterialType.DISCUSSION),
            ('teaching-materials/flashcards.md', 'Flashcards', MaterialType.FLASHCARDS),
            ('teaching-materials/assessment.md', 'Assessment', MaterialType.ASSESSMENT),
        ]

        for filename, title, material_type in materials:
            content = self.read_file(filename)
            if not content:
                continue

            material, created = TeachingMaterial.objects.update_or_create(
                topic=topic,
                title=title,
                defaults={
                    'material_type': material_type,
                    'content': content,
                    'tier': ContentTier.TIER_2,
                }
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} material: {title}')

    def load_audio_content(self, topic):
        """Load audio scripts from markdown files."""
        audio_files = [
            ('audio-scripts/overview-inflation-intro.md', 'Introduction to Inflation', AudioType.OVERVIEW, 600),
            ('audio-scripts/debate-what-causes-inflation.md', 'What Causes Inflation? A Debate', AudioType.DEBATE, 900),
        ]

        for filename, title, audio_type, est_duration in audio_files:
            script = self.read_file(filename)
            if not script:
                continue

            audio, created = AudioContent.objects.update_or_create(
                topic=topic,
                title=title,
                defaults={
                    'audio_type': audio_type,
                    'script': script,
                    'duration_seconds': est_duration,
                    'tier': ContentTier.TIER_2,
                }
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} audio: {title}')
