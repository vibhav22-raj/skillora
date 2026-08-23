'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Brain, Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import { useAuthStore } from '@/store/auth';
import toast from 'react-hot-toast';

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
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 mb-4">
            <Brain className="h-8 w-8 text-indigo-500" />
            <span className="text-2xl font-bold text-white">LearnPath <span className="text-indigo-400">AI</span></span>
          </Link>
          <h1 className="text-2xl font-bold text-white">
            {mode === 'login' ? 'Welcome back' : 'Create your account'}
          </h1>
          <p className="text-slate-400 mt-1">
            {mode === 'login' ? 'Sign in to continue your learning journey' : 'Start your personalized learning journey'}
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900 border border-slate-800 rounded-2xl p-8">

          {/* Mode toggle */}
          <div className="flex bg-slate-800 rounded-xl p-1 mb-6">
            {(['login', 'register'] as const).map((m) => (
              <button key={m} onClick={() => setMode(m)}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition-all ${mode === m ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'}`}>
                {m === 'login' ? 'Sign In' : 'Sign Up'}
              </button>
            ))}
          </div>

          {/* Demo button */}
          <button onClick={handleDemo} disabled={isLoading}
            className="w-full mb-4 bg-amber-600/20 hover:bg-amber-600/30 border border-amber-600/50 text-amber-300 font-medium py-3 px-4 rounded-xl transition-all text-sm flex items-center justify-center gap-2">
            <span>⚡</span>
            Try Demo Account (demo@learnpath.ai)
          </button>

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
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500" />
              </div>
            )}

            <div className="relative">
              <Mail className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
              <input type="email" placeholder="Email address" required value={form.email}
                onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-10 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500" />
            </div>

            <div className="relative">
              <Lock className="absolute left-3 top-3.5 h-5 w-5 text-slate-400" />
              <input type={showPass ? 'text' : 'password'} placeholder="Password" required value={form.password}
                onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
                className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-10 pr-12 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500" />
              <button type="button" onClick={() => setShowPass(!showPass)}
                className="absolute right-3 top-3.5 text-slate-400 hover:text-slate-200">
                {showPass ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>

            <button type="submit" disabled={isLoading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-white font-semibold py-3 rounded-xl transition-all flex items-center justify-center gap-2">
              {isLoading ? (
                <><div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Loading...</>
              ) : (
                mode === 'login' ? 'Sign In' : 'Create Account'
              )}
            </button>
          </form>

          <p className="text-center text-slate-500 text-sm mt-4">
            {mode === 'login' ? "Don't have an account? " : "Already have an account? "}
            <button onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
              className="text-indigo-400 hover:underline font-medium">
              {mode === 'login' ? 'Sign up free' : 'Sign in'}
            </button>
          </p>
        </motion.div>

        <p className="text-center text-slate-600 text-xs mt-4">
          Demo credentials: demo@learnpath.ai / Demo@12345
        </p>
      </div>
    </div>
  );
}
