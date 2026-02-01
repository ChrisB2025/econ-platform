# Deployment Guide: Railway

This guide covers deploying the Pluralist Economics Platform to Railway.

## Prerequisites

- A Railway account (https://railway.app)
- A GitHub repository with your code (recommended)
- API keys for AI features (optional but recommended):
  - Anthropic API key for the teaching chatbot
  - OpenAI API key for audio generation

## Deployment Steps

### 1. Create Railway Project

1. Log in to Railway
2. Click "New Project"
3. Choose "Deploy from GitHub repo" (recommended) or "Empty Project"

### 2. Add PostgreSQL Database

1. In your project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically set `DATABASE_URL`

### 3. Configure Environment Variables

In your Railway service, go to "Variables" and add:

**Required:**
```
SECRET_KEY=<generate a secure random string>
DEBUG=False
ALLOWED_HOSTS=<your-app>.up.railway.app
CSRF_TRUSTED_ORIGINS=https://<your-app>.up.railway.app
```

**For AI Features (optional but recommended):**
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

**For Auto Admin Creation (optional):**
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=<secure-password>
```

### 4. Deploy

If using GitHub:
- Push to your connected branch
- Railway will automatically deploy

If deploying directly:
- Use Railway CLI: `railway up`

### 5. Verify Deployment

1. Check the deployment logs for successful setup
2. Visit your Railway URL
3. Verify the Inflation topic loads correctly
4. Test the comparison tool and materials

## What Happens Automatically

The `release` command in the Procfile runs `setup_platform` which:

1. ✅ Runs all database migrations
2. ✅ Loads the 6 schools of thought
3. ✅ Loads all Inflation topic content:
   - Introduction
   - 6 school explanations
   - 7 comparison questions with positions
   - 4 teaching materials
   - 2 audio scripts
4. ✅ Collects static files
5. ✅ Creates superuser (if env vars set)

## Generating Audio Content

Audio files must be generated separately (they're too large to include in the repo).

**Option 1: Generate locally and upload**
```bash
# Set your OpenAI key locally
export OPENAI_API_KEY=sk-...

# Generate audio
python manage.py generate_audio

# Audio files will be in media/audio/
# Upload these to Railway's volume or a file storage service
```

**Option 2: Use Railway's one-off commands (if available)**
```bash
railway run python manage.py generate_audio
```

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key (generate a long random string) |
| `DEBUG` | Yes | Set to `False` for production |
| `DATABASE_URL` | Auto | Provided by Railway PostgreSQL |
| `ALLOWED_HOSTS` | Yes | Your Railway domain |
| `CSRF_TRUSTED_ORIGINS` | Yes | Full URL with https:// |
| `ANTHROPIC_API_KEY` | No | Enables AI chatbot |
| `OPENAI_API_KEY` | No | Enables audio generation |
| `DJANGO_SUPERUSER_*` | No | Auto-creates admin user |

## Troubleshooting

### "CSRF verification failed"
- Ensure `CSRF_TRUSTED_ORIGINS` includes `https://` prefix
- Check that the domain matches exactly

### "Server Error (500)"
- Check Railway logs for details
- Ensure all required environment variables are set
- Verify DATABASE_URL is correctly configured

### "Static files not loading"
- The release command should run `collectstatic`
- Check that WhiteNoise is properly configured

### "Chatbot not working"
- Verify `ANTHROPIC_API_KEY` is set
- Check `/api/chat/status/` endpoint returns `{"configured": true}`

## Generating a Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use any secure random string generator (50+ characters).

## File Structure for Deployment

```
├── Procfile              # Defines web and release commands
├── railway.toml          # Railway-specific configuration
├── runtime.txt           # Python version
├── requirements.txt      # Python dependencies
├── manage.py
├── pluralecon/           # Django project
├── topics/               # Main app
├── templates/
├── static/
└── docs/                 # Content source files
```
