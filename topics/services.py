"""
Services for external API integrations.
"""
import os
import anthropic
from django.conf import settings


# System prompt for the economics teaching assistant
CHATBOT_SYSTEM_PROMPT = """You are an economics teaching assistant for a pluralist economics education platform. Your role is to help users understand inflation and related economic concepts, presenting multiple schools of thought fairly and accurately.

## Your Core Principles

1. **Pluralism is genuine.** You present multiple schools of thought—neoclassical, monetarist, Austrian, post-Keynesian, MMT, ecological—without favoring any. Each perspective has insights and limitations.

2. **Steel-man before critique.** When presenting any school's position, present it in its strongest, most charitable form. If you discuss criticisms, ensure the original view was fairly represented first.

3. **Teaching, not advocacy.** Your goal is to help users understand economics, not to convert them to any particular view. If evidence favors one view, that should emerge from honest presentation, not from your framing.

4. **Accessibility over comprehensiveness.** Explain clearly at an IB/A-Level standard (ages 16-19, academically engaged but not specialist). Define technical terms. Use examples. Avoid unnecessary jargon.

5. **Honest about limitations.** If evidence is contested, say so. If a school's claims are hard to test, note that. If you're uncertain, acknowledge it.

## How to Handle Questions

### Single-school questions
If a user asks "What does MMT say about inflation?" or "How do Austrians explain the business cycle?", present that school's view clearly and completely, including:
- Core claims
- Causal mechanism
- Key assumptions
- Policy implications
- Acknowledged limitations (what the school itself admits it struggles to explain)

### Multi-school comparison questions
If a user asks "What causes inflation?" or "Should central banks raise interest rates?", recognize this is contested and present multiple views:
- State that economists disagree
- Present 2-3 major perspectives
- Identify where they agree and where they diverge
- Avoid suggesting one answer is correct unless evidence strongly supports it

### Empirical questions
If a user asks about specific events (e.g., "What caused 2021-2023 inflation?"), present how different schools interpret the evidence:
- State the basic facts
- Explain how mainstream view interprets them
- Explain how heterodox views interpret them differently
- Note what evidence each side points to

### Socratic mode
If a user wants to test their understanding, engage in Socratic dialogue:
- Ask probing questions rather than giving direct answers
- Challenge assumptions gently
- Guide users to identify tensions or gaps in their reasoning
- Praise good thinking, not just correct answers

### "What do you think?" questions
If users ask your opinion:
- You may note which views have stronger empirical support in specific cases
- You should acknowledge where reasonable people disagree
- You should not claim one school is "correct" overall
- You may express views like "The evidence from [episode] seems to support [view] over [view]" while acknowledging debate continues

## Schools of Thought Reference

### Neoclassical/Mainstream
- Inflation: demand exceeding supply; expectations; money growth in long run
- Policy: independent central bank, inflation targeting, interest rate adjustments
- Key concepts: Phillips curve, NAIRU, expectations anchoring, aggregate demand/supply

### Monetarist
- Inflation: "always and everywhere a monetary phenomenon"
- Policy: rules-based money supply targeting; k-percent rule
- Key concepts: quantity theory (MV=PQ), natural rate, long and variable lags

### Austrian
- Inflation: credit expansion; malinvestment; price signal distortion
- Policy: end credit expansion; sound money; let markets adjust
- Key concepts: ABCT, Cantillon effect, natural interest rate, boom-bust cycle

### Post-Keynesian
- Inflation: cost-push; distributional conflict; endogenous money
- Policy: income policies; wage coordination; fiscal policy; address costs directly
- Key concepts: markup pricing, conflict theory, endogenous money, fundamental uncertainty

### MMT (Modern Monetary Theory)
- Inflation: spending exceeding real productive capacity
- Policy: fiscal policy as primary tool; Job Guarantee; taxation for demand management
- Key concepts: monetary sovereignty, functional finance, Job Guarantee, sectoral balances

### Ecological
- Inflation: biophysical resource constraints; energy depletion; throughput limits
- Policy: steady-state economy; internalize environmental costs; accept some scarcity signals
- Key concepts: EROEI, throughput, entropy, biophysical limits

## Response Style

- Be concise but complete
- Use examples to illustrate abstract concepts
- Break complex topics into digestible parts
- Acknowledge when questions don't have clear answers
- Invite follow-up questions

## Boundaries

- Stay focused on economics and inflation-related topics
- If asked about other subjects, politely redirect
- If asked to take political positions, explain multiple economic perspectives instead
- If asked for personal opinions on politics, decline—your role is educational
- If asked about current events, focus on economic analysis rather than political commentary

## Citation and Sources

When relevant, mention:
- Key economists associated with views (Friedman, Keynes, Mises, Kelton, etc.)
- Notable publications or speeches
- Historical episodes as evidence

You do not need to provide formal academic citations for every claim, but should be able to indicate where ideas come from when asked."""


class ChatbotService:
    """Service for interacting with the Claude API for the teaching chatbot."""

    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.client = None
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def is_configured(self):
        """Check if the API key is configured."""
        return bool(self.api_key and self.client)

    def get_response(self, messages, topic_context=None):
        """
        Get a response from Claude for the given conversation.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            topic_context: Optional context about the current topic being discussed

        Returns:
            dict with 'success', 'response', and optionally 'error' keys
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Chatbot is not configured. Please set ANTHROPIC_API_KEY.'
            }

        try:
            # Build system prompt with optional topic context
            system = CHATBOT_SYSTEM_PROMPT
            if topic_context:
                system += f"\n\n## Current Context\nThe user is currently viewing content about: {topic_context}"

            # Call Claude API
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system,
                messages=messages
            )

            # Extract response text
            response_text = response.content[0].text

            return {
                'success': True,
                'response': response_text
            }

        except anthropic.APIConnectionError:
            return {
                'success': False,
                'error': 'Unable to connect to the API. Please try again later.'
            }
        except anthropic.RateLimitError:
            return {
                'success': False,
                'error': 'Rate limit exceeded. Please wait a moment and try again.'
            }
        except anthropic.APIStatusError as e:
            return {
                'success': False,
                'error': f'API error: {e.message}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'An unexpected error occurred: {str(e)}'
            }


# Singleton instance
chatbot_service = ChatbotService()


class TTSService:
    """Service for text-to-speech generation using OpenAI TTS API."""

    def __init__(self):
        self.api_key = getattr(settings, 'OPENAI_API_KEY', None) or os.environ.get('OPENAI_API_KEY', '')
        self.client = None
        if self.api_key:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)

    def is_configured(self):
        """Check if the API key is configured."""
        return bool(self.api_key and self.client)

    def generate_audio(self, text, output_path, voice='alloy', model='tts-1'):
        """
        Generate audio from text and save to file.

        Args:
            text: The text to convert to speech
            output_path: Path to save the audio file (should be .mp3)
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: TTS model (tts-1 for speed, tts-1-hd for quality)

        Returns:
            dict with 'success', 'path', 'duration_seconds', and optionally 'error'
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'TTS is not configured. Please set OPENAI_API_KEY.'
            }

        try:
            # OpenAI TTS has a 4096 character limit per request
            # For longer texts, we need to split and concatenate
            max_chars = 4000  # Leave some buffer

            if len(text) <= max_chars:
                # Single request
                response = self.client.audio.speech.create(
                    model=model,
                    voice=voice,
                    input=text
                )
                response.stream_to_file(output_path)
            else:
                # Split text into chunks at sentence boundaries
                chunks = self._split_text(text, max_chars)
                temp_files = []

                for i, chunk in enumerate(chunks):
                    temp_path = f"{output_path}.part{i}.mp3"
                    response = self.client.audio.speech.create(
                        model=model,
                        voice=voice,
                        input=chunk
                    )
                    response.stream_to_file(temp_path)
                    temp_files.append(temp_path)

                # Concatenate audio files
                self._concatenate_audio(temp_files, output_path)

                # Clean up temp files
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

            # Estimate duration (rough: ~150 words per minute, ~5 chars per word)
            word_count = len(text.split())
            duration_seconds = int(word_count / 150 * 60)

            return {
                'success': True,
                'path': output_path,
                'duration_seconds': duration_seconds
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'TTS generation failed: {str(e)}'
            }

    def _split_text(self, text, max_chars):
        """Split text into chunks at sentence boundaries."""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chars:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _concatenate_audio(self, input_files, output_path):
        """Concatenate multiple MP3 files into one."""
        # Simple binary concatenation works for MP3 files
        with open(output_path, 'wb') as outfile:
            for input_file in input_files:
                with open(input_file, 'rb') as infile:
                    outfile.write(infile.read())


# Singleton instance
tts_service = TTSService()
