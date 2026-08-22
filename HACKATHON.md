# HACKATHON.md — HCLTech Amplified

## Problem Statement

**AI-Powered Personalized Learning Path Recommender**

Online platforms have thousands of courses, but learners struggle to know:
- What to learn
- In what order
- Which skills they're missing
- Which resources match their exact level
- What to do next toward a specific career goal

---

## Solution: LearnPath AI

A complete AI-powered career learning system that acts as your personal learning mentor, roadmap generator, and adaptive recommendation engine — all in one app.

---

## WOW Features

### 1. 🎯 Intelligent Skill Gap Engine
- Maintains a complete skill requirements map for **10 career roles**
- Calculates exact skill gaps with priority levels (Critical → Low)
- Considers **prerequisite chains** — knows Python must come before ML
- Uses topological sorting to determine optimal learning order

### 2. 🗺️ Adaptive Roadmap Generation
The roadmap generator doesn't just list skills — it:
- Creates **phase-by-phase learning plans** with weeks, resources, projects, milestones
- **Auto-skips** phases for skills you already know
- **Adjusts timeline** based on your weekly hours commitment
- Supports 6 role-specific phase templates

### 3. ⚡ Natural Language Roadmap Adaptation (THE WOW FEATURE)
```
User: "I only have 5 hours per week now"
AI: "Understood! I've recalculated your roadmap.
     Your original 32-week plan has been extended to 48 weeks.
     No content was removed — just spread over a longer timeline."
```
The AI interprets natural language → maps to action → recalculates → responds conversationally.

Supported adaptations:
- Reduce/increase weekly hours
- Skip already-known skills
- Add prerequisite paths for difficult skills
- Adjust difficulty progression

### 4. ⭐ Explainable AI Recommendations
Every recommendation includes:
- **Overall match score** (0-100)
- **6-factor score breakdown** (goal relevance, gap coverage, prereq fit, difficulty, time, style)
- **Natural language explanation**: "This course is ranked #1 because it directly addresses your critical gap in Statistics..."

### 5. 🤖 Context-Aware AI Mentor
The chat is not generic — it's fully aware of:
- Your current skill levels
- Your active skill gaps
- Your target role and career goal
- Your weekly study schedule

Provides specific, actionable guidance rather than generic advice.

---

## Technical Architecture

### Backend
- **FastAPI** (async Python) with 11 API routers
- **SQLAlchemy 2.0** async ORM (SQLite → PostgreSQL)
- **AI Provider Chain**: Gemini → Groq → Demo fallback
- **Custom recommendation engine** (no ML framework needed)

### Frontend
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Framer Motion** for animations
- **Recharts** for data visualization
- **Zustand** for state management
- **TanStack Query** for server state

### AI Features Without a Paid API
- All features work with `DEMO_MODE=true`
- Demo provider uses pattern matching + templates to simulate AI responses
- Recommendation scoring is pure algorithmic (no LLM needed)
- Roadmap generation is template-based (no LLM needed)

---

## Innovation Points

| Feature | Standard Approach | Our Approach |
|---------|------------------|--------------|
| Recommendations | Simple filtering | 6-factor weighted scoring with explanations |
| Roadmap | Static curricula | Dynamic, adaptive, NL-adjustable |
| Skill Assessment | Score-only | Score + calibrates roadmap automatically |
| AI Chat | Generic chatbot | Full context of user's skills, gaps, roadmap |
| API Keys | Required | Zero mandatory APIs (demo mode) |

---

## Deployment & Scalability

- **Zero mandatory paid services** for hackathon demo
- Production-ready: Vercel (FE) + Render (BE) + Supabase (DB)
- Docker containerized backend
- Async SQLAlchemy scales to PostgreSQL without code changes
