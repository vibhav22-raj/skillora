'use client';

import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { recommendationsAPI, resourcesAPI } from '@/lib/api';
import { Star, ExternalLink, ThumbsUp, ThumbsDown, Clock, BookOpen, Zap } from 'lucide-react';
import { getFormatIcon, getDifficultyLabel, truncate } from '@/lib/utils';
import type { LearningResource } from '@/types';
import toast from 'react-hot-toast';
import ReactMarkdown from 'react-markdown';

const ScoreBar = ({ label, value }: { label: string; value: number }) => (
  <div className="mb-1.5">
    <div className="flex justify-between text-xs mb-0.5">
      <span className="text-slate-400">{label}</span>
      <span className="text-slate-300">{Math.round(value * 100)}%</span>
    </div>
    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${value * 100}%` }} />
    </div>
  </div>
);

function ResourceCard({ resource, index }: { resource: LearningResource & { explanation?: string }; index: number }) {
  const [expanded, setExpanded] = useState(false);
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);

  const feedbackMutation = useMutation({
    mutationFn: (helpful: boolean) => recommendationsAPI.submitFeedback(resource.id, { helpful }),
    onSuccess: () => toast.success('Feedback recorded! ✨'),
  });

  const startMutation = useMutation({
    mutationFn: () => resourcesAPI.start(resource.id),
    onSuccess: () => toast.success('Resource started! Good luck 🎓'),
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08 }}
      className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 transition-all">
      {/* Score badge */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`text-sm font-bold px-3 py-1 rounded-full ${
            (resource.score || 0) >= 80 ? 'bg-green-900/50 text-green-400' :
            (resource.score || 0) >= 60 ? 'bg-indigo-900/50 text-indigo-400' : 'bg-slate-800 text-slate-400'
          }`}>
            {Math.round(resource.score || 0)}% match
          </span>
          {resource.is_free && (
            <span className="text-xs bg-emerald-900/50 text-emerald-400 border border-emerald-700/50 px-2 py-0.5 rounded-full">Free</span>
          )}
          <span className="text-slate-500 text-xs">{getFormatIcon(resource.format || '')} {resource.format}</span>
        </div>
        <div className="text-right flex-shrink-0">
          <div className="text-white font-bold text-lg">{index + 1}</div>
          <div className="text-slate-500 text-xs">ranked</div>
        </div>
      </div>

      {/* Title & provider */}
      <h3 className="text-white font-semibold text-lg leading-snug mb-1">{resource.title}</h3>
      <p className="text-slate-400 text-sm mb-3">{resource.provider} · {resource.duration_hours}h · {getDifficultyLabel(resource.difficulty)}</p>

      {/* Skills */}
      <div className="flex flex-wrap gap-1.5 mb-4">
        {(resource.skills || []).slice(0, 4).map((s) => (
          <span key={s} className="bg-slate-800 text-slate-300 text-xs px-2.5 py-1 rounded-lg">{s}</span>
        ))}
      </div>

      {/* AI Explanation */}
      {resource.explanation && (
        <div className="bg-indigo-950/50 border border-indigo-800/50 rounded-xl p-3 mb-4">
          <p className="text-xs text-indigo-400 font-medium mb-1 flex items-center gap-1">
            <Zap className="h-3.5 w-3.5" /> Why this is recommended for you
          </p>
          <div className="text-slate-300 text-sm leading-relaxed prose-ai">
            <ReactMarkdown>{resource.explanation}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Score breakdown toggle */}
      <button onClick={() => setExpanded(!expanded)}
        className="text-xs text-slate-500 hover:text-slate-300 transition-colors mb-4 underline">
        {expanded ? 'Hide' : 'Show'} score breakdown
      </button>

      {expanded && (
        <div className="mb-4 p-3 bg-slate-800 rounded-xl">
          <ScoreBar label="Goal Relevance" value={resource.goal_relevance || 0} />
          <ScoreBar label="Skill Gap Coverage" value={resource.skill_gap_relevance || 0} />
          <ScoreBar label="Prerequisite Fit" value={resource.prerequisite_fit || 0} />
          <ScoreBar label="Difficulty Match" value={resource.difficulty_fit || 0} />
          <ScoreBar label="Time Fit" value={resource.time_fit || 0} />
          <ScoreBar label="Learning Style" value={resource.preference_fit || 0} />
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-3">
        <a href={resource.url} target="_blank" rel="noopener noreferrer"
          className="flex-1 flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-xl transition-all text-sm">
          <ExternalLink className="h-4 w-4" />
          Open Resource
        </a>
        <button onClick={() => startMutation.mutate()}
          className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2.5 rounded-xl text-sm transition-all">
          <BookOpen className="h-4 w-4" />
          Start
        </button>
        <div className="flex gap-1">
          <button onClick={() => { setFeedback('up'); feedbackMutation.mutate(true); }}
            className={`p-2 rounded-lg transition-all ${feedback === 'up' ? 'bg-green-900 text-green-400' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>
            <ThumbsUp className="h-4 w-4" />
          </button>
          <button onClick={() => { setFeedback('down'); feedbackMutation.mutate(false); }}
            className={`p-2 rounded-lg transition-all ${feedback === 'down' ? 'bg-red-900 text-red-400' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}>
            <ThumbsDown className="h-4 w-4" />
          </button>
        </div>
      </div>
    </motion.div>
  );
}

export default function RecommendationsPage() {
  const [limit, setLimit] = useState(10);

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['recommendations', limit],
    queryFn: () => recommendationsAPI.get(limit).then((r) => r.data.data),
  });

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Star className="h-6 w-6 text-amber-400" />
            AI Recommendations
          </h1>
          <p className="text-slate-400 mt-1">Personalized resources ranked by how well they match your exact situation.</p>
        </div>
        <button onClick={() => refetch()}
          className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-xl text-sm transition-all">
          <Zap className="h-4 w-4" />
          Refresh
        </button>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse">
              <div className="h-4 bg-slate-700 rounded w-1/3 mb-3" />
              <div className="h-6 bg-slate-700 rounded w-2/3 mb-2" />
              <div className="h-4 bg-slate-700 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {(data || []).map((resource: LearningResource, i: number) => (
            <ResourceCard key={resource.id} resource={resource} index={i} />
          ))}
          {data && data.length >= limit && (
            <div className="text-center py-4">
              <button onClick={() => setLimit((l) => l + 10)}
                className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-6 py-3 rounded-xl text-sm transition-all">
                Load More Recommendations
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
