# Project: Pluralist Economics Teaching Platform

## Current Status

**Phase 1 (Research) and Phase 2 (Content Writing) are COMPLETE.**

**Phase 3 (Technical Build) is READY TO START.**

Next step: Set up Django project with virtual environment and begin building the platform.

## Core Documents

Read these files before starting any work on this project:

- `docs/PROJECT_BRIEF.md` — Full project specification, editorial principles, content architecture, technical stack, and MVP scope (inflation module)
- `docs/DECISIONS.md` — Running log of design decisions and their rationale
- `docs/CURRENT_PHASE.md` — What is currently being worked on and immediate next steps

Do not deviate from the principles, scope, or architectural decisions defined in these documents without explicit instruction from the user.

## Quick Context

- **What this is**: A web-based economics teaching platform presenting topics through multiple schools of thought (neoclassical, post-Keynesian, MMT, Austrian, ecological, etc.) with genuine pluralism and no ideological bias
- **MVP**: A single topic hub on inflation with per-school explanations, comparison tools, a teaching chatbot, downloadable materials, and pre-generated audio content
- **Stack**: Django, PostgreSQL, Railway, Claude API, TTS API for audio
- **Builder**: Solo amateur developer using Claude as coding assistant, no budget beyond bootstrapping costs
- **Content tiers**: (1) Approved reference material, (2) AI-assisted but reviewed platform content, (3) Fully generative on-demand content — each carrying a visible provenance label

## Completed Work

### Phase 1: Research Documents
All in `docs/research/`:
- Topic map, 6 school research docs, comparison framework, source materials

### Phase 2: Content Documents
All in `docs/content/`:
- Introduction + 6 school explanations (Tier 2 platform content)
- Structured comparisons document
- Teaching materials: lesson plan, 30 discussion questions, 40 flashcards, assessment
- Audio scripts: intro overview (~10 min), debate episode (~15 min)
- Chatbot system prompt

## Phase 3: Technical Build (Next)

To be implemented:
1. Set up Django project with virtual environment
2. Create database models for content (topics, schools, explanations, comparisons)
3. Build topic hub page with school-of-thought navigation
4. Build comparison tool (select 2+ schools, see structured comparison)
5. Integrate AI chatbot (Claude API with system prompt from `docs/content/chatbot-system-prompt.md`)
6. Generate audio from scripts (TTS API)
7. Build materials download section
8. Deploy to Railway

## Key Principles (Always Follow)

1. **Pluralism is genuine** — No school of thought favored in tone, depth, or framing
2. **Steel-man before critique** — Present each view in strongest form first
3. **Teaching, not advocacy** — Help users understand, don't convert them
4. **IB-level accessibility** — Clear prose for ages 16-19, define jargon
5. **Honest about limitations** — Acknowledge contested evidence and uncertainty
