# Skillora AI — Frontend Application

This is the Next.js frontend application for **Skillora AI**, an AI-powered personalized learning path recommender.

---

## Tech Stack

- **Framework**: Next.js 16.3.1 (App Router, Turbopack)
- **Library**: React 19.2.8
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4, Glassmorphism UI
- **Animations**: Framer Motion 13
- **State Management**: TanStack React Query v5, Zustand v5
- **Visualizations**: Recharts 3
- **Markdown & Icons**: React-Markdown 10, Lucide-React

---

## Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Copy `.env.example` to `.env.local`:
```bash
copy .env.example .env.local
```
Set `NEXT_PUBLIC_API_URL` to your backend API URL (defaults to `http://localhost:8000`).

### 3. Run Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Production Build

```bash
npm run build
npm start
```
