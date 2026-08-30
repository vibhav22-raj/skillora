'use client';

import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { dashboardAPI } from '@/lib/api';
import { useAuthStore } from '@/store/auth';
import { getGreeting, getStreakEmoji, getDifficultyColor } from '@/lib/utils';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import Walkthrough from './Walkthrough';
import {
  TrendingUp, Clock, Zap, Target, ChevronRight, BookOpen,
  MessageCircle, CheckCircle, Play, Star, Map,
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, RadarChart, Radar, PolarGrid, PolarAngleAxis } from 'recharts';
import ReactMarkdown from 'react-markdown';

const StatCard = ({ label, value, icon: Icon, color = 'indigo', subtitle = '', delay = 0 }: any) => (
  <motion.div 
    initial={{ opacity: 0, y: 16, scale: 0.95 }} 
    animate={{ opacity: 1, y: 0, scale: 1 }}
    transition={{ delay, duration: 0.5, type: 'spring', stiffness: 100 }}
    whileHover={{ y: -6, transition: { duration: 0.2 } }}
    className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6 hover:border-slate-700/80 hover:shadow-lg hover:shadow-black/20 transition-all duration-300 group">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <p className="text-slate-400 text-sm font-medium">{label}</p>
        <p className="text-4xl font-bold text-white mt-2">{value}</p>
        {subtitle && <p className="text-slate-500 text-xs mt-2">{subtitle}</p>}
      </div>
      <motion.div 
        whileHover={{ scale: 1.15, rotate: 8 }}
        transition={{ type: 'spring', stiffness: 300 }}
        className={`w-12 h-12 rounded-xl flex items-center justify-center bg-${color}-950/60 border border-${color}-800/40 shrink-0`}>
        <Icon className={`h-6 w-6 text-${color}-400`} />
      </motion.div>
    </div>
  </motion.div>
);

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm">
        <p className="text-slate-300 font-medium">{label}</p>
        <p className="text-indigo-400">{payload[0].value}h studied</p>
      </div>
    );
  }
  return null;
};

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [showWalkthrough, setShowWalkthrough] = useState(false);
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const seen = localStorage.getItem('learnpath_walkthrough_shown');
    if (!seen) setShowWalkthrough(true);
  }, []);
  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => dashboardAPI.get().then((r) => r.data.data),
    refetchInterval: 60000,
  });

  if (isLoading) return (
    <div className="p-6 max-w-7xl mx-auto space-y-6 animate-pulse">
      <div className="h-10 bg-slate-800 rounded-xl w-1/3" />
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => <div key={i} className="h-28 bg-slate-900 border border-slate-800 rounded-2xl" />)}
      </div>
      <div className="h-24 bg-slate-900 border border-slate-800 rounded-2xl" />
      <div className="grid lg:grid-cols-2 gap-6">
        <div className="h-48 bg-slate-900 border border-slate-800 rounded-2xl" />
        <div className="h-48 bg-slate-900 border border-slate-800 rounded-2xl" />
      </div>
    </div>
  );

  if (error || !data) return (
    <div className="flex items-center justify-center h-full min-h-screen">
      <div className="text-center max-w-md px-4">
        <p className="text-slate-400 mb-4">Could not load dashboard. Make sure the backend server is running.</p>
        <Link href="/onboarding" className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-xl text-sm">Set Up Your Profile</Link>
      </div>
    </div>
  );

  const radarData = (data.skill_gaps || []).slice(0, 6).map((g: any) => ({
    skill: g.skill_name?.split(' ')[0],
    current: g.current_level,
    target: g.target_level,
    fullMark: 5,
  }));

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {showWalkthrough && <Walkthrough onClose={() => { setShowWalkthrough(false); localStorage.setItem('learnpath_walkthrough_shown', '1'); }} /> }
      {/* Header with enhanced hero section */}
      <motion.div initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
        className="bg-linear-to-r from-indigo-900/30 to-violet-900/20 border border-indigo-700/30 rounded-2xl p-6 mb-6 relative overflow-hidden">
        {/* Decorative background elements */}
        <div className="absolute top-0 right-0 w-40 h-40 bg-indigo-500/10 rounded-full blur-3xl z-0" />
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-violet-500/10 rounded-full blur-3xl z-0" />
        
        <div className="relative z-10 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-white">
              {getGreeting()}, {data.user_name?.split(' ')[0] || 'there'}! 👋
            </h1>
            <p className="text-slate-300 mt-2">
              {data.target_role
                ? <>Your learning mission: <span className="text-indigo-300 font-semibold">{data.target_role}</span></>
                : <Link href="/onboarding" className="text-indigo-400 hover:underline">→ Set up your learning goal</Link>
              }
            </p>
          </div>
          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-3 bg-linear-to-r from-indigo-600/20 to-violet-600/20 border border-indigo-500/30 rounded-xl px-4 py-3 backdrop-blur-sm">
            <span className="text-2xl">{getStreakEmoji(data.current_streak)}</span>
            <div>
              <p className="text-white font-bold text-lg">{data.current_streak}</p>
              <p className="text-slate-400 text-xs">day streak</p>
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Overall Progress" value={`${data.overall_progress}%`} icon={TrendingUp} delay={0.1} />
        <StatCard label="Hours Learned" value={data.hours_learned} icon={Clock} subtitle="Total hours" delay={0.15} />
        <StatCard label="Skills Improved" value={data.skills_improved} icon={Zap} color="violet" delay={0.2} />
        <StatCard label="Completed" value={data.completed_resources} icon={CheckCircle} color="green" subtitle="resources" delay={0.25} />
      </div>

      {/* Progress bar */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4, duration: 0.4 }}
        className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="font-bold text-white text-lg flex items-center gap-2">
              <motion.span animate={{ scale: [1, 1.05, 1] }} transition={{ duration: 2, repeat: Infinity }}>📊</motion.span>
              Learning Progress
            </h2>
            <p className="text-slate-400 text-sm mt-1">{data.overall_progress}% toward your goal</p>
          </div>
          <Link href="/roadmap" className="text-indigo-400 hover:text-indigo-300 text-sm font-medium flex items-center gap-1 hover:gap-2 transition-all">
            View Roadmap <ChevronRight className="h-4 w-4" />
          </Link>
        </div>
        <div className="space-y-3">
          <div className="h-4 bg-slate-800 rounded-full overflow-hidden relative">
            <motion.div
              className="h-full bg-linear-to-r from-indigo-500 via-violet-500 to-indigo-500 rounded-full shadow-lg shadow-indigo-500/40"
              initial={{ width: 0 }}
              animate={{ width: `${data.overall_progress}%` }}
              transition={{ duration: 1.5, ease: 'easeOut', delay: 0.5 }}
            />
            {/* Animated shine effect */}
            <motion.div
              className="absolute inset-0 bg-linear-to-r from-transparent via-white/20 to-transparent"
              animate={{ x: ['100%', '-100%'] }}
              transition={{ duration: 2, repeat: Infinity, repeatDelay: 0.5 }}
            />
          </div>
        </div>
        <div className="flex items-center justify-between mt-4 text-xs text-slate-500">
          <span>{data.overall_progress}% complete</span>
          <span>{data.roadmap_summary?.total_weeks || 0} weeks total plan</span>
        </div>
        {data.skills_improved > 0 && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.2 }}
            className="mt-4 pt-4 border-t border-slate-700">
            <p className="text-sm text-green-400 flex items-center gap-2 font-medium">
              <motion.span animate={{ scale: [1, 1.2, 1] }} transition={{ duration: 1.5, repeat: Infinity }}>
                ✨
              </motion.span>
              You've improved {data.skills_improved} skill{data.skills_improved > 1 ? 's' : ''}! Keep the momentum going.
            </p>
          </motion.div>
        )}
      </motion.div>

      {/* Two columns: NBA + Today's Focus */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Next Best Action - Premium card */}
        <motion.div initial={{ opacity: 0, x: -20, scale: 0.96 }} animate={{ opacity: 1, x: 0, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="lg:row-span-1 bg-linear-to-br from-indigo-900/60 via-indigo-800/40 to-violet-900/50 border border-indigo-600/40 rounded-2xl p-6 relative overflow-hidden shadow-xl shadow-indigo-500/10 hover:shadow-2xl hover:shadow-indigo-500/20 transition-all duration-300">
          <div className="absolute top-0 right-0 w-40 h-40 bg-indigo-400/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-20 -left-20 w-60 h-60 bg-violet-400/5 rounded-full blur-3xl" />
          <div className="relative">
            <div className="flex items-center gap-3 mb-4">
              <motion.div 
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-10 h-10 rounded-lg bg-linear-to-br from-indigo-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-500/40">
                <Zap className="h-5 w-5 text-white" />
              </motion.div>
              <h2 className="font-bold text-white text-lg">Next Best Action</h2>
            </div>
            {data.next_best_action ? (
              <>
                <div className="mb-5">
                  <h3 className="text-2xl font-bold text-white mb-2">{data.next_best_action.title}</h3>
                  <p className="text-slate-200 text-sm leading-relaxed">{data.next_best_action.description}</p>
                </div>
                <div className="flex flex-wrap items-center gap-4 mb-5">
                  <div className="flex items-center gap-2 text-slate-300 text-sm bg-black/20 px-3 py-1.5 rounded-lg backdrop-blur-sm">
                    <Clock className="h-4 w-4" />
                    <span>~{data.next_best_action.estimated_minutes} min</span>
                  </div>
                  {data.next_best_action.skill && (
                    <div className="flex items-center gap-2 text-slate-300 text-sm bg-black/20 px-3 py-1.5 rounded-lg backdrop-blur-sm">
                      <Target className="h-4 w-4" />
                      <span>{data.next_best_action.skill}</span>
                    </div>
                  )}
                </div>
                <div className="bg-indigo-950/80 border border-indigo-600/30 rounded-xl p-4 mb-5 backdrop-blur-sm">
                  <p className="text-xs text-indigo-300 font-bold mb-1.5 flex items-center gap-1.5">
                    <span>💡</span> Why this action?
                  </p>
                  <p className="text-slate-200 text-sm leading-relaxed">&ldquo;{data.next_best_action.reason}&rdquo;</p>
                </div>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}>
                  <Link href={data.next_best_action.type === 'assessment' ? '/assessment' : '/recommendations'}
                    className="w-full bg-linear-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white text-sm font-semibold px-4 py-3.5 rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/30">
                    <Play className="h-4 w-4" />
                    Start Learning Now
                  </Link>
                </motion.div>
              </>
            ) : (
              <div className="text-slate-200 text-sm">
                <p className="mb-4">Complete onboarding to get a personalized next step.</p>
                <Link href="/onboarding" className="inline-flex bg-linear-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white text-sm font-medium px-4 py-2.5 rounded-lg transition-all shadow-lg shadow-indigo-500/30">Set up your goal →</Link>
              </div>
            )}
          </div>
        </motion.div>

        {/* Today's Focus */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6 hover:border-slate-700/50 transition-all duration-300">
          <div className="flex items-center gap-3 mb-5">
            <motion.div
              animate={{ rotate: [0, 5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-10 h-10 rounded-lg bg-indigo-900/60 border border-indigo-700/40 flex items-center justify-center">
              <Target className="h-5 w-5 text-indigo-400" />
            </motion.div>
            <h2 className="font-bold text-white text-lg">Today's Focus</h2>
          </div>
          <div className="space-y-2">
            {(data.today_focus || []).map((task: any, i: number) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.35 + (i * 0.08) }}
                whileHover={{ x: 4 }}
                className="flex items-start gap-3 p-3.5 bg-slate-800/60 hover:bg-slate-800/80 border border-slate-700/50 rounded-xl transition-all duration-200 cursor-pointer group">
                <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 text-lg group-hover:scale-110 transition-transform ${
                  task.type === 'lesson' ? 'bg-indigo-900/60' : task.type === 'quiz' ? 'bg-violet-900/60' : 'bg-orange-900/60'
                }`}>
                  {task.type === 'lesson' ? '📚' : task.type === 'quiz' ? '✏️' : '🔨'}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-semibold">{task.title}</p>
                  <p className="text-slate-400 text-xs mt-0.5">{task.estimated_minutes} min</p>
                </div>
              </motion.div>
            ))}
            {(!data.today_focus || data.today_focus.length === 0) && (
              <p className="text-slate-500 text-sm py-4 text-center">Complete your profile setup to get daily tasks.</p>
            )}
          </div>
        </motion.div>
      </div>

      {/* Charts row */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Weekly Activity */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45 }}
          className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6 hover:border-slate-700/50 transition-all">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-lg">📈</span>
            <h2 className="font-bold text-white text-lg">Weekly Activity</h2>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data.weekly_activity || []}>
              <XAxis dataKey="day" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="hours" fill="#6366f1" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Skill Radar */}
        {radarData.length > 0 ? (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6 hover:border-slate-700/50 transition-all">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-lg">🎯</span>
              <h2 className="font-bold text-white text-lg">Skill Gaps Overview</h2>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="skill" tick={{ fill: '#64748b', fontSize: 11 }} />
                <Radar name="Target" dataKey="target" stroke="#6366f1" fill="#6366f1" fillOpacity={0.1} />
                <Radar name="Current" dataKey="current" stroke="#22c55e" fill="#22c55e" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
            <div className="flex gap-4 justify-center mt-4 text-xs">
              <span className="flex items-center gap-1.5 text-slate-400"><span className="w-3 h-1 bg-green-500 inline-block rounded" /> Your level</span>
              <span className="flex items-center gap-1.5 text-slate-400"><span className="w-3 h-1 bg-indigo-500 inline-block rounded" /> Target level</span>
            </div>
          </motion.div>
        ) : (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6 flex items-center justify-center">
            <div className="text-center text-slate-400">
              <Target className="h-12 w-12 mx-auto mb-3 text-slate-700" />
              <p className="text-sm">Complete onboarding to see your skill analysis</p>
              <Link href="/onboarding" className="mt-3 inline-block text-indigo-400 hover:underline text-sm font-medium">Get Started →</Link>
            </div>
          </motion.div>
        )}
      </div>

      {/* Top Recommendations Preview */}
      {data.recent_recommendations?.length > 0 && (
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-slate-900/80 backdrop-blur border border-slate-800/50 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-bold text-white text-lg flex items-center gap-2">
              <motion.span animate={{ scale: [1, 1.1, 1] }} transition={{ duration: 2, repeat: Infinity }}>⭐</motion.span> 
              Recommended For You
            </h2>
            <Link href="/recommendations" className="text-indigo-400 hover:text-indigo-300 text-sm font-medium flex items-center gap-1 hover:gap-2 transition-all">
              See all <ChevronRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="grid sm:grid-cols-3 gap-4">
            {data.recent_recommendations.map((r: any, idx: number) => (
              <motion.a 
                key={r.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.55 + (idx * 0.05) }}
                whileHover={{ y: -4, transition: { duration: 0.2 } }}
                href={r.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex flex-col bg-slate-800/60 hover:bg-slate-800/90 border border-slate-700/50 hover:border-indigo-500/50 rounded-xl p-4 transition-all group">
                <div className="flex items-center justify-between mb-3">
                  <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${r.score >= 70 ? 'bg-green-900/60 text-green-300' : 'bg-indigo-900/60 text-indigo-300'}`}>
                    {Math.round(r.score)}% match
                  </span>
                  <span className="text-slate-400 text-xs group-hover:text-slate-300">{r.is_free ? '🆓 Free' : '💰'}</span>
                </div>
                <p className="text-white text-sm font-semibold line-clamp-2 flex-1 group-hover:text-indigo-200">{r.title}</p>
                <p className="text-slate-400 text-xs mt-3">{r.provider} · {r.duration_hours}h</p>
              </motion.a>
            ))}
          </div>
        </motion.div>
      )}

      {/* Quick links */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.55 }}
        className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { href: '/roadmap', label: 'My Roadmap', icon: Map, color: 'indigo' },
          { href: '/chat', label: 'AI Mentor', icon: MessageCircle, color: 'violet' },
          { href: '/skills', label: 'Skill Gaps', icon: TrendingUp, color: 'blue' },
          { href: '/assessment', label: 'Take Quiz', icon: BookOpen, color: 'green' },
        ].map((item, idx) => (
          <motion.div
            key={item.href}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6 + (idx * 0.05) }}
            whileHover={{ y: -4 }}>
            <Link href={item.href}
              className={`flex flex-col items-center justify-center gap-2.5 p-5 bg-slate-900/80 backdrop-blur border border-slate-800/50 hover:border-${item.color}-500/50 rounded-2xl transition-all group h-full`}>
              <motion.div whileHover={{ scale: 1.15, rotate: 8 }} className="relative">
                <item.icon className={`h-6 w-6 text-${item.color}-400 group-hover:text-${item.color}-300`} />
              </motion.div>
              <span className="text-slate-300 group-hover:text-white text-sm font-semibold text-center">{item.label}</span>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
