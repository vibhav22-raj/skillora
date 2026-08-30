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
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.8, delay: 0.1 }}
    className="relative w-full h-full flex items-center justify-center px-8">
    {/* Central circle gradient */}
    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
      <motion.div
        className="w-64 h-64 bg-linear-to-br from-indigo-500/20 to-violet-500/20 rounded-full blur-3xl"
        animate={{ scale: [1, 1.1, 1] }}
        transition={{ duration: 4, repeat: Infinity }}
      />
    </div>

    {/* SVG Illustration - Learning journey visual */}
    <svg className="w-full max-w-sm relative z-10" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Brain/AI icon */}
      <motion.g
        animate={{ y: [-5, 5, -5] }}
        transition={{ duration: 3, repeat: Infinity }}
      >
        <circle cx="200" cy="120" r="35" fill="none" stroke="url(#brainGradient)" strokeWidth="2" />
        <path d="M 180 120 Q 180 105 200 105 Q 220 105 220 120" fill="none" stroke="url(#brainGradient)" strokeWidth="2" />
        <circle cx="190" cy="115" r="4" fill="url(#brainGradient)" />
        <circle cx="210" cy="115" r="4" fill="url(#brainGradient)" />
      </motion.g>

      {/* Learning path nodes */}
      <motion.g
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.1 }}
      >
        {/* Python */}
        <circle cx="100" cy="200" r="20" fill="none" stroke="#60a5fa" strokeWidth="2" />
        <text x="100" y="206" textAnchor="middle" fontSize="12" fill="#bfdbfe" fontWeight="bold">Py</text>

        {/* Arrow 1 */}
        <line x1="115" y1="200" x2="165" y2="200" stroke="#6366f1" strokeWidth="1.5" strokeDasharray="5,5" />
        <polygon points="170,200 165,197 165,203" fill="#6366f1" />
      </motion.g>

      {/* ML */}
      <motion.g
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.3 }}
      >
        <circle cx="200" cy="200" r="20" fill="none" stroke="#a78bfa" strokeWidth="2" />
        <text x="200" y="206" textAnchor="middle" fontSize="12" fill="#ddd6fe" fontWeight="bold">ML</text>

        {/* Arrow 2 */}
        <line x1="215" y1="200" x2="265" y2="200" stroke="#6366f1" strokeWidth="1.5" strokeDasharray="5,5" />
        <polygon points="270,200 265,197 265,203" fill="#6366f1" />
      </motion.g>

      {/* AI */}
      <motion.g
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
      >
        <circle cx="300" cy="200" r="20" fill="none" stroke="#ec4899" strokeWidth="2" />
        <text x="300" y="206" textAnchor="middle" fontSize="12" fill="#fbcfe8" fontWeight="bold">AI</text>
      </motion.g>

      {/* Upward growth path */}
      <motion.path
        d="M 140 280 Q 200 220 260 160"
        fill="none"
        stroke="url(#pathGradient)"
        strokeWidth="2"
        strokeDasharray="300"
        initial={{ strokeDashoffset: 300 }}
        animate={{ strokeDashoffset: 0 }}
        transition={{ duration: 3, delay: 0.5, repeat: Infinity }}
      />

      {/* Career target */}
      <motion.g
        animate={{ scale: [1, 1.1, 1], rotate: [0, 3, 0] }}
        transition={{ duration: 2.5, repeat: Infinity }}
      >
        <circle cx="280" cy="140" r="15" fill="none" stroke="#10b981" strokeWidth="2" />
        <path d="M 275 140 L 280 145 L 285 135" fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </motion.g>

      {/* Gradient definitions */}
      <defs>
        <linearGradient id="brainGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#a78bfa" />
        </linearGradient>
        <linearGradient id="pathGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#10b981" />
        </linearGradient>
      </defs>
    </svg>

    {/* Floating skill badges */}
    <FloatingSkillBadge skill="Python" delay={0.2} x={15} y={30} />
    <FloatingSkillBadge skill="DSA" delay={0.35} x={75} y={20} />
    <FloatingSkillBadge skill="SQL" delay={0.5} x={70} y={65} />
    <FloatingSkillBadge skill="Cloud" delay={0.65} x={15} y={75} />
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