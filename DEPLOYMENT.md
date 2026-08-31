# Skillora AI — Production Deployment Guide

This guide covers deploying **Skillora AI** to production using free-tier cloud platforms (**Vercel** for Frontend, **Render/Railway** for Backend, and **Supabase** for PostgreSQL).

---

## Architecture Overview

- **Frontend**: Next.js 16 (React 19, TypeScript, Tailwind CSS 4) hosted on **Vercel**.
- **Backend**: FastAPI (Python 3.11+, AsyncIO, SQLAlchemy 2.0) hosted on **Railway** or **Render**.
- **Database**: Managed PostgreSQL on **Supabase** (or SQLite for single-instance container deployments).
- **AI Layer**: **Groq API** (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`) with automatic fallback to **DemoProvider**.

---

## Step 1: Database Setup (Supabase / PostgreSQL)

1. Create an account at [Supabase](https://supabase.com).
2. Create a new project and retrieve the Connection String (URI).
3. Ensure the connection string uses the `postgresql+asyncpg` driver format:
   ```text
   postgresql+asyncpg://postgres:[YOUR-PASSWORD]@[YOUR-HOST]:5432/postgres
   ```
4. *Note: Skillora automatically runs migrations and seeds default skill/resource catalogs on startup.*

---

## Step 2: Backend Deployment (Railway or Render)

### Option A: Railway (Recommended)
1. Log in to [Railway](https://railway.app) and click **New Project** → **Deploy from GitHub repo**.
2. Select `vibhav22-raj/skillora`.
3. In **Settings**:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@[YOUR-HOST]:5432/postgres
   JWT_SECRET=your-secure-production-jwt-secret
   AI_PROVIDER=groq
   AI_API_KEY=your-groq-api-key
   DEMO_MODE=false
   FRONTEND_URL=https://your-skillora.vercel.app
   ```
5. Copy the generated service domain (e.g. `https://skillora-api.up.railway.app`).

### Option B: Render
1. Log in to [Render](https://render.com) and create a **New Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add the same environment variables listed above.

---

## Step 3: Frontend Deployment (Vercel)

1. Log in to [Vercel](https://vercel.com) and click **Add New Project**.
2. Import the `vibhav22-raj/skillora` repository.
3. Configure the build settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
4. Add Environment Variables:
   ```env
   NEXT_PUBLIC_API_URL=https://your-skillora-backend.up.railway.app
   ```
5. Click **Deploy**. Vercel will build all static pages and deploy the application.

---

## Step 4: Verification & Smoke Testing

Once both services are live:
1. Navigate to the Vercel URL.
2. Complete onboarding with a sample career goal (e.g. *AI/ML Engineer*).
3. Verify that the **Skill Gap Matrix**, **Personalized Roadmap**, and **Recommendations** load properly.
4. Test the **AI Mentor** by asking a conceptual question (*"What is recursion?"* or *"What is polymorphism?"*).
5. Verify response completion, crisp formatting, and clean markdown rendering.

---

## Environment Variables Summary

### Backend
| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `DATABASE_URL` | No | `sqlite+aiosqlite:///./learnpath.db` | PostgreSQL or SQLite connection URI |
| `JWT_SECRET` | Yes | `change-me-in-production` | Secret key for signing auth tokens |
| `AI_PROVIDER` | No | `groq` | `groq` or `demo` |
| `AI_API_KEY` | No | `None` | Groq API Key |
| `DEMO_MODE` | No | `false` | Fallback mode indicator |
| `FRONTEND_URL` | No | `http://localhost:3000` | Allowed frontend origin for CORS |

### Frontend
| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | Deployed backend REST API URL |
