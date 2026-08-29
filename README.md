# Skillora (LearnPath AI)

AI-powered personalized learning platform for the HCLTech Amplified Hackathon.

The product UI is branded **LearnPath AI**. The repository and hackathon submission name is **Skillora**.

Skillora analyzes a learner’s goal, current skills, gaps, progress, preferences, and available time. It then generates a personalized roadmap, explainable recommendations, assessments, industry-oriented projects, and AI mentor support. The app runs in zero-cost demo mode with no mandatory paid APIs.

## What The App Does

- Authentication with JWT, bcrypt, register/login, and a seeded demo account.
- Learner profile, onboarding, profile image, bio, preferences, streak, and activity heatmap.
- Skill-gap analysis for target career roles.
- Personalized learning roadmap generation and natural-language adaptation.
- Explainable resource recommendations and a Next Best Action.
- Dashboard with progress, streak, weekly activity, and current milestone.
- Resources browser with progress actions.
- Assessments (15–20 question banks, 15 questions per session) with strong/weak area results.
- 50+ industry-oriented portfolio projects with domain, problem statement, and resume value.
- AI Mentor with Gemini/Groq when keys are present, plus a deterministic demo fallback.
- Responsive layout with desktop sidebar and mobile bottom navigation.

## Tech Stack

**Backend**

- FastAPI, SQLAlchemy async, SQLite by default
- Pydantic v2, JWT + bcrypt
- Optional Gemini or Groq; DemoProvider fallback
- Custom recommendation engine (skill gap, scoring, prerequisites, roadmap, next action)
cd backend 
python -m uvicorn app.main:app --port 8000

**Frontend**

- Next.js 16 App Router, React 19, TypeScript
- Tailwind CSS 4, Framer Motion, TanStack Query, Zustand, Recharts
cd frontend 
npm run dev

## Project Structure

```text
HCL_Amplified/
  backend/
    app/
      api/              FastAPI routes
      ai/               Gemini, Groq, and demo providers
      config/           Runtime settings
      database/         Async DB setup and seed data
      models/           SQLAlchemy ORM models
      recommender/      Skill gap, scoring, roadmap, next action
      schemas/          Pydantic schemas
      services/         Auth and profile services
      main.py           FastAPI entrypoint
    tests/
    requirements.txt
  frontend/
    src/app/            Next.js App Router pages
    src/lib/api.ts      API client
    src/store/auth.ts   Zustand auth store
    src/types/index.ts
    package.json
  HACKATHON.md
  DEPLOYMENT.md
```

## Prerequisites

- Python 3.12 or newer
- Node.js 20 or newer
- npm

## Environment Setup

### Backend (Optional)

The backend works **without a `.env` file** — it uses sensible defaults.

If you want to customize settings, create `backend/.env`:

```env
AI_PROVIDER=demo
AI_API_KEY=
DEMO_MODE=true
DATABASE_URL=sqlite+aiosqlite:///./learnpath.db
JWT_SECRET=your-secret-key-change-in-production
```

**Supported AI Providers:**
- `demo` (default) — Pattern-matching, always available, zero-cost
- `gemini` — Requires `AI_API_KEY` (Google AI API key)
- `groq` — Requires `AI_API_KEY` (Groq API key)

### Frontend (Optional)

Frontend uses `http://localhost:8000` by default. To customize, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Install Dependencies

**Backend** (from the repository root, so `backend.app` imports resolve):

```powershell
python -m pip install -r backend/requirements.txt
```

**Frontend:**

```powershell
cd frontend
npm install
```

## Start The Backend Server

Always start the API from the **repository root**, not from the `backend/` folder. Imports are `backend.app.*`.

```powershell
python -m uvicorn backend.app.main:app --reload --port 8000
```

- App: http://localhost:8000
- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Keep this terminal running.

## Start The Frontend Server

Open a **second terminal**:

```powershell
cd frontend
npm run dev
```

App URL: http://localhost:3000

## Demo Login

The backend seeds a demo user on startup.

```text
Email: demo@learnpath.ai
Password: Demo@12345
```

You can also use **Try Demo** on the landing page. A judge can enter the product immediately with no paid APIs.

## Useful Commands

Backend tests:

```powershell
python -m pytest backend/tests -v
```

Frontend lint and production build:

```powershell
cd frontend
npm run lint
npm run build
npm run start
```

## AI Provider Chain

```text
Configured Gemini or Groq (optional)
        ↓
Demo Provider (always available, offline)
```

Recommendation scoring and roadmap generation are deterministic. The LLM is used for mentor chat, explanations, and natural-language adaptation.

## Database

SQLite is the default. Tables are created on startup. Seed data includes skills, resources, 50+ projects, 5 assessments, and the demo user.

Existing local databases receive additive columns (`bio`, `profile_image`, project metadata) on startup. You do not need to delete `learnpath.db` unless seed data is stale.

If assessments still show 6–7 questions after a previous run, restart the backend so seed can expand the question banks.

## Hackathon Demo Flow (2–3 minutes)

1. Open http://localhost:3000 and use demo login.
2. Dashboard: show Next Best Action, streak, and progress.
3. Skills: show gap bars for the AI/ML Engineer path.
4. Roadmap: show the personalized phased plan.
5. Recommendations: open score breakdown (“why this?”).
6. AI Mentor: ask `I only have 1 hour today. What should I study?` and a Hinglish question such as `bhai mujhe recursion samajh nahi aa raha`.
7. Take an assessment and show strong/weak areas.
8. Projects: filter by domain and show industry metadata.

## Deployment

See `DEPLOYMENT.md`. Keep private AI keys in backend environment variables only. Never put private keys in `NEXT_PUBLIC_*` variables.

## Zero-Cost Constraint

No paid OpenAI, Anthropic, hosted vector DB, or paid auth is required. Demo mode is the default for judging.
