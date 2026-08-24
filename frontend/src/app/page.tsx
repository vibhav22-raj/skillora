'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Brain, Zap, Target, TrendingUp, MessageCircle, Star, ChevronRight, BookOpen, Map, Users } from 'lucide-react';
import { useAuthStore } from '@/store/auth';
import toast from 'react-hot-toast';
import { useEffect, useState } from 'react';
import HeroVisual from './(app)/HeroVisual';
import RoleCard from './(app)/RoleCard';

const features = [
  { icon: Target, title: 'Skill Gap Analysis', desc: 'Identify exactly what skills you\'re missing for your dream role with precision scoring across 50+ skills.' },
  { icon: Map, title: 'Personalized Roadmap', desc: 'Get a week-by-week learning plan that adapts to your schedule, experience, and learning style.' },
  { icon: Brain, title: 'AI Mentor Chat', desc: 'Ask any learning question and get instant, context-aware guidance from your AI learning mentor.' },
  { icon: TrendingUp, title: 'Adaptive Learning', desc: 'Your roadmap automatically recalculates when your schedule or priorities change.' },
  { icon: BookOpen, title: '100+ Free Resources', desc: 'Curated free courses, tutorials, and projects ranked by relevance to your specific goals.' },
  { icon: MessageCircle, title: 'Smart Recommendations', desc: 'AI-scored recommendations with detailed explanations for every suggestion.' },
];

const roles = ['AI/ML Engineer', 'Data Scientist', 'Frontend Developer', 'Backend Developer', 'Data Analyst', 'DevOps Engineer'];

// static stats for public landing page (avoid backend dependency when unauthenticated)
let initialStats = [
  { label: 'Career Paths', value: '10+' },
  { label: 'Free Resources', value: '100+' },
  { label: 'Skills Tracked', value: '50+' },
  { label: 'AI-Powered', value: '100%' },
];

export default function HomePage() {
  const router = useRouter();
  const { demoLogin, isLoading } = useAuthStore();
  // static landing stats — no backend call here so unauthenticated visitors see meaningful numbers
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
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white">
      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Brain className="h-7 w-7 text-indigo-500" />
            <span className="text-xl font-bold">LearnPath <span className="text-indigo-400">AI</span></span>
          </Link>
          <div className="flex items-center gap-3">
            <Link href="/login" className="text-slate-300 hover:text-white text-sm transition-colors px-3 py-1.5 rounded-lg hover:bg-slate-800">
              Sign In
            </Link>
            <Link href="/onboarding" className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
              Get Started Free
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-28 pb-20 px-4">
        <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            {/* Left: copy */}
            <div className="text-center lg:text-left">
              <div className="inline-flex items-center gap-2 bg-slate-900/40 text-indigo-300 text-sm px-4 py-2 rounded-full mb-4 border border-indigo-800">
                <Zap className="h-4 w-4" />
                AI-Powered • Demo Mode Available • Zero Cost
              </div>

              <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold mb-4 leading-tight">
                Your Personalized
                <br />
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-white/95 via-indigo-300 to-violet-400">
                  Learning Roadmap
                </span>
              </h1>

              <p className="text-lg text-slate-300 mb-6 max-w-xl mx-auto lg:mx-0 leading-relaxed">
                Stop guessing what to learn next. LearnPath AI analyzes your skills, identifies gaps, and builds a
                week-by-week roadmap tailored to your schedule and goals.
              </p>

              <div className="flex flex-col sm:flex-row gap-3 justify-center lg:justify-start">
                <Link href="/onboarding"
                  className="inline-flex items-center justify-center gap-3 bg-violet-600 hover:shadow-[0_0_18px_rgba(124,58,237,0.28)] text-white font-semibold px-6 py-3 rounded-2xl text-lg transition-all">
                  Build My Roadmap Free
                  <ChevronRight className="h-5 w-5" />
                </Link>

                <button
                  onClick={handleDemo}
                  disabled={isLoading}
                  className="inline-flex items-center justify-center gap-2 border border-slate-700 hover:border-indigo-500 text-slate-200 font-semibold px-5 py-3 rounded-2xl text-lg transition-all hover:bg-slate-900">
                  {isLoading ? 'Loading...' : '▶ Try Demo Account'}
                </button>
              </div>

              <p className="text-slate-500 text-sm mt-3">No credit card. Demo account includes realistic data for exploration.</p>

              {/* stat row */}
              <div className="mt-8 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-xl">
                {statsState.map((s: any) => (
                  <div key={s.label} className="bg-slate-900/40 border border-slate-800/60 rounded-lg p-3 text-center">
                    <div className="text-xl font-bold text-indigo-300">{s.value}</div>
                    <div className="text-slate-400 text-xs mt-1">{s.label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: visual */}
            <div className="flex items-center justify-center relative">
              <div className="w-full max-w-md">
                <HeroVisual />

                {/* glass tag */}
                <div className="absolute -bottom-6 right-6 bg-white/6 backdrop-blur-md border border-violet-700/30 text-xs text-indigo-100 px-3 py-1.5 rounded-full shadow-sm flex items-center gap-2">
                  <span className="inline-block w-2 h-2 rounded-full bg-violet-400 shadow-[0_0_8px_rgba(124,58,237,0.25)]" />
                  AI ROADMAP GENERATION
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* small spacer to flow into features */}
      <div className="max-w-7xl mx-auto px-4 -mt-8"></div>

      {/* Roles / Career path selector strip (Phase 2) */}
      <section className="py-8 bg-slate-900/50 border-y border-slate-800 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4">
          <h3 className="text-lg text-slate-300 mb-3">Popular career paths</h3>
          <div className="flex gap-4 overflow-x-auto hide-scrollbar py-2">
            {roles.map((role, i) => (
              <div key={role} className="flex-shrink-0">
                <RoleCard role={role} href={`/onboarding?goal=${encodeURIComponent(role)}`} variant={i % 3} />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-4 max-w-7xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">Everything you need to accelerate your career</h2>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">Not just another course list. LearnPath AI is a complete learning intelligence system.</p>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-6 transition-all group">
              <div className="w-12 h-12 bg-indigo-950 rounded-xl flex items-center justify-center mb-4 group-hover:bg-indigo-900 transition-colors">
                <f.icon className="h-6 w-6 text-indigo-400" />
              </div>
              <h3 className="text-white font-semibold text-lg mb-2">{f.title}</h3>
              <p className="text-slate-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="py-24 px-4 bg-slate-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Your roadmap in 3 steps</h2>
            <p className="text-slate-400 mb-12">Takes 2 minutes. No account required to see your plan.</p>
          </motion.div>

          <div className="grid sm:grid-cols-3 gap-8">
            {[
              { step: '01', title: 'Tell us your goal', desc: 'Select your target role (AI Engineer, Data Scientist, etc.) and current skill level.' },
              { step: '02', title: 'Rate your skills', desc: 'Quick self-assessment across relevant skills. Our AI fills in the gaps intelligently.' },
              { step: '03', title: 'Get your roadmap', desc: 'Receive a personalized, week-by-week learning plan with 100+ curated free resources.' },
            ].map((item, i) => (
              <motion.div key={item.step} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.15 }}
                className="relative">
                <div className="text-6xl font-bold text-indigo-900 mb-4">{item.step}</div>
                <h3 className="text-white font-semibold text-xl mb-2">{item.title}</h3>
                <p className="text-slate-400">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-4 text-center">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }}
          className="max-w-2xl mx-auto bg-gradient-to-br from-indigo-900/50 to-violet-900/50 border border-indigo-700/50 rounded-3xl p-12">
          <Brain className="h-16 w-16 text-indigo-400 mx-auto mb-6" />
          <h2 className="text-3xl font-bold mb-4">Start your learning journey today</h2>
          <p className="text-slate-300 mb-8">Free forever. No credit card. No API key required.</p>
          <Link href="/onboarding"
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-8 py-4 rounded-xl text-lg transition-all shadow-lg shadow-indigo-500/25">
            Build My Free Roadmap
            <ChevronRight className="h-5 w-5" />
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-8 text-center text-slate-500 text-sm px-4">
        <div className="flex items-center justify-center gap-2 mb-2">
          <Brain className="h-4 w-4 text-indigo-500" />
          <span className="font-semibold text-slate-300">LearnPath AI</span>
        </div>
        <p>Built for HCLTech Amplified Hackathon · AI-Powered · Open Source</p>
        <p className="mt-1">Demo: <code className="bg-slate-900 px-2 py-0.5 rounded">demo@learnpath.ai</code> / <code className="bg-slate-900 px-2 py-0.5 rounded">Demo@12345</code></p>
      </footer>
    </div>
  );
}
