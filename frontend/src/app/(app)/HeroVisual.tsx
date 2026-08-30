'use client';

import { motion } from 'framer-motion';
import { Target, Award, GitBranch, Map, TrendingUp } from 'lucide-react';

const steps = [
  { icon: Target, title: 'Goal', subtitle: 'Target Career Role', color: 'from-violet-500 to-indigo-500', badge: 'Step 1' },
  { icon: Award, title: 'Skills', subtitle: 'Self & Quiz Ratings', color: 'from-blue-500 to-cyan-500', badge: 'Step 2' },
  { icon: GitBranch, title: 'Skill Gap', subtitle: 'Priority Gap Matrix', color: 'from-amber-500 to-orange-500', badge: 'Step 3' },
  { icon: Map, title: 'Personalized Roadmap', subtitle: 'Phased Milestones', color: 'from-purple-500 to-pink-500', badge: 'Step 4' },
  { icon: TrendingUp, title: 'Progress & Next Action', subtitle: 'Adaptive AI Tracking', color: 'from-emerald-500 to-teal-500', badge: 'Step 5' },
];

export default function HeroVisual() {
  return (
    <div className="w-full max-w-md mx-auto p-4 rounded-3xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 right-0 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-48 h-48 bg-violet-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center justify-between mb-4 px-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400 flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
          Skillora Learning Pipeline
        </span>
        <span className="text-[11px] text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded-full border border-slate-700/50">
          Deterministic + AI
        </span>
      </div>

      <div className="space-y-2.5 relative">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * idx, duration: 0.4 }}
              className="flex items-center gap-3.5 p-2.5 rounded-2xl bg-slate-850/70 border border-slate-800/60 hover:border-slate-700/80 transition-all group"
            >
              <div className={`w-9 h-9 rounded-xl bg-gradient-to-br ${step.color} flex items-center justify-center text-white shadow-md shadow-black/20 shrink-0`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-semibold text-white truncate">{step.title}</h4>
                  <span className="text-[10px] font-medium text-slate-400 px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700/40">
                    {step.badge}
                  </span>
                </div>
                <p className="text-xs text-slate-400 truncate">{step.subtitle}</p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

