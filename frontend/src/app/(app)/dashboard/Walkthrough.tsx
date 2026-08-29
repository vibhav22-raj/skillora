'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight } from 'lucide-react';

// Professional full-screen walkthrough overlay that anchors to DOM selectors
export default function Walkthrough({ onClose }: { onClose: () => void }) {
  const steps: { title: string; desc: string; selector?: string }[] = [
    { title: 'Dashboard', desc: 'Overview of progress, streaks and quick stats.', selector: 'a[href="/dashboard"]' },
    { title: 'Roadmap', desc: 'A week-by-week personalized learning plan.', selector: 'a[href="/roadmap"]' },
    { title: 'Recommendations', desc: 'AI-ranked resources tailored to your skill gaps.', selector: 'a[href="/recommendations"]' },
    { title: 'Skills', desc: 'View and update your skill levels and gaps.', selector: 'a[href="/skills"]' },
    { title: 'Projects', desc: 'Hands-on projects to build your portfolio.', selector: 'a[href="/projects"]' },
    { title: 'Assessments', desc: 'Take quizzes to calibrate your roadmap.', selector: 'a[href="/assessment"]' },
    { title: 'Chat Mentor', desc: 'Ask the AI Mentor for guidance and explanations.', selector: 'a[href="/chat"]' },
    { title: 'Resources', desc: 'Search curated learning materials and filters.', selector: 'a[href="/resources"]' },
    { title: 'Next Best Action', desc: 'One actionable item to make progress today.', selector: '#walk-next-best-action' },
    { title: 'Profile & Settings', desc: 'Manage account, preferences, and integrations.', selector: 'a[href="/profile"]' },
  ];

  const [index, setIndex] = useState(0);
  const total = steps.length;

  // card position state
  const [pos, setPos] = useState<{ left: number; top: number; width: number } | null>(null);
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);

  useEffect(() => {
    // compute position for current step
    const s = steps[index];
    if (!s?.selector || typeof window === 'undefined') {
      setPos(null);
      setTargetRect(null);
      return;
    }

    const el = document.querySelector(s.selector);
    if (!el) {
      setPos(null);
      setTargetRect(null);
      return;
    }

    const rect = el.getBoundingClientRect();
    setTargetRect(rect);

    // position the floating card near the element (above-right by default)
    const cardWidth = Math.min(520, window.innerWidth - 48);
    const left = Math.min(Math.max(rect.left + rect.width + 12, 24), window.innerWidth - cardWidth - 24);
    const top = Math.min(Math.max(rect.top, 24), window.innerHeight - 160);

    setPos({ left, top: Math.max(top, 24), width: cardWidth });

    // Add brief highlight to target
    const highlight = (el as HTMLElement).style;
    const prevOutline = (el as HTMLElement).getAttribute('data-prev-outline') || '';
    (el as HTMLElement).setAttribute('data-prev-outline', prevOutline);
    highlight.boxShadow = '0 8px 30px rgba(99,102,241,0.18)';
    highlight.zIndex = '60';

    const cleanup = () => {
      highlight.boxShadow = '';
      highlight.zIndex = '';
    };

    return () => cleanup();
  }, [index]);

  const closeAndPersist = () => {
    localStorage.setItem('learnpath_walkthrough_shown', '1');
    onClose();
  };

  const next = () => {
    if (index < total - 1) setIndex((i) => i + 1);
    else closeAndPersist();
  };

  const prev = () => setIndex((i) => Math.max(0, i - 1));

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 pointer-events-auto">
        {/* dimmed backdrop */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 0.6 }} exit={{ opacity: 0 }} className="absolute inset-0 bg-black" />

        {/* optional spotlight over the target */}
        {targetRect && (
          <div style={{ position: 'absolute', left: targetRect.left - 8, top: targetRect.top - 8, width: targetRect.width + 16, height: targetRect.height + 16, borderRadius: 12, boxShadow: '0 0 0 9999px rgba(0,0,0,0.6), 0 10px 30px rgba(99,102,241,0.12)', transition: 'all 0.25s ease', pointerEvents: 'none' }} />
        )}

        {/* floating card — animate to pos if available */}
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={pos ? { opacity: 1, x: pos.left, y: pos.top } : { opacity: 1, x: window.innerWidth / 2 - 260, y: 120 }}
          exit={{ opacity: 0 }}
          transition={{ type: 'spring', stiffness: 220, damping: 28 }}
          style={{ position: 'absolute', left: 0, top: 0, width: pos?.width || 520 }}
        >
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-slate-400 text-sm">Walkthrough</p>
                <h3 className="text-lg font-bold text-white">Step {index + 1} of {total} — {steps[index].title}</h3>
              </div>
              <div className="flex items-center gap-2">
                {index > 0 && <button onClick={prev} className="text-slate-400 hover:text-slate-200 text-sm px-3 py-1">Back</button>}
                <button onClick={closeAndPersist} className="text-slate-400 hover:text-slate-200 text-sm">Close</button>
              </div>
            </div>

            <p className="text-slate-300 mb-4">{steps[index].desc}</p>

            <div className="flex items-center justify-between">
              <div className="text-slate-500 text-sm">
                {steps.map((_, i) => (
                  <span key={i} className={i === index ? 'text-indigo-400 mr-1' : 'text-slate-700 mr-1'}>●</span>
                ))}
              </div>

              <div className="flex items-center gap-2">
                <button onClick={() => { localStorage.setItem('learnpath_walkthrough_shown', '1'); onClose(); }} className="px-3 py-2 text-sm rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">Skip</button>
                <button onClick={next} className="px-4 py-2 text-sm rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white flex items-center gap-2">
                  {index === total - 1 ? 'Finish' : 'Next'} <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* pointer arrow from card to target */}
        {targetRect && (
          <svg style={{ position: 'absolute', left: 0, top: 0, pointerEvents: 'none' }} width={window.innerWidth} height={window.innerHeight}>
            <defs>
              <marker id="arrow" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto">
                <path d="M0,0 L10,5 L0,10 z" fill="#8b5cf6" />
              </marker>
            </defs>
            {/* line from card center to target center */}
            {pos && (
              <line x1={pos.left + (pos.width / 2)} y1={pos.top + 40} x2={targetRect.left + targetRect.width / 2} y2={targetRect.top + targetRect.height / 2} stroke="#8b5cf6" strokeWidth={2} strokeLinecap="round" markerEnd="url(#arrow)" strokeOpacity={0.9} />
            )}
          </svg>
        )}
      </div>
    </AnimatePresence>
  );
}
