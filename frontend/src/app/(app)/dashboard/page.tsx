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

const StatCard = ({ label, value, icon: Icon, color = 'indigo', subtitle = '' }: any) => (
  <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}
    className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
    <div className="flex items-start justify-between">
      <div>
        <p className="text-slate-400 text-sm">{label}</p>
        <p className="text-3xl font-bold text-white mt-1">{value}</p>
        {subtitle && <p className="text-slate-500 text-xs mt-1">{subtitle}</p>}
      </div>
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center bg-${color}-950`}>
        <Icon className={`h-5 w-5 text-${color}-400`} />
      </div>
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
    <div className="flex items-center justify-center h-full min-h-screen">
      <div className="text-center">
        <div className="h-10 w-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-slate-400">Loading your dashboard...</p>
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
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">
            {getGreeting()}, {data.user_name?.split(' ')[0] || 'there'}! 👋
          </h1>
          <p className="text-slate-400 mt-1">
            {data.target_role
              ? <>Working toward: <span className="text-indigo-400 font-medium">{data.target_role}</span></>
              : <Link href="/onboarding" className="text-indigo-400 hover:underline">→ Set up your learning goal</Link>
            }
          </p>
        </div>
        <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2">
          <span className="text-xl">{getStreakEmoji(data.current_streak)}</span>
          <div>
            <p className="text-white font-bold">{data.current_streak} day streak</p>
            <p className="text-slate-500 text-xs">Keep it going!</p>
          </div>
          <button onClick={() => { if (typeof window !== 'undefined') { localStorage.removeItem('learnpath_walkthrough_shown'); } setShowWalkthrough(true); }} className="ml-4 bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 px-3 py-2 rounded-lg text-sm">
            Restart Tour
          </button>
        </div>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Overall Progress" value={`${data.overall_progress}%`} icon={TrendingUp} />
        <StatCard label="Hours Learned" value={data.hours_learned} icon={Clock} subtitle="Total hours" />
        <StatCard label="Skills Improved" value={data.skills_improved} icon={Zap} color="violet" />
        <StatCard label="Completed" value={data.completed_resources} icon={CheckCircle} color="green" subtitle="resources" />
      </div>

      {/* Progress bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-semibold text-white">Learning Progress</h2>
          <Link href="/roadmap" className="text-indigo-400 hover:text-indigo-300 text-sm flex items-center gap-1">
            View Roadmap <ChevronRight className="h-4 w-4" />
          </Link>
        </div>
        <div className="h-3 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${data.overall_progress}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
        </div>
        <div className="flex justify-between mt-2 text-xs text-slate-500">
          <span>{data.overall_progress}% complete</span>
          <span>{data.roadmap_summary?.total_weeks || 0} weeks total plan</span>
        </div>
      </div>

      {/* Two columns: NBA + Today's Focus */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Next Best Action */}
        {data.next_best_action && (
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}
            className="bg-gradient-to-br from-indigo-900/50 to-violet-900/50 border border-indigo-700/50 rounded-2xl p-5">
            <div className="flex items-center gap-2 mb-3">
              <Zap className="h-5 w-5 text-indigo-400" />
              <h2 className="font-semibold text-white">Next Best Action</h2>
            </div>
            <h3 className="text-lg font-bold text-white mb-2">{data.next_best_action.title}</h3>
            <p className="text-slate-300 text-sm leading-relaxed mb-4">{data.next_best_action.description}</p>
            <div className="flex items-center justify-between">
              <span className="text-slate-400 text-sm">⏱ ~{data.next_best_action.estimated_minutes} min</span>
              <Link href={data.next_best_action.type === 'assessment' ? '/assessment' : '/recommendations'}
                className="bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-all flex items-center gap-1">
                <Play className="h-4 w-4" />
                Start Now
              </Link>
            </div>
            <p className="text-slate-500 text-xs mt-3 italic">"{data.next_best_action.reason}"</p>
          </motion.div>
        )}

        {/* Today's Focus */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
          className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <div className="flex items-center gap-2 mb-4">
            <Target className="h-5 w-5 text-indigo-400" />
            <h2 className="font-semibold text-white">Today's Focus</h2>
          </div>
          <div className="space-y-3">
            {(data.today_focus || []).map((task: any, i: number) => (
              <div key={i} className="flex items-start gap-3 p-3 bg-slate-800 rounded-xl">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                  task.type === 'lesson' ? 'bg-indigo-900' : task.type === 'quiz' ? 'bg-violet-900' : 'bg-orange-900'
                }`}>
                  {task.type === 'lesson' ? '📚' : task.type === 'quiz' ? '✏️' : '🔨'}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-medium truncate">{task.title}</p>
                  <p className="text-slate-400 text-xs">{task.estimated_minutes} min</p>
                </div>
              </div>
            ))}
            {(!data.today_focus || data.today_focus.length === 0) && (
              <p className="text-slate-500 text-sm">Complete your profile setup to get daily tasks.</p>
            )}
          </div>
        </motion.div>
      </div>

      {/* Charts row */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Weekly Activity */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <h2 className="font-semibold text-white mb-4">Weekly Activity</h2>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={data.weekly_activity || []}>
              <XAxis dataKey="day" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="hours" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Skill Radar */}
        {radarData.length > 0 ? (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="font-semibold text-white mb-4">Skill Gaps Overview</h2>
            <ResponsiveContainer width="100%" height={160}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="skill" tick={{ fill: '#64748b', fontSize: 11 }} />
                <Radar name="Target" dataKey="target" stroke="#6366f1" fill="#6366f1" fillOpacity={0.1} />
                <Radar name="Current" dataKey="current" stroke="#22c55e" fill="#22c55e" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
            <div className="flex gap-4 justify-center mt-2 text-xs">
              <span className="flex items-center gap-1 text-slate-400"><span className="w-3 h-1 bg-green-500 inline-block rounded" /> Your level</span>
              <span className="flex items-center gap-1 text-slate-400"><span className="w-3 h-1 bg-indigo-500 inline-block rounded" /> Target level</span>
            </div>
          </div>
        ) : (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex items-center justify-center">
            <div className="text-center text-slate-500">
              <Target className="h-10 w-10 mx-auto mb-3 text-slate-700" />
              <p className="text-sm">Complete onboarding to see your skill analysis</p>
              <Link href="/onboarding" className="mt-3 inline-block text-indigo-400 hover:underline text-sm">Get Started →</Link>
            </div>
          </div>
        )}
      </div>

      {/* Top Recommendations Preview */}
      {data.recent_recommendations?.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-white flex items-center gap-2"><Star className="h-5 w-5 text-indigo-400" /> Recommended For You</h2>
            <Link href="/recommendations" className="text-indigo-400 hover:text-indigo-300 text-sm flex items-center gap-1">
              See all <ChevronRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="grid sm:grid-cols-3 gap-4">
            {data.recent_recommendations.map((r: any) => (
              <a key={r.id} href={r.url} target="_blank" rel="noopener noreferrer"
                className="flex flex-col bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-indigo-500 rounded-xl p-4 transition-all group">
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${r.score >= 70 ? 'bg-green-900/50 text-green-400' : 'bg-indigo-900/50 text-indigo-400'}`}>
                    {Math.round(r.score)}% match
                  </span>
                  <span className="text-slate-500 text-xs">{r.is_free ? '🆓 Free' : '💰 Paid'}</span>
                </div>
                <p className="text-white text-sm font-semibold line-clamp-2 flex-1">{r.title}</p>
                <p className="text-slate-400 text-xs mt-2">{r.provider} · {r.duration_hours}h</p>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Quick links */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { href: '/roadmap', label: 'My Roadmap', icon: Map, color: 'indigo' },
          { href: '/chat', label: 'AI Mentor', icon: MessageCircle, color: 'violet' },
          { href: '/skills', label: 'Skill Gaps', icon: TrendingUp, color: 'blue' },
          { href: '/assessment', label: 'Take Quiz', icon: BookOpen, color: 'green' },
        ].map((item) => (
          <Link key={item.href} href={item.href}
            className={`flex flex-col items-center justify-center gap-2 p-4 bg-slate-900 border border-slate-800 hover:border-${item.color}-500 rounded-2xl transition-all group`}>
            <item.icon className={`h-6 w-6 text-${item.color}-400 group-hover:scale-110 transition-transform`} />
            <span className="text-slate-300 text-sm font-medium">{item.label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
