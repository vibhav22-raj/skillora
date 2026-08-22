# Deployment Guide

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

---

## Free Production Deployment

### Option 1: Vercel + Render + Supabase (Recommended)

#### 1. Database — Supabase (Free tier)
1. Create account at supabase.com
2. New project → Get connection string
3. Format: `postgresql+asyncpg://user:pass@host:5432/dbname`

#### 2. Backend — Render (Free tier)
1. Create account at render.com
2. New Web Service → Connect GitHub repo
3. Root Directory: `backend`
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Environment variables:
```
DATABASE_URL=postgresql+asyncpg://...  (from Supabase)
JWT_SECRET=your-secret-key-here
AI_PROVIDER=demo
DEMO_MODE=true
FRONTEND_URL=https://your-app.vercel.app
```

#### 3. Frontend — Vercel (Free tier)
1. Create account at vercel.com
2. Import GitHub repo
3. Root Directory: `frontend`
4. Environment variables:
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

---

## Docker Deployment

```bash
cd backend
docker build -t learnpath-api .
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite+aiosqlite:///./learnpath.db \
  -e JWT_SECRET=your-secret \
  -e DEMO_MODE=true \
  learnpath-api
```

## Environment Variables

### Backend (.env)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | No | sqlite+aiosqlite:///./learnpath.db | Database connection |
| JWT_SECRET | Yes | change-me-in-production | JWT signing key |
| AI_PROVIDER | No | demo | `demo`, `gemini`, or `groq` |
| AI_API_KEY | No | - | API key for Gemini/Groq |
| DEMO_MODE | No | true | Enable demo features |
| FRONTEND_URL | No | http://localhost:3000 | For CORS |

### Frontend (.env.local)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | Yes | http://localhost:8000 | Backend URL |
