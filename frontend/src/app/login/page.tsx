'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Brain, Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import { useAuthStore } from '@/store/auth';
import toast from 'react-hot-toast';

const FloatingSkillBadge = ({ skill, delay, x, y }: { skill: string; delay: number; x: number; y: number }) => (
  <motion.div
    initial={{ opacity: 0, scale: 0 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ delay, duration: 0.6, type: 'spring' }}
    className="absolute text-xs font-semibold bg-linear-to-r from-indigo-500/20 to-violet-500/20 border border-indigo-400/30 text-indigo-200 px-3 py-1 rounded-full backdrop-blur-sm"
    style={{ left: `${x}%`, top: `${y}%` }}>
    {skill}
  </motion.div>
);

const HeroIllustration = () => (
  <motion.div
    initial={{ opacity: 0, scale: 0.96 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.7 }}
    className="relative w-full max-w-md p-6 rounded-3xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl shadow-2xl space-y-4"
  >
    <div className="flex items-center justify-between border-b border-slate-800 pb-3">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-indigo-300 font-bold text-xs">
          AI
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">Target Career Pathway</h3>
          <p className="text-[11px] text-slate-400">Personalized • Adaptive • Deterministic</p>
        </div>
      </div>
      <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-full">
        Active Path
      </span>
    </div>

    <div className="space-y-3 relative">
      {/* Step 1 */}
      <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.15 }}
        className="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 border border-slate-700/40"
      >
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-xs">
            ✓
          </div>
          <div>
            <h4 className="text-xs font-semibold text-white">Diagnostic & Skill Gaps</h4>
            <p className="text-[11px] text-slate-400">Target role analysis complete</p>
          </div>
        </div>
        <span className="text-[10px] text-emerald-400 font-medium">100%</span>
      </motion.div>

      {/* Step 2 */}
      <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.3 }}
        className="flex items-center justify-between p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/40 shadow-lg shadow-indigo-500/5"
      >
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-xs animate-pulse">
            2
          </div>
          <div>
            <h4 className="text-xs font-semibold text-white">Personalized Roadmap</h4>
            <p className="text-[11px] text-indigo-300">Phase 2: Core Engineering</p>
          </div>
        </div>
        <span className="text-[10px] text-indigo-300 font-semibold bg-indigo-500/20 px-2 py-0.5 rounded-full">
          In Progress
        </span>
      </motion.div>

      {/* Step 3 */}
      <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 0.45 }}
        className="flex items-center justify-between p-3 rounded-xl bg-slate-850/40 border border-slate-800/60 opacity-80"
      >
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-slate-800 text-slate-400 flex items-center justify-center font-bold text-xs">
            3
          </div>
          <div>
            <h4 className="text-xs font-semibold text-slate-300">Industry Project & Portfolio</h4>
            <p className="text-[11px] text-slate-500">Real-world problem statement</p>
          </div>
        </div>
        <span className="text-[10px] text-slate-500 font-medium">Upcoming</span>
      </motion.div>
    </div>

    <div className="p-3 rounded-xl bg-indigo-900/30 border border-indigo-700/30 flex items-center justify-between text-xs">
      <span className="text-slate-300 flex items-center gap-1.5 font-medium">
        <span>⚡</span> Next Best Action ready
      </span>
      <span className="text-indigo-400 font-semibold text-[11px]">~25 min</span>
    </div>
  </motion.div>
);

export default function LoginPage() {
  const router = useRouter();
  const { login, register, demoLogin, isLoading } = useAuthStore();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [showPass, setShowPass] = useState(false);
  const [form, setForm] = useState({ name: '', email: '', password: '' });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (mode === 'login') {
        await login(form.email, form.password);
        toast.success('Welcome back! 👋');
      } else {
        await register(form.name, form.email, form.password);
        toast.success('Account created! Let\'s build your roadmap 🚀');
      }
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Invalid credentials. Please try again.');
    }
  };

  const handleDemo = async () => {
    try {
      await demoLogin();
      toast.success('Welcome, Alex! Demo account loaded 🎉');
      router.push('/dashboard');
    } catch {
      toast.error('Could not connect to backend. Make sure it\'s running on port 8000.');
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-950 via-slate-900 to-indigo-950 flex items-center justify-center relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-indigo-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-600/5 rounded-full blur-3xl" />
      </div>

      {/* Grid layout */}
      <div className="w-full h-full lg:grid lg:grid-cols-2 relative z-10 max-h-screen">
        {/* Hero section - hidden on mobile */}
        <div className="hidden lg:flex items-center justify-center p-8">
          <HeroIllustration />
        </div>

        {/* Login form section */}
        <div className="flex items-center justify-center px-4 py-8 min-h-screen lg:min-h-full">
          <div className="w-full max-w-sm">
            {/* Logo */}
            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
              className="text-center mb-8">
              <Link href="/" className="inline-flex items-center gap-2 mb-4">
                <div className="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <span className="text-2xl font-bold text-white">Skillora <span className="text-indigo-400">AI</span></span>
              </Link>
              <h1 className="text-3xl font-bold text-white mt-6">
                {mode === 'login' ? 'Welcome back' : 'Join the journey'}
              </h1>
              <p className="text-slate-400 mt-2">
                {mode === 'login' ? 'Continue your personalized learning path' : 'Start your AI-powered learning journey'}
              </p>
            </motion.div>

            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-slate-900/80 backdrop-blur-xl border border-slate-800/50 rounded-2xl p-8 shadow-2xl shadow-black/20">

          {/* Mode toggle */}
          <div className="flex bg-slate-800/50 rounded-xl p-1 mb-6">
            {(['login', 'register'] as const).map((m) => (
              <button key={m} onClick={() => setMode(m)}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${mode === m ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/25' : 'text-slate-400 hover:text-white hover:bg-slate-700/50'}`}>
                {m === 'login' ? 'Sign In' : 'Sign Up'}
              </button>
            ))}
          </div>

          {/* Demo button */}
          <motion.button onClick={handleDemo} disabled={isLoading}
            whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
            className="w-full mb-4 bg-linear-to-r from-amber-600/20 to-orange-600/20 hover:from-amber-600/30 hover:to-orange-600/30 border border-amber-600/50 text-amber-300 font-medium py-3 px-4 rounded-xl transition-all text-sm flex items-center justify-center gap-2 group">
            <span className="group-hover:scale-110 transition-transform">⚡</span>
            Try Demo Account
          </motion.button>

          <div className="flex items-center gap-3 mb-4">
            <div className="flex-1 h-px bg-slate-700" />
            <span className="text-slate-500 text-xs">or</span>
            <div className="flex-1 h-px bg-slate-700" />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === 'register' && (
              <div className="relative">
                <User className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
                <input type="text" placeholder="Full name" required value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl pl-10 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all" />
              </div>
            )}

            <div className="relative">
              <Mail className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
              <input type="email" placeholder="Email address" required value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl pl-10 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all" />
            </div>

            <div className="relative">
              <Lock className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
              <input type={showPass ? 'text' : 'password'} placeholder="Password" required value={form.password}
                onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl pl-10 pr-12 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all" />
              <button type="button" onClick={() => setShowPass(!showPass)}
                className="absolute right-3 top-3.5 text-slate-400 hover:text-slate-200 transition-colors">
                {showPass ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>

            <motion.button type="submit" disabled={isLoading}
              whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }}
              className="w-full bg-linear-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 disabled:opacity-60 text-white font-semibold py-3 rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/25">
              {isLoading ? (
                <><div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Loading...</>
              ) : (
                mode === 'login' ? 'Sign In' : 'Create Account'
              )}
            </motion.button>
          </form>

              <p className="text-center text-slate-500 text-sm mt-4">
                {mode === 'login' ? "Don't have an account? " : "Already have an account? "}
                <button onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
                  className="text-indigo-400 hover:underline font-medium">
                  {mode === 'login' ? 'Sign up free' : 'Sign in'}
                </button>
              </p>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}