"""
Management command to generate audio files from audio content scripts.

Usage:
    python manage.py generate_audio                    # Generate all pending
    python manage.py generate_audio --id 1             # Generate specific audio
    python manage.py generate_audio --regenerate       # Regenerate all
    python manage.py generate_audio --voice nova       # Use specific voice
"""
import os
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from topics.models import AudioContent
from topics.services import tts_service


class Command(BaseCommand):
    help = 'Generate audio files from audio content scripts using TTS'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            type=int,
            help='Generate audio for a specific AudioContent ID'
        )
        parser.add_argument(
            '--regenerate',
            action='store_true',
            help='Regenerate audio even if file already exists'
        )
        parser.add_argument(
            '--voice',
            type=str,
            default='nova',
            choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'],
            help='Voice to use for TTS (default: nova)'
        )
        parser.add_argument(
            '--model',
            type=str,
            default='tts-1-hd',
            choices=['tts-1', 'tts-1-hd'],
            help='TTS model (tts-1 for speed, tts-1-hd for quality)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be generated without actually generating'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if not tts_service.is_configured() and not dry_run:
            raise CommandError(
                'TTS service is not configured. Please set OPENAI_API_KEY in your environment.\n'
                'Use --dry-run to preview what would be generated.'
            )

        # Ensure media/audio directory exists
        audio_dir = Path(settings.MEDIA_ROOT) / 'audio'
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Get audio content to process
        if options['id']:
            try:
                audio_items = [AudioContent.objects.get(id=options['id'])]
            except AudioContent.DoesNotExist:
                raise CommandError(f'AudioContent with ID {options["id"]} not found')
        else:
            audio_items = AudioContent.objects.all()

        if not audio_items:
            self.stdout.write('No audio content found.')
            return

        voice = options['voice']
        model = options['model']
        regenerate = options['regenerate']
        dry_run = options['dry_run']

        self.stdout.write(f'Found {len(audio_items)} audio content item(s)')
        self.stdout.write(f'Voice: {voice}, Model: {model}')
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - no files will be generated'))
        self.stdout.write('')

        generated = 0
        skipped = 0
        failed = 0

        for audio in audio_items:
            # Check if audio file already exists
            if audio.audio_file and not regenerate:
                file_path = Path(settings.MEDIA_ROOT) / audio.audio_file.name
                if file_path.exists():
                    self.stdout.write(f'  Skipping: {audio.title} (file exists)')
                    skipped += 1
                    continue

            self.stdout.write(f'  Processing: {audio.title}')

            # Clean the script text for TTS
            script_text = self._clean_script(audio.script)

            if not script_text:
                self.stdout.write(self.style.WARNING(f'    No usable text in script'))
                failed += 1
                continue

            self.stdout.write(f'    Script length: {len(script_text)} characters')

            if dry_run:
                self.stdout.write(self.style.SUCCESS(f'    Would generate audio'))
                generated += 1
                continue

            # Generate filename
            filename = f'{audio.topic.slug}_{audio.audio_type}_{audio.id}.mp3'
            output_path = audio_dir / filename

            # Generate audio
            self.stdout.write(f'    Generating audio...')
            result = tts_service.generate_audio(
                text=script_text,
                output_path=str(output_path),
                voice=voice,
                model=model
            )

            if result['success']:
                # Update the model
                audio.audio_file = f'audio/{filename}'
                audio.duration_seconds = result.get('duration_seconds')
                audio.save()

                self.stdout.write(self.style.SUCCESS(
                    f'    Generated: {filename} (~{audio.duration_display})'
                ))
                generated += 1
            else:
                self.stdout.write(self.style.ERROR(
                    f'    Failed: {result["error"]}'
                ))
                failed += 1

        self.stdout.write('')
        self.stdout.write(f'Summary: {generated} generated, {skipped} skipped, {failed} failed')

    def _clean_script(self, script):
        """
        Clean markdown script for TTS.
        Remove markdown formatting, headers, stage directions, and metadata.
        Only process content between '## Script' and '## Production Notes'.
        """
        import re

        if not script:
            return ''

        lines = script.split('\n')
        cleaned_lines = []

        # Track whether we're in the script section
        in_script_section = False

        for line in lines:
            # Start processing at '## Script'
            if line.strip() == '## Script':
                in_script_section = True
                continue

            # Stop processing at '## Production Notes' or similar end sections
            if line.strip().startswith('## Production') or line.strip().startswith('## Notes'):
                in_script_section = False
                continue

            # Skip lines until we reach the script section
            if not in_script_section:
                continue

            # Skip markdown headers
            if line.startswith('#'):
                continue

            # Skip code blocks
            if line.startswith('```'):
                continue

            # Skip horizontal rules
            if line.strip() in ['---', '***', '___']:
                continue

            # Skip lines that are just formatting
            if re.match(r'^[\*\-_\s]+$', line):
                continue

            # Skip metadata lines (bullet points with bold labels)
            if re.match(r'^-\s*\*\*\w+:\*\*', line):
                continue

            # Remove markdown bold/italic
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            line = re.sub(r'\*(.+?)\*', r'\1', line)
            line = re.sub(r'__(.+?)__', r'\1', line)
            line = re.sub(r'_(.+?)_', r'\1', line)

            # Remove markdown links but keep text
            line = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', line)

            # Remove stage directions in brackets (common in scripts)
            line = re.sub(r'\[.+?\]', '', line)

            # Skip speaker labels (e.g., "NARRATOR:", "HOST:", "GUEST 1:")
            if re.match(r'^[A-Z][A-Z\s\d]*:\s*$', line.strip()):
                continue

            # Clean up multiple spaces
            line = re.sub(r'\s+', ' ', line).strip()

            if line:
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)
