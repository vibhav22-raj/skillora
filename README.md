<<<<<<< HEAD
# LearnPath AI 🧠

> **AI-Powered Personalized Learning Path Recommender** — HCLTech Amplified Hackathon

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat&logo=nextdotjs)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat&logo=typescript)](https://typescriptlang.org/)

## 🎯 What It Does

LearnPath AI is a complete AI-powered career learning system that:

- 🎯 **Analyzes your skill gaps** against 10 target roles (AI/ML Engineer, Data Scientist, etc.)
- 🗺️ **Generates a week-by-week personalized roadmap** from your current level to your goal
- ⚡ **Adapts your plan** when life changes ("I only have 5 hours this week")
- 🤖 **AI Mentor chat** for instant learning guidance
- ⭐ **Recommends resources** with explainable AI scoring (6-factor algorithm)
- 📊 **Tracks your progress** with streaks, charts, and milestone achievements
- 📝 **Skill assessments** that calibrate your roadmap based on actual test results

## 🚀 Quick Start (Local Dev)

### Prerequisites
- Python 3.12+, Node.js 18+, npm

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --port 8000
```

Backend runs on: http://localhost:8000
API docs at: http://localhost:8000/docs

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Frontend runs on: http://localhost:3000

### Demo Account

After backend starts, the demo account is auto-created:
- **Email:** `demo@learnpath.ai`
- **Password:** `Demo@12345`

## 🏗️ Architecture

```
learnpath-ai/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/             # 11 API router modules
│   │   ├── models/          # SQLAlchemy ORM models (SQLite/PostgreSQL)
│   │   ├── schemas/         # Pydantic v2 validation schemas
│   │   ├── services/        # Auth (JWT + bcrypt)
│   │   ├── recommender/     # 5-module AI recommendation engine
│   │   │   ├── skill_gap.py          # Role skill requirements
│   │   │   ├── prerequisite_graph.py # DAG topological sorting
│   │   │   ├── scorer.py             # 6-factor weighted scoring
│   │   │   ├── roadmap_generator.py  # Personalized phase generation
│   │   │   └── next_best_action.py   # Adaptive next step
│   │   ├── ai/              # AI provider chain
│   │   │   ├── demo_provider.py  # Works with ZERO API keys
│   │   │   ├── gemini_provider.py
│   │   │   └── groq_provider.py
│   │   └── database/        # Async SQLAlchemy + seed data
│   └── tests/               # Pytest test suite (25 tests)
│
└── frontend/                # Next.js 15 TypeScript frontend
    └── src/
        ├── app/
        │   ├── page.tsx           # Landing page
        │   ├── login/             # Auth
        │   ├── onboarding/        # 5-step setup wizard
        │   └── (app)/             # Dashboard layout group
        │       ├── dashboard/     # Main dashboard
        │       ├── roadmap/       # Visual roadmap + AI adapt
        │       ├── recommendations/ # Scored recommendations
        │       ├── resources/     # 100+ searchable resources
        │       ├── skills/        # Skill gap analysis
        │       ├── assessment/    # Interactive quizzes
        │       ├── projects/      # Portfolio project browser
        │       └── chat/          # AI Mentor chat
        ├── lib/api.ts             # Complete API client
        ├── store/auth.ts          # Zustand auth state
        └── types/index.ts         # TypeScript interfaces
```

## 🤖 AI Provider Chain

The app works with ZERO API keys thanks to the fallback chain:

```
1. Gemini 1.5 Flash (if GEMINI_API_KEY set)
2. Groq Llama3 (if GROQ_API_KEY set)
3. Demo Provider (built-in, always works)
```

Set `DEMO_MODE=true` or leave no API key — the app works fully.

## 🎯 Recommendation Scoring Algorithm

Each resource is scored 0-100 using a weighted multi-factor model:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Goal Relevance | 25% | How well resource skills match target role |
| Skill Gap Coverage | 25% | Does it address your specific gaps? |
| Prerequisite Fit | 20% | Do you have the prerequisites? |
| Difficulty Match | 15% | Optimal challenge level (slightly above current) |
| Time Fit | 10% | Duration fits your weekly schedule |
| Learning Style | 5% | Matches preferred format (video/reading/etc) |

## 📊 Seed Data

The demo database includes:
- **50+ skills** across 8 categories
- **100+ free resources** from Coursera, YouTube, Harvard, Google, MIT, fast.ai
- **30+ projects** from beginner CLI to advanced MLOps pipelines
- **5 skill assessments** with detailed explanations
- **1 complete demo user** (AI/ML Engineer roadmap, intermediate level)

## 🧪 Tests

```bash
cd backend
python -m pytest tests/ -v
# 25/25 tests passing
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for Vercel + Render + Supabase deployment.

## 🏆 Hackathon

See [HACKATHON.md](HACKATHON.md) for problem statement, solution design, and WOW features.

