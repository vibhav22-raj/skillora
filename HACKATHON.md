# Skillora AI — Hackathon Overview & Evaluation Guide

## 1. Problem Statement
**PathFinder / AI-Powered Personalized Learning Path Recommender**

Modern learners navigating self-directed tech education face several key challenges:
- **Generic Curricula**: One-size-fits-all recommendations fail to account for the learner's existing skills, background, and weekly availability.
- **Skill Gap Blindspots**: Learners struggle to identify exactly what competencies they need to reach their target job role.
- **Prerequisite Misalignment**: Learning paths often lack prerequisite ordering, causing learners to encounter advanced topics without sufficient foundation.

---

## 2. Solution: Skillora AI
**Skillora AI** is an intelligent, context-driven learning assistant that builds an end-to-end personalized curriculum tailored to the learner's background, target career role, and pace.

### Key Capabilities:
1. **Natural Language & Interactive Profiling**: Captures learner goals, weekly time commitments, and experience levels.
2. **Dynamic Skill Gap Engine**: Automatically calculates gap magnitude and assigns priority tiers (*Critical*, *High*, *Medium*, *Low*).
3. **Explainable Recommendations**: Uses a 5-factor weighted algorithm ($0.35\text{ Goal} + 0.25\text{ Gap} + 0.20\text{ Prereq} + 0.10\text{ Difficulty} + 0.10\text{ Preference}$) with plain-English justification for why each resource was chosen.
4. **Prerequisite-Aware Roadmap**: Employs Directed Acyclic Graph (DAG) topological sorting so foundational skills always precede advanced applications.
5. **Context-Injected AI Mentor**: Leverages Groq LLMs (with instant offline fallback) to provide 1-on-1 coaching, concise 3-part concept explanations, and practical milestone guidance.
6. **Project Hub & Skill Quizzes**: Contextualizes portfolio projects with actionable blueprints and recalibrates skill state through interactive assessments.

---

## 3. Alignment with Judging Criteria

### 1. Problem Understanding & Solution Design (20%)
- **End-to-End Pipeline**: Follows a cohesive trajectory: *Onboarding → Skill Gap Analysis → Prerequisite DAG → Multi-Factor Recommendations → Adaptive Roadmap → AI Coaching*.
- **Explainability**: Every recommendation card explicitly explains the selection rationale based on target role and active skill gaps.

### 2. Functionality & Feature Completeness (25%)
- All 8 core prompt requirements are fully implemented and functional:
  - Learner profiling
  - Skill gap identification
  - Personalized recommendations with explanations
  - Milestone roadmap generation with prerequisite ordering
  - Interactive quiz assessments with skill score updates
  - Hands-on project hub with AI blueprints
  - Multi-turn AI mentor chat
  - Comprehensive progress dashboard

### 3. AI/ML Implementation (20%)
- **Hybrid Architecture**: Combines deterministic graph and mathematical scoring algorithms with low-latency LLM inference via Groq (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`).
- **Context Injection**: Mentors receive dynamic system prompts populated with real-time user skills, gap priorities, and active milestones.
- **Guardrails & Fallback**: Strictly structured 3-part concept answers and `DemoProvider` guarantee 100% platform availability.

### 4. Innovation & Creativity (15%)
- **Natural Language Timeline Adaptation**: Adjusts roadmap duration and milestone schedules dynamically based on changes to weekly study hours.
- **Interactive Project Blueprint Generator**: Converts recommended project ideas into structured, guided implementation sprints via the AI Mentor.

### 5. User Experience & Interface (10%)
- Modern dark-themed glassmorphism interface built with Tailwind CSS 4, Framer Motion animations, and responsive layouts.
- Real-time progress trackers, skill mastery charts, and interactive quiz interfaces.

### 6. Performance & Code Quality (10%)
- **Backend**: FastAPI async architecture with SQLAlchemy 2.0 ORM; automated pytest test suite (**29/29 passing**).
- **Frontend**: Next.js 16 App Router with React 19 and TypeScript (**0 type errors**, production build verified).

---

## 4. Verification & Demo Flow

To evaluate Skillora AI during the demo:
1. **Try Demo Account**: Log in instantly with seeded profile data.
2. **Review Gaps & Recommendations**: Navigate to **Skills & Gaps** and **Recommendations** to see the 5-factor scoring and personalized justification.
3. **Inspect Roadmap**: View the phase-by-phase prerequisite DAG roadmap.
4. **Chat with AI Mentor**: Ask conceptual questions (*"What is recursion?"*, *"What is polymorphism?"*) to verify structured, complete coaching responses.
5. **Take Assessment**: Complete a topic quiz and observe real-time skill score updates.
