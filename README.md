# LearnPath AI

LearnPath AI is an AI-powered learning platform that helps users discover their next best skills, generate personalized roadmaps, and learn faster with a focused, adaptive plan.

Built for the HCLTech Amplified Hackathon, the project blends a modern frontend experience with a FastAPI backend, recommendation logic, and AI-assisted learning workflows.

## What the product does

- Analyzes a learner's current skill profile versus a target career role
- Identifies critical skill gaps and ranks them by priority
- Builds a personalized weekly learning roadmap
- Suggests curated free learning resources and projects
- Adapts the roadmap based on time constraints and progress
- Provides an AI mentor chat for contextual guidance
- Tracks learning progress and recommendation quality

## Tech stack

- Frontend: Next.js, TypeScript, Tailwind CSS, Framer Motion
- Backend: FastAPI, SQLAlchemy, Pydantic
- AI layer: Demo provider with optional Gemini/Groq fallback
- Database: SQLite for local development, PostgreSQL-ready for production

## Quick start

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Local URLs

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

## Demo account

The app seeds a demo user automatically.

- Email: demo@skillora.io
- Password: DemoPass123

## Project structure

```text
LearnPath AI/
├── backend/              # FastAPI backend
├── frontend/             # Next.js frontend
├── README.md             # Project overview
├── HACKATHON.md          # Hackathon positioning and solution narrative
├── DEPLOYMENT.md         # Local and cloud deployment guide
└── .gitignore
```

## Important notes

- The app is designed to work without mandatory paid API keys.
- Demo mode is available for local testing and hackathon presentations.
- The backend can run from the terminal without IDE-specific setup.

## References

- [DEPLOYMENT.md](DEPLOYMENT.md)
- [HACKATHON.md](HACKATHON.md)

