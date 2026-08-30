'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { learningPathAPI, dashboardAPI } from '@/lib/api';
import { useState } from 'react';
import { Map, CheckCircle, Clock, ChevronDown, ChevronUp, BookOpen, Folder, Zap, Star, ExternalLink, Play, Sparkles, X, Video, FileText, Code2 } from 'lucide-react';
import toast from 'react-hot-toast';
import Link from 'next/link';
import type { Roadmap, RoadmapPhase } from '@/types';
import { cn } from '@/lib/utils';
import { getTopicGuide, TopicGuide } from '@/lib/roadmapTopics';

const statusColors: Record<string, string> = {
  completed: 'bg-green-900/50 text-green-400 border-green-700/50',
  in_progress: 'bg-indigo-900/50 text-indigo-400 border-indigo-700/50',
  not_started: 'bg-slate-800 text-slate-400 border-slate-700',
};

const statusLabels: Record<string, string> = {
  completed: '✅ Completed',
  in_progress: '🔄 In Progress',
  not_started: '⏳ Not Started',
};

function TopicModal({ topicName, onClose }: { topicName: string; onClose: () => void }) {
  const guide: TopicGuide = getTopicGuide(topicName);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-xs">
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 10 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 10 }}
        className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl relative"
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-semibold uppercase tracking-wider px-2.5 py-1 rounded-md bg-indigo-950 text-indigo-300 border border-indigo-800">
            {guide.category}
          </span>
          <span className="text-xs text-slate-400">Roadmap Topic Guide</span>
        </div>
        <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-amber-400" />
          {guide.topic}
        </h2>
        <p className="text-slate-300 text-sm leading-relaxed mb-4">{guide.summary}</p>

        {/* Why learn this */}
        <div className="bg-indigo-950/40 border border-indigo-800/40 rounded-xl p-4 mb-6">
          <p className="text-xs font-semibold text-indigo-300 uppercase tracking-wider mb-1 flex items-center gap-1.5">
            <span>💡</span> Why this matters in your roadmap
          </p>
          <p className="text-slate-200 text-sm leading-relaxed">{guide.why_it_matters}</p>
        </div>

        {/* Official Docs & Articles */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
            <FileText className="h-4 w-4 text-emerald-400" />
            Official Documentation & Guides
          </h3>
          <div className="space-y-2.5">
            {guide.articles.map((art, i) => (
              <a
                key={i}
                href={art.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 hover:border-emerald-500/50 rounded-xl transition-all group"
              >
                <div className="min-w-0 flex-1 pr-3">
                  <p className="text-white text-sm font-medium group-hover:text-emerald-300 transition-colors truncate">
                    {art.title}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {art.provider} {art.duration && `• ${art.duration}`}
                  </p>
                </div>
                <span className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-950/60 border border-emerald-800/60 text-emerald-300 flex items-center gap-1 shrink-0 group-hover:bg-emerald-900 transition-colors">
                  <ExternalLink className="h-3.5 w-3.5" /> Read
                </span>
              </a>
            ))}
          </div>
        </div>

        {/* YouTube Tutorials */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
            <Video className="h-4 w-4 text-red-400" />
            Top YouTube Video Tutorials
          </h3>
          <div className="space-y-2.5">
            {guide.youtube.map((vid, i) => (
              <a
                key={i}
                href={vid.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 hover:border-red-500/50 rounded-xl transition-all group"
              >
                <div className="min-w-0 flex-1 pr-3">
                  <p className="text-white text-sm font-medium group-hover:text-red-300 transition-colors truncate">
                    {vid.title}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Channel: <span className="text-slate-300 font-medium">{vid.provider}</span> {vid.duration && `• ${vid.duration}`}
                  </p>
                </div>
                <span className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-red-950/60 border border-red-800/60 text-red-300 flex items-center gap-1.5 shrink-0 group-hover:bg-red-900 transition-colors">
                  <Play className="h-3 w-3 fill-current" /> Watch Video
                </span>
              </a>
            ))}
          </div>
        </div>

        {/* Practice Exercises */}
        {guide.practice.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
              <Code2 className="h-4 w-4 text-cyan-400" />
              Interactive Practice & Challenges
            </h3>
            <div className="space-y-2.5">
              {guide.practice.map((prac, i) => (
                <a
                  key={i}
                  href={prac.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-3.5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 hover:border-cyan-500/50 rounded-xl transition-all group"
                >
                  <div className="min-w-0 flex-1 pr-3">
                    <p className="text-white text-sm font-medium group-hover:text-cyan-300 transition-colors truncate">
                      {prac.title}
                    </p>
                    <p className="text-xs text-slate-400 mt-0.5">{prac.provider}</p>
                  </div>
                  <span className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-cyan-950/60 border border-cyan-800/60 text-cyan-300 flex items-center gap-1 shrink-0 group-hover:bg-cyan-900 transition-colors">
                    <ExternalLink className="h-3.5 w-3.5" /> Practice
                  </span>
                </a>
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

function PhaseCard({ phase, index, onSelectTopic }: { phase: RoadmapPhase; index: number; onSelectTopic: (topic: string) => void }) {
  const [expanded, setExpanded] = useState(phase.status === 'in_progress');

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.07 }}
      className={cn(
        'border rounded-2xl overflow-hidden transition-all',
        phase.status === 'in_progress' ? 'border-indigo-600/50' :
        phase.status === 'completed' ? 'border-green-700/30' : 'border-slate-800'
      )}>
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-4 p-5 bg-slate-900 hover:bg-slate-800/50 transition-colors text-left">
        {/* Phase number */}
        <div className={cn(
          'w-10 h-10 rounded-xl flex items-center justify-center text-sm font-bold flex-shrink-0',
          phase.status === 'completed' ? 'bg-green-900 text-green-400' :
          phase.status === 'in_progress' ? 'bg-indigo-900 text-indigo-400' : 'bg-slate-800 text-slate-500'
        )}>
          {phase.status === 'completed' ? <CheckCircle className="h-5 w-5" /> : phase.phase_number}
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="text-white font-semibold">{phase.title}</h3>
            <span className={cn('text-xs px-2 py-0.5 rounded-full border', statusColors[phase.status])}>
              {statusLabels[phase.status]}
            </span>
          </div>
          <div className="flex items-center gap-4 mt-1 text-sm text-slate-400">
            <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> {phase.weeks}w</span>
            <span>{phase.skills.slice(0, 3).join(', ')}{phase.skills.length > 3 ? '...' : ''}</span>
          </div>
        </div>

        {expanded ? <ChevronUp className="h-5 w-5 text-slate-400 flex-shrink-0" /> : <ChevronDown className="h-5 w-5 text-slate-400 flex-shrink-0" />}
      </button>

      {expanded && (
        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }}
          className="px-5 pb-5 bg-slate-900 border-t border-slate-800">
          <p className="text-slate-300 text-sm mt-4 mb-5 leading-relaxed">{phase.description}</p>

          {/* Skills */}
          <div className="mb-5">
            <div className="flex items-center justify-between mb-2">
              <p className="text-slate-400 text-xs font-medium uppercase tracking-wider">Topics & Skills (Click to view resources & YouTube)</p>
            </div>
            <div className="flex flex-wrap gap-2">
              {phase.skills.map((s) => (
                <button
                  key={s}
                  onClick={() => onSelectTopic(s)}
                  className="bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 hover:text-white border border-indigo-800/80 hover:border-indigo-600 text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all shadow-xs group"
                >
                  <span>{s}</span>
                  <span className="text-[10px] text-indigo-400 group-hover:text-indigo-200">📚 🎥 →</span>
                </button>
              ))}
            </div>
          </div>

          {/* Resources */}
          {phase.resources?.length > 0 && (
            <div className="mb-4">
              <p className="text-slate-400 text-xs font-medium mb-2 uppercase tracking-wider flex items-center gap-1">
                <BookOpen className="h-3.5 w-3.5" /> Phase Core Resources
              </p>
              <div className="space-y-2">
                {phase.resources.slice(0, 3).map((r: any, i: number) => (
                  <a key={i} href={r.url} target="_blank" rel="noopener noreferrer"
                    className="flex items-center gap-3 p-3 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors group">
                    <span className="text-lg flex-shrink-0">
                      {r.format === 'video' ? '🎥' : r.format === 'course' ? '🎓' : r.format === 'interactive' ? '💻' : '📄'}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="text-white text-sm font-medium truncate group-hover:text-indigo-300 transition-colors">{r.title}</p>
                      <p className="text-slate-500 text-xs">{r.provider}</p>
                    </div>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded ${r.score >= 70 ? 'bg-green-900/50 text-green-400' : 'bg-slate-700 text-slate-400'}`}>
                      {Math.round(r.score || 0)}%
                    </span>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Projects */}
          {phase.projects?.length > 0 && (
            <div>
              <p className="text-slate-400 text-xs font-medium mb-2 uppercase tracking-wider flex items-center gap-1">
                <Folder className="h-3.5 w-3.5" /> Phase Project
              </p>
              {phase.projects.map((p: any, i: number) => (
                <div key={i} className="p-3 bg-slate-800 rounded-xl">
                  <p className="text-white text-sm font-medium">🔨 {p.title}</p>
                  {p.description && <p className="text-slate-400 text-xs mt-1">{p.description}</p>}
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}
    </motion.div>
  );
}


export default function RoadmapPage() {
  const queryClient = useQueryClient();
  const [feedbackText, setFeedbackText] = useState('');
  const [isAdapting, setIsAdapting] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['roadmap'],
    queryFn: () => learningPathAPI.get().then((r) => r.data.data),
  });

  const dashboardQuery = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => dashboardAPI.get().then((r) => r.data.data),
  });

  const adaptMutation = useMutation({
    mutationFn: (feedback: string) => learningPathAPI.adapt(feedback),
    onSuccess: (res) => {
      toast.success(res.data.message || 'Roadmap adapted!');
      queryClient.invalidateQueries({ queryKey: ['roadmap'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
      setFeedbackText('');
      setIsAdapting(false);
    },
    onError: () => toast.error('Could not adapt roadmap right now.'),
  });

  const handleAdapt = () => {
    if (!feedbackText.trim()) return;
    adaptMutation.mutate(feedbackText);
  };

  if (isLoading) return (
    <div className="flex items-center justify-center h-full p-12">
      <div className="h-8 w-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  if (!data) return (
    <div className="p-6 text-center">
      <Map className="h-16 w-16 text-slate-700 mx-auto mb-4" />
      <h2 className="text-xl font-bold text-white mb-2">No Roadmap Yet</h2>
      <p className="text-slate-400 mb-6">Complete onboarding to generate your personalized learning roadmap.</p>
      <Link href="/onboarding" className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-3 rounded-xl">
        Build My Roadmap
      </Link>
    </div>
  );

  const roadmap = data as Roadmap;

  // Use dashboard's authoritative overall_progress for consistency across pages
  const progress = dashboardQuery.data?.overall_progress ?? Math.round(((roadmap.phases || []).filter((p) => p.status === 'completed').length / (roadmap.phases?.length || 1)) * 100);
  const completedPhases = dashboardQuery.data ? Math.round(((dashboardQuery.data.overall_progress || 0) / 100) * (roadmap.phases?.length || 1)) : (roadmap.phases || []).filter((p) => p.status === 'completed').length;

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-start gap-4 justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Map className="h-6 w-6 text-indigo-400" />
            {roadmap.title}
          </h1>
          <p className="text-slate-400 mt-1">{roadmap.description}</p>
        </div>
        <button onClick={() => setIsAdapting(!isAdapting)}
          className="flex items-center gap-2 bg-indigo-950 hover:bg-indigo-900 border border-indigo-700 text-indigo-300 px-4 py-2 rounded-xl text-sm font-medium transition-all flex-shrink-0">
          <Zap className="h-4 w-4" />
          Adapt Roadmap
        </button>
      </div>

      {/* Progress */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <div className="flex items-center justify-between mb-3">
          <span className="text-white font-medium">Overall Progress</span>
          <span className="text-indigo-400 font-bold">{progress}%</span>
        </div>
        <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full"
            initial={{ width: 0 }} animate={{ width: `${progress}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
        </div>
        <div className="flex gap-4 mt-3 text-sm text-slate-400">
          <span>📅 {roadmap.total_weeks} weeks total</span>
          <span>✅ {completedPhases}/{roadmap.phases?.length || 0} phases done</span>
          <span>🏆 {roadmap.milestones?.length || 0} milestones</span>
        </div>
      </div>

      {/* Adapt Roadmap Panel */}
      {isAdapting && (
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
          className="bg-slate-900 border border-indigo-700/50 rounded-2xl p-5">
          <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
            <Zap className="h-5 w-5 text-indigo-400" />
            Adapt Your Roadmap with AI
          </h3>
          <p className="text-slate-400 text-sm mb-3">Tell me about any changes and I'll recalculate your entire learning plan.</p>
          <div className="flex flex-wrap gap-2 mb-3">
            {[
              'I only have 5 hours per week now',
              "I've mastered Python, skip beginner content",
              'I find statistics too hard, add prerequisites',
              'I have 30 hours a week, accelerate my plan',
            ].map((suggestion) => (
              <button key={suggestion} onClick={() => setFeedbackText(suggestion)}
                className="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-lg transition-all">
                {suggestion}
              </button>
            ))}
          </div>
          <textarea
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder="Tell me what changed: 'I only have 5 hours per week now' or 'I already know Python'"
            className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm resize-none"
            rows={3}
          />
          <div className="flex justify-end gap-3 mt-3">
            <button onClick={() => setIsAdapting(false)} className="text-slate-400 hover:text-white text-sm px-4 py-2 rounded-xl hover:bg-slate-800 transition-all">Cancel</button>
            <button onClick={handleAdapt} disabled={adaptMutation.isPending || !feedbackText.trim()}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-medium px-5 py-2 rounded-xl transition-all flex items-center gap-2">
              {adaptMutation.isPending ? <><div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Adapting...</> : '⚡ Adapt Now'}
            </button>
          </div>
        </motion.div>
      )}

      {/* Milestones */}
      {roadmap.milestones?.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <h2 className="font-semibold text-white mb-4 flex items-center gap-2"><Star className="h-5 w-5 text-amber-400" /> Milestones</h2>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {roadmap.milestones.map((m, i) => (
              <div key={m.id} className="flex-shrink-0 bg-slate-800 rounded-xl p-4 w-52">
                <div className="text-amber-400 text-2xl mb-1">🏆</div>
                <p className="text-white text-sm font-semibold leading-tight">{m.title}</p>
                <p className="text-slate-400 text-xs mt-1">Week {m.week}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Phases */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-white text-lg">Learning Phases</h2>
          <span className="text-xs text-indigo-400">💡 Click any topic badge to view official docs & YouTube tutorials</span>
        </div>
        <div className="space-y-3">
          {(roadmap.phases || []).map((phase, i) => (
            <PhaseCard
              key={phase.phase_number}
              phase={phase}
              index={i}
              onSelectTopic={(topic) => setSelectedTopic(topic)}
            />
          ))}
        </div>
      </div>

      {/* Topic Study Guide Modal */}
      <AnimatePresence>
        {selectedTopic && (
          <TopicModal
            topicName={selectedTopic}
            onClose={() => setSelectedTopic(null)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

