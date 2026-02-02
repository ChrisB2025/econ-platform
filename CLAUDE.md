# Project: Pluralist Economics Teaching Platform

## Current Status

**Phase 3 (Technical Build) is COMPLETE. Fully deployed and operational on Railway.**

- **Repository**: https://github.com/ChrisB2025/econ-platform
- **Live URL**: https://web-production-0007.up.railway.app

### What's Working
- Topic hub with all 6 school explanations
- Comparison tool with school filtering
- AI chatbot (Claude API) with markdown rendering
- Audio content (2 episodes generated, ~22 minutes total)
- Teaching materials with download options
- Persistent PostgreSQL database
- Persistent volume for media/audio files

## Infrastructure

### Railway Services
- **web**: Django app with gunicorn
- **Postgres**: PostgreSQL database (persistent)
- **Volume**: Mounted at `/app/media` for audio files

### Key Fixes Applied
- `/health` endpoint exempt from SSL redirect for Railway healthchecks
- Flexbox layout for sidebar (was overlapping footer with float)
- Media file serving with Range request support (required for audio playback)
- Audio script cleaning removes metadata, stage directions, speaker labels
- Markdown rendering in chatbot via marked.js

## Core Documents

- `docs/PROJECT_BRIEF.md` — Full project specification
- `docs/DECISIONS.md` — Design decisions log
- `docs/DEPLOYMENT.md` — Railway deployment guide
- `docs/CURRENT_PHASE.md` — Phase status

## Quick Context

- **What this is**: Web-based economics teaching platform presenting topics through multiple schools of thought (neoclassical, post-Keynesian, MMT, Austrian, ecological, etc.)
- **MVP**: Inflation topic hub with per-school explanations, comparison tools, teaching chatbot, downloadable materials, audio content
- **Stack**: Django, PostgreSQL, Railway, Claude API, OpenAI TTS
- **Repository**: https://github.com/ChrisB2025/econ-platform

## Completed Work

### Phase 1: Research
All in `docs/research/` - Topic map, 6 school research docs, comparison framework, source materials

### Phase 2: Content
All in `docs/content/` - Introduction, 6 school explanations, comparisons, teaching materials, audio scripts, chatbot prompt

### Phase 3: Technical Build
- Django project with PostgreSQL support
- Database models: School, Topic, Explanation, ComparisonQuestion, SchoolPosition, TeachingMaterial, AudioContent
- Topic hub page with school navigation
- Comparison tool with school filtering
- AI chatbot (Claude API) with pluralist system prompt and markdown rendering
- TTS audio generation (OpenAI API) with script cleaning
- Materials download (Markdown/text formats)
- Railway deployment with PostgreSQL and persistent volume

## Key Commands

```bash
# Local development
python manage.py runserver

# Load/reload content
python manage.py load_inflation_content

# Full setup (runs on Railway deploy via startCommand)
python manage.py setup_platform

# Generate audio (requires OPENAI_API_KEY)
python manage.py generate_audio --dry-run
python manage.py generate_audio
python manage.py generate_audio --regenerate  # Force regenerate all

# Railway CLI commands
railway link --project econ-platform
railway service web
railway ssh --service web "cd /app && /opt/venv/bin/python manage.py <command>"
railway logs -n 50
railway deployment list
```

## Railway Environment Variables

Required:
- `SECRET_KEY` - Django secret key
- `DEBUG=False`
- `ALLOWED_HOSTS` - Railway domain
- `CSRF_TRUSTED_ORIGINS` - https://railway-domain
- `DATABASE_URL` - References `${{Postgres.DATABASE_URL}}`

Optional:
- `ANTHROPIC_API_KEY` - Enables AI chatbot
- `OPENAI_API_KEY` - Enables audio generation
- `DJANGO_SUPERUSER_*` - Auto-creates admin user

## Project Structure

```
├── pluralecon/          # Django project settings
├── topics/              # Main app (models, views, templates)
├── templates/           # HTML templates
├── static/              # CSS, JS
├── docs/                # Content source files
├── media/               # Audio files (on Railway volume)
├── railway.toml         # Railway deployment config
├── Procfile             # Web process definition
├── requirements.txt     # Python dependencies
└── runtime.txt          # Python version
```

## Key Principles

1. **Pluralism is genuine** — No school favored
2. **Steel-man before critique** — Present strongest form first
3. **Teaching, not advocacy** — Help understand, don't convert
4. **IB-level accessibility** — Ages 16-19, clear prose
5. **Honest about limitations** — Acknowledge uncertainty
