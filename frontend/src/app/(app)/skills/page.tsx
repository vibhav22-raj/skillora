'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { skillsAPI } from '@/lib/api';
import { TrendingUp, AlertCircle, ChevronRight } from 'lucide-react';
import { getPriorityColor } from '@/lib/utils';
import type { SkillGap } from '@/types';
import Link from 'next/link';

const PriorityBadge = ({ priority }: { priority: string }) => (
  <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border capitalize ${getPriorityColor(priority)}`}>
    {priority}
  </span>
);

function SkillGapBar({ gap }: { gap: SkillGap }) {
  const gapPct = (gap.current_level / gap.target_level) * 100;
  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="text-white font-semibold">{gap.skill_name}</h3>
          {gap.description && <p className="text-slate-400 text-sm mt-0.5">{gap.description}</p>}
        </div>
        <PriorityBadge priority={gap.priority} />
      </div>

      {/* Level bar */}
      <div className="mb-4">
        <div className="flex justify-between text-xs text-slate-400 mb-1.5">
          <span>Current: {gap.current_level}/5</span>
          <span>Target: {gap.target_level}/5</span>
        </div>
        <div className="relative h-3 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            className="absolute left-0 top-0 h-full rounded-full bg-gradient-to-r from-indigo-500 to-violet-500"
            initial={{ width: 0 }}
            animate={{ width: `${gapPct}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
          {/* Target marker */}
          <div className="absolute top-0 h-full w-0.5 bg-white/30" style={{ left: `${(gap.target_level / 5) * 100}%` }} />
        </div>
        <div className="flex justify-between text-xs text-slate-500 mt-1">
          <span>Beginner</span>
          <span>Expert</span>
        </div>
      </div>

      {/* Gap indicator */}
      <div className={`text-sm font-medium mb-3 ${gap.gap === 0 ? 'text-green-400' : gap.priority === 'critical' ? 'text-red-400' : 'text-amber-400'}`}>
        {gap.gap === 0 ? '✅ No gap — skill requirement met!' : `Gap: ${gap.gap} levels to close`}
      </div>

      {/* Recommendations */}
      {gap.recommended_resources?.length > 0 && (
        <div>
          <p className="text-slate-500 text-xs mb-2">Top resources to close this gap:</p>
          <div className="space-y-1.5">
            {gap.recommended_resources.slice(0, 2).map((r, i) => (
              <div key={i} className="text-slate-400 text-xs flex items-center gap-1.5">
                <ChevronRight className="h-3 w-3 text-indigo-500 flex-shrink-0" />
                {r}
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

export default function SkillsPage() {
  const [filter, setFilter] = useState<'all' | 'critical' | 'high' | 'medium' | 'low'>('all');

  const { data: gaps, isLoading } = useQuery({
    queryKey: ['skill-gaps'],
    queryFn: () => skillsAPI.getGaps().then((r) => r.data.data),
  });

  const filteredGaps = (gaps || []).filter((g: SkillGap) => filter === 'all' || g.priority === filter);

  const criticalCount = (gaps || []).filter((g: SkillGap) => g.priority === 'critical').length;
  const highCount = (gaps || []).filter((g: SkillGap) => g.priority === 'high').length;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <TrendingUp className="h-6 w-6 text-indigo-400" />
          Skills & Gaps Analysis
        </h1>
        <p className="text-slate-400 mt-1">See exactly what skills you need to reach your target role.</p>
      </div>

      {/* Alert if critical gaps */}
      {criticalCount > 0 && (
        <div className="bg-red-950/50 border border-red-800/50 rounded-2xl p-4 mb-6 flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-red-300 font-medium">{criticalCount} Critical Gap{criticalCount > 1 ? 's' : ''} Detected</p>
            <p className="text-red-400/70 text-sm mt-0.5">Focus on these first — they block your progress to the next phase.</p>
          </div>
        </div>
      )}

      {/* Summary cards */}
      {!isLoading && gaps && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          {[
            { label: 'Critical', value: criticalCount, color: 'red' },
            { label: 'High', value: highCount, color: 'orange' },
            { label: 'Medium', value: (gaps || []).filter((g: SkillGap) => g.priority === 'medium').length, color: 'yellow' },
            { label: 'Resolved', value: (gaps || []).filter((g: SkillGap) => g.gap === 0).length, color: 'green' },
          ].map((item) => (
            <div key={item.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-center">
              <p className={`text-2xl font-bold text-${item.color}-400`}>{item.value}</p>
              <p className="text-slate-500 text-sm">{item.label}</p>
            </div>
          ))}
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap mb-5">
        {(['all', 'critical', 'high', 'medium', 'low'] as const).map((f) => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all capitalize ${
              filter === f ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700'
            }`}>
            {f} {f !== 'all' && `(${(gaps || []).filter((g: SkillGap) => g.priority === f).length})`}
          </button>
        ))}
      </div>

      {/* Gaps list */}
      {isLoading ? (
        <div className="space-y-4">
          {[1,2,3,4].map((i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse">
              <div className="h-5 bg-slate-700 rounded w-1/3 mb-3" />
              <div className="h-3 bg-slate-700 rounded-full" />
            </div>
          ))}
        </div>
      ) : filteredGaps.length === 0 ? (
        <div className="text-center py-16">
          <TrendingUp className="h-16 w-16 text-slate-700 mx-auto mb-4" />
          <p className="text-slate-400 text-lg">No gaps found for this filter.</p>
          <Link href="/onboarding" className="mt-4 inline-block text-indigo-400 hover:underline">
            Set up your profile to see skill gaps →
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredGaps.map((gap: SkillGap) => (
            <SkillGapBar key={gap.skill_name} gap={gap} />
          ))}
        </div>
      )}
    </div>
  );
}
