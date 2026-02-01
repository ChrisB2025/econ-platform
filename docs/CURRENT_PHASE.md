# Current Phase: Ready for Technical Build

## Status

**Phase 1 (Research) and Phase 2 (Content Writing) are complete.**

**Phase 3 (Technical Build) is ready to begin.**

Next action: Set up Django project with virtual environment, then build the platform.

---

## Completed Work

### Phase 1: Research (Complete)

| File | Description |
|------|-------------|
| `docs/research/00-topic-map.md` | Sub-questions structuring the module |
| `docs/research/01-neoclassical.md` | Neoclassical/mainstream research |
| `docs/research/02-monetarist.md` | Monetarist research |
| `docs/research/03-austrian.md` | Austrian research |
| `docs/research/04-post-keynesian.md` | Post-Keynesian research |
| `docs/research/05-mmt.md` | MMT research |
| `docs/research/06-ecological.md` | Ecological economics research |
| `docs/research/07-comparison-framework.md` | Dimensions for comparing schools |
| `docs/research/08-source-materials.md` | Bibliography and references |

### Phase 2: Content Writing (Complete)

| File | Description |
|------|-------------|
| `docs/content/00-introduction.md` | Neutral introduction to inflation |
| `docs/content/01-neoclassical.md` | Neoclassical explanation (Tier 2) |
| `docs/content/02-monetarist.md` | Monetarist explanation (Tier 2) |
| `docs/content/03-austrian.md` | Austrian explanation (Tier 2) |
| `docs/content/04-post-keynesian.md` | Post-Keynesian explanation (Tier 2) |
| `docs/content/05-mmt.md` | MMT explanation (Tier 2) |
| `docs/content/06-ecological.md` | Ecological explanation (Tier 2) |
| `docs/content/07-comparisons.md` | Structured school comparisons |
| `docs/content/teaching-materials/lesson-plan.md` | 4-lesson teaching plan |
| `docs/content/teaching-materials/discussion-questions.md` | 30 discussion questions |
| `docs/content/teaching-materials/flashcards.md` | 40 flashcards |
| `docs/content/teaching-materials/assessment.md` | MCQs, short answer, essays |
| `docs/content/audio-scripts/overview-inflation-intro.md` | 10-min intro audio script |
| `docs/content/audio-scripts/debate-what-causes-inflation.md` | 15-min debate audio script |
| `docs/content/chatbot-system-prompt.md` | AI teaching assistant configuration |

---

## Content Summary

### Platform Content (Tier 2)
- **Introduction**: 3 paragraphs, neutral, sets up pluralist framing
- **School explanations**: 6 documents, ~1500-2000 words each, accessible IB-level writing
- **Comparisons**: 7 structured comparison topics with tables and analysis

### Teaching Materials
- **Lesson plan**: 4 class periods covering definitions, theories, heterodox views, case study
- **Discussion questions**: 30 questions across foundational, policy, historical, and big-picture categories
- **Flashcards**: 40 cards covering definitions, schools, concepts, quotes
- **Assessment**: 13 MCQs, 3 short-answer questions, 3 essay prompts, 1 data analysis question

### Audio Content
- **Overview episode**: ~10 minutes introducing inflation and why economists disagree
- **Debate episode**: ~15 minutes with three voices (mainstream, post-Keynesian, MMT) debating causes and policy

### Chatbot
- **System prompt**: Defines pluralist tone, response patterns, school reference guide, boundaries

---

## Next Steps: Phase 3 Technical Build

1. **Set up Django project** - Create virtual environment, install Django, initialize project
2. **Create database models** - Topics, schools, explanations, comparisons, materials
3. **Build topic hub page** - School-of-thought navigation with tab/card UI
4. **Build comparison tool** - Select 2+ schools, display structured comparison
5. **Integrate AI chatbot** - Claude API with system prompt from `chatbot-system-prompt.md`
6. **Generate audio** - Use TTS API to create audio from scripts
7. **Build materials section** - Downloadable lesson plans, flashcards, assessments
8. **Deploy to Railway** - PostgreSQL database, production configuration

---

## File Structure

```
docs/
├── PROJECT_BRIEF.md
├── DECISIONS.md
├── CURRENT_PHASE.md
├── research/
│   ├── 00-topic-map.md
│   ├── 01-neoclassical.md
│   ├── 02-monetarist.md
│   ├── 03-austrian.md
│   ├── 04-post-keynesian.md
│   ├── 05-mmt.md
│   ├── 06-ecological.md
│   ├── 07-comparison-framework.md
│   └── 08-source-materials.md
└── content/
    ├── 00-introduction.md
    ├── 01-neoclassical.md
    ├── 02-monetarist.md
    ├── 03-austrian.md
    ├── 04-post-keynesian.md
    ├── 05-mmt.md
    ├── 06-ecological.md
    ├── 07-comparisons.md
    ├── chatbot-system-prompt.md
    ├── teaching-materials/
    │   ├── lesson-plan.md
    │   ├── discussion-questions.md
    │   ├── flashcards.md
    │   └── assessment.md
    └── audio-scripts/
        ├── overview-inflation-intro.md
        └── debate-what-causes-inflation.md
```
