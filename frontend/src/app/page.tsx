'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Brain, Zap, Target, TrendingUp, MessageCircle, ChevronRight, BookOpen, Map } from 'lucide-react';
import { useAuthStore } from '@/store/auth';
import toast from 'react-hot-toast';
import { useState } from 'react';
import HeroVisual from './(app)/HeroVisual';
import RoleCard from './(app)/RoleCard';

const features = [
  { icon: Target, title: 'Skill Gap Analysis', desc: 'Identify the exact gaps blocking your dream role and prioritize your next wins with data-driven clarity.' },
  { icon: Map, title: 'Personalized Roadmap', desc: 'Get a realistic week-by-week learning plan built around your schedule, goals, and current skill level.' },
  { icon: Brain, title: 'AI Mentor Chat', desc: 'Ask questions in natural language and receive advice grounded in your profile, gaps, and progress.' },
  { icon: TrendingUp, title: 'Adaptive Learning', desc: 'Recalculate your roadmap as your hours change, your confidence changes, or your priorities shift.' },
  { icon: BookOpen, title: '100+ Free Resources', desc: 'Browse curated learning resources, courses, and projects ranked specifically for your target career path.' },
  { icon: MessageCircle, title: 'Smart Recommendations', desc: 'Get explainable AI recommendations with match scores and clear reasoning behind every suggestion.' },
];

const roles = ['AI/ML Engineer', 'Data Scientist', 'Frontend Developer', 'Backend Developer', 'Data Analyst', 'DevOps Engineer'];

const initialStats = [
  { label: 'Career Paths', value: '10+' },
  { label: 'Free Resources', value: '100+' },
  { label: 'Skills Tracked', value: '50+' },
  { label: 'AI-Powered', value: '100%' },
];

export default function HomePage() {
  const router = useRouter();
  const { demoLogin, isLoading } = useAuthStore();
  const [statsState] = useState(initialStats);

  const handleDemo = async () => {
    try {
      await demoLogin();
      toast.success('Welcome, Alex! Demo account loaded. 🎉');
      router.push('/dashboard');
    } catch {
      toast.error('Could not load demo. Make sure the backend is running.');
    }
  };

  return (
    <div className="space-shell min-h-screen overflow-hidden bg-[#030817] text-white">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(124,58,237,0.18),_transparent_35%),radial-gradient(circle_at_20%_20%,_rgba(56,189,248,0.12),_transparent_22%),radial-gradient(circle_at_80%_0%,_rgba(14,116,144,0.14),_transparent_24%)]" />

      <nav className="relative z-20 border-b border-white/10 bg-[#020b18]/80 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
          <Link href="/" className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-full border border-violet-400/50 bg-violet-500/10 text-violet-300">
              <Brain className="h-4 w-4" />
            </span>
            <span className="text-xl font-bold">LearnPath <span className="text-violet-400">AI</span></span>
          </Link>

          <div className="flex items-center gap-3">
            <Link href="/login" className="rounded-lg px-3 py-1.5 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white">
              Sign In
            </Link>
            <Link href="/onboarding" className="rounded-lg bg-violet-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-violet-500">
              Get Started Free
            </Link>
          </div>
        </div>
      </nav>

      <main className="relative z-10">
        <section className="px-4 pb-12 pt-20 sm:pt-24">
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
            <div className="mx-auto grid max-w-7xl items-center gap-10 lg:grid-cols-[1.08fr_0.92fr]">
              <div className="text-center lg:text-left">
                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-violet-400/25 bg-violet-500/8 px-4 py-2 text-sm text-violet-200">
                  <Zap className="h-4 w-4" />
                  AI-Powered • Zero Cost • Personalized by Design
                </div>

                <h1 className="text-4xl font-black leading-[0.95] sm:text-5xl md:text-6xl">
                  Your Personalized
                  <span className="mt-2 block bg-gradient-to-r from-white via-violet-200 to-cyan-300 bg-clip-text text-transparent">
                    Learning Roadmap
                  </span>
                </h1>

                <p className="mx-auto mt-5 max-w-xl text-base leading-relaxed text-slate-300 lg:mx-0">
                  Stop guessing what to learn next. LearnPath AI analyzes your skill profile, highlights critical gaps,
                  and builds a realistic roadmap tailored to your target role, schedule, and pace.
                </p>

                <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row lg:justify-start">
                  <Link href="/onboarding" className="inline-flex items-center justify-center gap-2 rounded-2xl bg-violet-600 px-6 py-3.5 text-base font-semibold text-white shadow-[0_0_25px_rgba(139,92,246,0.25)] transition hover:bg-violet-500">
                    Build My Roadmap Free
                    <ChevronRight className="h-5 w-5" />
                  </Link>
                  <button onClick={handleDemo} disabled={isLoading} className="inline-flex items-center justify-center rounded-2xl border border-slate-700 bg-slate-900/60 px-5 py-3.5 text-base font-semibold text-slate-100 transition hover:border-violet-400/50 hover:bg-slate-800">
                    {isLoading ? 'Loading...' : 'Try Demo Account'}
                  </button>
                </div>

                <div className="mt-8 grid max-w-xl grid-cols-2 gap-3 sm:grid-cols-4">
                  {statsState.map((stat) => (
                    <div key={stat.label} className="rounded-xl border border-white/8 bg-slate-900/40 p-3 text-center backdrop-blur-sm">
                      <div className="text-xl font-bold text-violet-300">{stat.value}</div>
                      <div className="mt-1 text-[11px] text-slate-400">{stat.label}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="relative flex items-center justify-center">
                <HeroVisual />
                <div className="absolute -bottom-3 right-6 rounded-full border border-violet-400/30 bg-white/5 px-3 py-1.5 text-[10px] font-medium uppercase tracking-[0.18em] text-violet-100 backdrop-blur-md">
                  AI Roadmap Generation
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        <section className="border-y border-white/10 bg-slate-950/30 py-8">
          <div className="mx-auto max-w-7xl px-4">
            <p className="mb-3 text-sm uppercase tracking-[0.2em] text-slate-400">Popular career paths</p>
            <div className="flex gap-4 overflow-x-auto pb-2">
              {roles.map((role, i) => (
                <div key={role} className="shrink-0">
                  <RoleCard role={role} href={`/onboarding?goal=${encodeURIComponent(role)}`} variant={i % 3} />
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 py-20">
          <motion.div initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="mb-12 text-center">
            <h2 className="text-3xl font-bold sm:text-4xl">Everything you need to accelerate your career</h2>
            <p className="mx-auto mt-4 max-w-xl text-slate-400">Not just another course list. LearnPath AI combines skill analysis, personalized planning, and mentoring in one system.</p>
          </motion.div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="rounded-2xl border border-white/8 bg-slate-900/45 p-6 shadow-[0_0_0_1px_rgba(148,163,184,0.02)] transition hover:border-violet-400/35 hover:bg-slate-900/70"
              >
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-violet-500/10 text-violet-300">
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="mb-2 text-xl font-semibold text-white">{feature.title}</h3>
                <p className="leading-relaxed text-slate-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        <section className="bg-slate-950/40 py-20">
          <div className="mx-auto max-w-5xl px-4 text-center">
            <motion.div initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
              <h2 className="text-3xl font-bold sm:text-4xl">Your roadmap in 3 steps</h2>
              <p className="mt-3 text-slate-400">Takes only a few minutes. No credit card or API key required.</p>
            </motion.div>

            <div className="mt-12 grid gap-8 sm:grid-cols-3">
              {[
                { step: '01', title: 'Tell us your goal', desc: 'Select your target role and current skill level to create a meaningful starting point.' },
                { step: '02', title: 'Rate your skills', desc: 'Use a quick self-assessment to highlight strengths and identify the biggest gaps.' },
                { step: '03', title: 'Get your roadmap', desc: 'Receive a step-by-step plan with milestones, resources, and progress tracking.' },
              ].map((item, index) => (
                <motion.div key={item.step} initial={{ opacity: 0, y: 18 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: index * 0.12 }} className="text-left rounded-2xl border border-white/8 bg-slate-900/40 p-6">
                  <div className="text-6xl font-black text-violet-500/30">{item.step}</div>
                  <h3 className="mt-3 text-xl font-semibold text-white">{item.title}</h3>
                  <p className="mt-2 text-slate-400">{item.desc}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="px-4 py-24 text-center">
          <motion.div initial={{ opacity: 0, scale: 0.96 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} className="mx-auto max-w-3xl rounded-[32px] border border-violet-400/20 bg-[radial-gradient(circle_at_top,_rgba(124,58,237,0.18),_rgba(15,23,42,0)_40%),linear-gradient(135deg,_rgba(17,24,39,0.8),_rgba(88,28,135,0.52))] p-10 shadow-[0_0_60px_rgba(139,92,246,0.18)]">
            <Brain className="mx-auto mb-6 h-16 w-16 text-violet-300" />
            <h2 className="text-3xl font-bold sm:text-4xl">Start your learning journey today</h2>
            <p className="mt-3 text-slate-300">Free forever. No credit card. No API key required.</p>
            <Link href="/onboarding" className="mt-8 inline-flex items-center gap-2 rounded-xl bg-violet-600 px-8 py-4 text-lg font-semibold text-white transition hover:bg-violet-500">
              Build My Free Roadmap
              <ChevronRight className="h-5 w-5" />
            </Link>
          </motion.div>
        </section>
      </main>

      <footer className="relative z-10 border-t border-white/10 bg-[#020b18] py-8 text-center text-sm text-slate-500">
        <div className="mb-2 flex items-center justify-center gap-2">
          <Brain className="h-4 w-4 text-violet-400" />
          <span className="font-semibold text-slate-200">LearnPath AI</span>
        </div>
        <p>Built for HCLTech Amplified Hackathon · AI-powered skill roadmap platform</p>
        <p className="mt-1">
          Demo: <span className="rounded bg-slate-900 px-2 py-0.5 text-slate-300">demo@skillora.io</span> / <span className="rounded bg-slate-900 px-2 py-0.5 text-slate-300">DemoPass123</span>
        </p>
      </footer>
    </div>
  );
}
