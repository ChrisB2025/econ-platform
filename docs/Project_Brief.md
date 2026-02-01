# Project Prompt: Pluralist Economics Teaching Platform

## Project Overview

Build a web-based teaching platform that presents economics topics through the lenses of multiple schools of economic thought. For each topic, the platform surfaces the explanations offered by different traditions (neoclassical, Austrian, post-Keynesian, MMT, ecological economics, and others), identifies the strengths and weaknesses of each, and lets the user draw their own conclusions.

The platform serves three audiences from a single content architecture: teachers constrained by formal curricula (IB, IGCSE, AP), self-directed learners with no curricular obligations, and professionals in organizations (unions, advocacy groups, policy shops) who need economics literacy tied to real-world problems.

The editorial voice is neutral and institutional. No school of thought is presented as the correct answer. Instead, each perspective is subjected to consistent critical scrutiny, including the heterodox alternatives. The expectation is that this honest, even-handed treatment will itself reveal which frameworks hold up better under pressure, without the platform needing to make that case explicitly.

---

## MVP Scope

### Topic: Inflation

The MVP is a single topic module on **inflation**. This topic was chosen because:

- The orthodox/heterodox divide is sharp and well-documented (monetarist quantity theory vs. cost-push/conflict theory vs. MMT's fiscal and capacity-constraint lens vs. Austrian credit-expansion theory).
- It is viscerally relevant to all three target audiences.
- It connects naturally to adjacent topics (money, employment, interest rates, fiscal policy), which will reveal how modules should eventually link together.

The MVP does not require user accounts, progress tracking, or curriculum tagging. Those features come later once multiple modules exist.

### What the MVP Delivers

A "topic hub" page for inflation that allows a user to:

1. **Explore inflation through the lens of a specific school of thought.** For example, select "Neoclassical" and read their explanation, or select "MMT" and read theirs. Each perspective is presented with its core claims, key assumptions, supporting evidence, acknowledged limitations, and relevant citations.

2. **Compare and contrast perspectives.** Select two or more schools and see a structured comparison: where they agree, where they diverge, what each fails to explain, and how they respond to each other's critiques.

3. **Access generated teaching and learning materials.** These include downloadable lesson notes, discussion questions, flashcards, infographics, and (where pre-generated) audio overviews in the style of Google NotebookLM.

4. **Interact with an AI teaching assistant.** A chatbot that can answer questions about inflation from any or all perspectives, pose Socratic questions to test understanding, and provide citations and quotes from relevant academic sources.

---

## Content Architecture

### Topic Hub Structure

Each topic hub has **inputs** and **outputs**.

**Inputs** (the raw intellectual material):
- Core concepts and definitions from each school of thought
- Key assumptions and logical framework
- Supporting evidence and empirical claims
- Relevant academic references, quotes, and source materials
- Diagrams and models specific to each perspective
- Known weaknesses, gaps, and internal critiques
- Points of conflict with other schools

**Outputs** (what users consume):
- Written explanations by school of thought (browsable via tabs or navigation)
- Structured comparison views (side-by-side or sequential)
- Pre-generated audio overviews (NotebookLM-style, created once and stored)
- Pre-generated audio debates between perspectives (created once and stored)
- Downloadable materials: lesson plans, slides, flashcards, infographics, discussion guides, assessments
- AI chatbot for dynamic Q&A and Socratic teaching
- Shareable links to specific sections (for viral/peer-to-peer distribution)

### Content Tiers

All content falls into one of three tiers, each carrying a visible designation so users understand its provenance:

**Tier 1: Approved Reference Content**
Static, curated material. Includes chunked and embedded academic papers, book excerpts, and key quotes from established sources. This content is stored as files and presented verbatim. It must be accurately represented, properly attributed, and faithful to the original source.

**Tier 2: Resource-Informed Platform Content**
Written explanations, lesson notes, and structured comparisons generated with AI assistance but reviewed and approved before publication. These form the stable "spine" of each topic hub. They draw on the Tier 1 knowledge base but are presented in the platform's own voice at an IB-appropriate reading level.

**Tier 3: Generative On-Demand Content**
AI-generated outputs that cannot be pre-approved: chatbot responses, Socratic dialogues, custom material generation. These are produced dynamically per user request. Where possible (audio overviews, standard debate scripts), generate once and cache rather than regenerating per request.

---

## Schools of Thought to Cover (for Inflation MVP)

At minimum, the inflation module should present these perspectives:

1. **Neoclassical/Mainstream** - Quantity theory of money, expectations-augmented Phillips curve, central bank inflation targeting, NAIRU
2. **Monetarist** - Friedman's "inflation is always and everywhere a monetary phenomenon," money supply growth as causal mechanism
3. **Austrian** - Credit expansion through fractional reserve banking, malinvestment, distortion of price signals
4. **Post-Keynesian** - Cost-push theory, markup pricing, conflict theory of inflation (wages vs. profits), endogenous money
5. **MMT (Modern Monetary Theory)** - Inflation as evidence of spending beyond real resource capacity, functional finance, the role of taxation as a demand drain rather than a funding mechanism
6. **Ecological Economics** - Biophysical constraints on growth, resource depletion as inflationary pressure, throughput limits

Not every school needs equal depth in the MVP. Neoclassical, post-Keynesian, and MMT should receive the fullest treatment, as the contrasts between them are the most instructive and well-documented.

---

## Technical Specification

### Stack

- **Backend**: Django (Python), hosted on Railway
- **Frontend**: Django templates for the MVP; more interactive framework (React or similar) considered for later phases
- **AI/LLM**: Claude API for the teaching chatbot (Tier 2 and 3 content generation)
- **Audio**: Text-to-speech API (ElevenLabs, OpenAI TTS, or Google Cloud TTS) for generating audio overviews and debates; generated once and stored as static audio files
- **Database**: PostgreSQL (Railway default) for content metadata, topic structure, and cached generated content
- **File storage**: S3-compatible storage (or Railway equivalent) for PDFs, audio files, and static assets

### Key Technical Decisions

1. **Not a pure RAG system.** The platform prioritizes accurate synthesis and effective teaching over exhaustive source tracing. The LLM should be well-prompted with economics knowledge and supplemented by a curated knowledge base of key texts, not dependent on retrieval from a comprehensive database of all economics literature.

2. **Citation as a feature, not a constraint.** The chatbot and Tier 2 content should provide citations and quotes from relevant academic work where they strengthen the explanation. But the system should not refuse to explain a concept simply because it lacks a specific source document. The goal is a teaching assistant, not a research assistant.

3. **Generate-once audio.** Audio content (overviews, debates) should be generated from Tier 2 written content, reviewed, and stored as static files. Users do not generate new audio on demand. This controls costs and quality.

4. **No user accounts in MVP.** The topic hub is publicly accessible. User accounts, progress tracking, and personalized learning paths are Phase 2 features.

---

## User Experience (MVP)

### Entry Points

Users arrive at the inflation topic hub through different paths:
- Direct link shared by a peer ("read this on inflation")
- Search engine query landing on the topic page
- Navigation from the platform's topic index (when multiple modules exist)
- Social media post linking to a specific comparison or insight

### Core Navigation

The topic hub page presents:

1. **A brief, neutral introduction** to inflation as a concept (2-3 paragraphs, Tier 2 content)
2. **School-of-thought navigation** allowing the user to select any covered perspective and read its full explanation of inflation
3. **A comparison tool** allowing the user to select two or more schools and see a structured analysis of agreements, divergences, and mutual critiques
4. **A materials section** with downloadable resources (lesson plans, slides, flashcards, discussion questions, assessments)
5. **An audio section** with pre-generated overview episodes and inter-school debate episodes
6. **A chatbot** for asking questions, testing understanding via Socratic dialogue, and requesting explanations at different levels of detail

### Tone and Reading Level

- Target: IB Economics level (ages 16-19, academically engaged but not specialist)
- Clear, direct prose. Avoid jargon where possible; define it where necessary.
- Each school's explanation should be presented in its strongest form before weaknesses are identified. Steel-man first, then critique.
- Critiques should be specific and substantive, not dismissive. "This model assumes X, which empirical evidence from Y suggests does not hold" rather than "this model is wrong."

---

## Content Development Process (for the Inflation MVP)

### Phase 1: Research

Before any code is written, produce a structured content outline for the inflation module:

1. **Map the topic.** What are the sub-questions within inflation? (What causes it? How is it measured? What controls it? What are its effects? What is the relationship between inflation and employment? Between inflation and money supply? Between inflation and fiscal policy?)

2. **For each sub-question, document what each school of thought says.** Use credible academic sources. Identify the key texts, key authors, and key claims for each perspective.

3. **Identify the fault lines.** Where do schools directly contradict each other? Where do they talk past each other? Where do they agree but for different reasons?

4. **Draft the comparison framework.** What dimensions should the comparison tool use? (Causal mechanism, policy prescription, empirical track record, assumptions about human behavior, assumptions about institutions, etc.)

5. **Gather source materials.** Identify which academic papers, book chapters, and other sources should form the Tier 1 reference base. Prioritize freely available or open-access materials where possible.

### Phase 2: Content Writing

Using the research outline:

1. Write the neutral introduction
2. Write each school's explanation of inflation (Tier 2 content)
3. Write the structured comparisons
4. Develop teaching materials (lesson plans, discussion questions, assessments, flashcards)
5. Write scripts for audio overviews and debates
6. Define the chatbot's system prompt, including its knowledge base, tone, and boundaries

### Phase 3: Technical Build

1. Set up the Django project structure
2. Build the topic hub page with school-of-thought navigation
3. Build the comparison tool
4. Integrate the AI chatbot
5. Generate and store audio content
6. Build the materials download section
7. Deploy to Railway

### Phase 4: Review and Iteration

1. Review all Tier 2 content for accuracy and balance
2. Test the chatbot against known edge cases and common misconceptions
3. Gather feedback from at least one IB economics teacher, one autodidact, and one organizational user
4. Iterate on content and UX based on feedback

---

## Future Phases (Post-MVP)

These are scoped out of the MVP but inform architectural decisions:

- **Additional topic modules** (money, employment, trade, fiscal policy, environmental economics, etc.)
- **Curriculum tagging** (map content to IB, IGCSE, AP syllabi so teachers can filter by their curriculum)
- **User accounts and progress tracking** (learning pathways, bookmarks, completion tracking)
- **Material generation tools** (on-demand slide decks, assessments, and policy briefs customized to context)
- **White-labeling** (organizations can brand the platform for internal use)
- **Multi-language support**
- **Mobile application** (based on the most-used web features)
- **Pre-made diagram library** (heterodox diagrams: administered pricing curves, stock-flow consistent models, sectoral balances, etc.) with potential for dynamic/interactive diagrams
- **Qualification pathways** for autodidacts who want structured credentialing

---

## Key Principles (for any AI assistant working on this project)

1. **Pluralism is genuine.** Do not favor any school of thought in tone, depth, or framing. Subject every perspective to the same standard of critical inquiry.

2. **Steel-man before critique.** Every school's position should be presented in its strongest, most charitable form before weaknesses are identified.

3. **Teaching, not advocacy.** The platform helps people understand economics, not convert them. If the heterodox perspectives are stronger, that will be evident from honest presentation. The platform does not need to argue the case.

4. **Accessibility over comprehensiveness.** Better to explain three perspectives clearly than five perspectives confusingly. IB-level readability is the floor.

5. **Practical utility.** Every piece of content should be usable: a teacher should be able to base a lesson on it, an autodidact should be able to learn from it, an organizer should be able to apply it.

6. **Honest about limitations.** Where evidence is contested, say so. Where a school's claims are untestable, note that. Where the platform's own coverage is incomplete, acknowledge it.

---

## Builder Context

- The primary builder is an amateur developer with experience building Python/HTML platforms on Railway, working with Claude as a coding assistant.
- There is no budget beyond reasonable bootstrapping costs.
- There is no hard deadline, but a functional MVP of the inflation module is the near-term goal.
- Peter (the IB economics teacher from the original conversation) is available as an occasional advisor but is not a co-builder.
- The existing MMT Academy platform (built separately) is a reference for feature ideas but this project starts from scratch.
