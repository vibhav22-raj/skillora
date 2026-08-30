'use client';

import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { resourcesAPI } from '@/lib/api';
import { BookOpen, Search, ExternalLink, Filter, CheckCircle, Play } from 'lucide-react';
import { getDifficultyLabel, getFormatIcon, getScoreColor } from '@/lib/utils';
import type { LearningResource } from '@/types';
import toast from 'react-hot-toast';

const FORMATS = ['', 'video', 'article', 'course', 'interactive', 'book'];
const DIFFICULTIES = [0, 1, 2, 3, 4, 5];

export default function ResourcesPage() {
  const [search, setSearch] = useState('');
  const [format, setFormat] = useState('');
  const [difficulty, setDifficulty] = useState(0);
  const [freeOnly, setFreeOnly] = useState(false);
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['resources', search, format, difficulty, freeOnly, page],
    queryFn: () => resourcesAPI.getAll({
      search: search || undefined,
      format: format || undefined,
      difficulty: difficulty || undefined,
      free_only: freeOnly || undefined,
      page,
      per_page: 12,
    }).then((r) => r.data.data),
    placeholderData: (prev) => prev,
  });

  const startMutation = useMutation({
    mutationFn: (id: string) => resourcesAPI.start(id),
    onSuccess: () => toast.success('Resource started! 🎓'),
  });

  const completeMutation = useMutation({
    mutationFn: (id: string) => resourcesAPI.complete(id),
    onSuccess: () => toast.success('🎉 Resource completed! Great work!'),
  });

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <BookOpen className="h-6 w-6 text-indigo-400" />
          Learning Resources & Tutorials
        </h1>
        <p className="text-slate-400 mt-1">100+ verified free documentation guides, video tutorials, and interactive coding practice.</p>
      </div>

      {/* Quick Category Filter Pills */}
      <div className="flex gap-2 overflow-x-auto pb-1 text-xs">
        {[
          { label: 'All Resources', val: '' },
          { label: '🎥 YouTube Videos', val: 'video' },
          { label: '📖 Official Docs & Articles', val: 'article' },
          { label: '💻 Interactive & Practice', val: 'interactive' },
          { label: '🎓 Complete Courses', val: 'course' },
        ].map((pill) => (
          <button
            key={pill.val}
            onClick={() => { setFormat(pill.val); setPage(1); }}
            className={`px-3.5 py-2 rounded-xl border whitespace-nowrap transition-all ${
              format === pill.val
                ? 'bg-indigo-600 border-indigo-500 text-white font-medium shadow-md shadow-indigo-950'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white hover:border-slate-700'
            }`}
          >
            {pill.label}
          </button>
        ))}
      </div>

      {/* Filters Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
        <div className="flex flex-col sm:flex-row gap-3">
          {/* Search */}
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search Python, DSA, Machine Learning, SQL, Docker..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="w-full bg-slate-800 border border-slate-700 rounded-xl pl-9 pr-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 text-sm"
            />
          </div>

          {/* Difficulty */}
          <select value={difficulty} onChange={(e) => { setDifficulty(Number(e.target.value)); setPage(1); }}
            className="bg-slate-800 border border-slate-700 rounded-xl px-3 py-2.5 text-slate-300 focus:outline-none focus:border-indigo-500 text-sm">
            <option value={0}>All Levels</option>
            {[1,2,3,4,5].map((d) => (
              <option key={d} value={d}>{getDifficultyLabel(d)}</option>
            ))}
          </select>

          {/* Free only */}
          <label className="flex items-center gap-2 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 cursor-pointer hover:border-indigo-500 transition-all">
            <input type="checkbox" checked={freeOnly} onChange={(e) => { setFreeOnly(e.target.checked); setPage(1); }}
              className="w-4 h-4 accent-indigo-500" />
            <span className="text-slate-300 text-sm whitespace-nowrap">Free only</span>
          </label>
        </div>
      </div>

      {/* Results count */}
      {data && (
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>{data.total} verified resources available</span>
          <span>Showing page {data.page} of {data.pages}</span>
        </div>
      )}

      {/* Resource grid */}
      {isLoading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1,2,3,4,5,6].map((i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse">
              <div className="h-5 bg-slate-700 rounded w-2/3 mb-3" />
              <div className="h-4 bg-slate-700 rounded w-1/2 mb-3" />
              <div className="h-8 bg-slate-700 rounded" />
            </div>
          ))}
        </div>
      ) : (
        <>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {(data?.resources || []).map((resource: LearningResource, i: number) => {
              const isVideo = resource.format === 'video' || resource.url?.includes('youtube.com') || resource.url?.includes('youtu.be');
              const isInteractive = resource.format === 'interactive' || resource.url?.includes('leetcode') || resource.url?.includes('kaggle');

              return (
                <motion.div
                  key={resource.id}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.03 }}
                  className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 flex flex-col transition-all group">
                  {/* Badges */}
                  <div className="flex items-center gap-2 flex-wrap mb-3">
                    <span className="text-sm">{getFormatIcon(resource.format || '')}</span>
                    <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded">{getDifficultyLabel(resource.difficulty)}</span>
                    {resource.is_free && (
                      <span className="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800/60 px-2 py-0.5 rounded font-medium">Free</span>
                    )}
                    {resource.rating > 0 && (
                      <span className="text-xs text-amber-400">⭐ {resource.rating.toFixed(1)}</span>
                    )}
                  </div>

                  {/* Title */}
                  <h3 className="text-white font-semibold text-sm leading-snug mb-1 flex-1 line-clamp-2 group-hover:text-indigo-300 transition-colors">
                    {resource.title}
                  </h3>
                  <p className="text-slate-400 text-xs mb-3 font-medium">
                    {resource.provider} · {resource.duration_hours}h
                  </p>

                  {/* Skills */}
                  <div className="flex flex-wrap gap-1 mb-3">
                    {(resource.skills || []).slice(0, 3).map((s) => (
                      <span key={s} className="bg-slate-800/90 text-slate-300 text-xs px-2 py-0.5 rounded border border-slate-700/50">{s}</span>
                    ))}
                  </div>

                  {/* Description */}
                  {resource.description && (
                    <p className="text-slate-500 text-xs line-clamp-2 mb-4">{resource.description}</p>
                  )}

                  {/* Actions */}
                  <div className="flex gap-2 mt-auto pt-2">
                    <a
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`flex-1 flex items-center justify-center gap-1.5 text-white text-xs font-medium py-2.5 rounded-xl transition-all shadow-sm ${
                        isVideo
                          ? 'bg-red-600 hover:bg-red-500'
                          : isInteractive
                          ? 'bg-cyan-600 hover:bg-cyan-500'
                          : 'bg-indigo-600 hover:bg-indigo-500'
                      }`}
                    >
                      {isVideo ? (
                        <>▶️ Watch on YouTube</>
                      ) : isInteractive ? (
                        <>💻 Practice Now</>
                      ) : (
                        <>
                          <ExternalLink className="h-3.5 w-3.5" />
                          Open Resource
                        </>
                      )}
                    </a>
                    <button
                      onClick={() => startMutation.mutate(resource.id)}
                      title="Mark as started"
                      className="flex items-center gap-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs px-3 py-2.5 rounded-xl transition-all">
                      <Play className="h-3.5 w-3.5" />
                    </button>
                    <button
                      onClick={() => completeMutation.mutate(resource.id)}
                      title="Mark as completed"
                      className="bg-slate-800 hover:bg-emerald-950 text-slate-400 hover:text-emerald-300 hover:border hover:border-emerald-800 p-2.5 rounded-xl transition-all">
                      <CheckCircle className="h-4 w-4" />
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </div>


          {/* Pagination */}
          {data && data.pages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-8">
              <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 rounded-xl text-sm transition-all">
                ← Previous
              </button>
              <span className="text-slate-400 text-sm">Page {data.page} of {data.pages}</span>
              <button onClick={() => setPage((p) => Math.min(data.pages, p + 1))} disabled={page === data.pages}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 rounded-xl text-sm transition-all">
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
