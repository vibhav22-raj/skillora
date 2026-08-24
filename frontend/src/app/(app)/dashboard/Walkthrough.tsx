'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronRight } from 'lucide-react';

export default function Walkthrough({ onClose }: { onClose: () => void }) {
  const steps = [
    { title: 'Dashboard', desc: 'Overview of progress, streaks and quick stats.' },
    { title: 'Roadmap', desc: 'A week-by-week personalized learning plan.' },
    { title: 'Recommendations', desc: 'AI-ranked resources tailored to your skill gaps.' },
    { title: 'Skills', desc: 'View and update your skill levels and gaps.' },
    { title: 'Projects', desc: 'Hands-on projects to build your portfolio.' },
    { title: 'Assessments', desc: 'Take quizzes to calibrate your roadmap.' },
    { title: 'Chat Mentor', desc: 'Ask the AI Mentor for guidance and explanations.' },
    { title: 'Resources', desc: 'Search curated learning materials and filters.' },
    { title: 'Next Best Action', desc: 'One actionable item to make progress today.' },
    { title: 'Settings', desc: 'Manage account, preferences, and integrations.' },
  ];

  const [index, setIndex] = useState(0);
  const total = steps.length;

  const next = () => {
    if (index < total - 1) setIndex((i) => i + 1);
    else {
      localStorage.setItem('learnpath_walkthrough_shown', '1');
      onClose();
    }
  };

  const skip = () => {
    localStorage.setItem('learnpath_walkthrough_shown', '1');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="max-w-xl w-full bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <p className="text-slate-400 text-sm">Walkthrough</p>
            <h3 className="text-lg font-bold text-white">Step {index + 1} of {total} — {steps[index].title}</h3>
          </div>
          <button onClick={skip} className="text-slate-400 hover:text-slate-200 text-sm">Skip</button>
        </div>

        <p className="text-slate-300 mb-6">{steps[index].desc}</p>

        <div className="flex items-center justify-between">
          <div className="text-slate-500 text-sm">
            <span className="mr-2">{Array.from({ length: total }).map((_, i) => (
              <span key={i} className={i === index ? 'text-indigo-400' : 'text-slate-700'}>●</span>
            ))}</span>
          </div>

          <div className="flex items-center gap-2">
            <button onClick={skip} className="px-3 py-2 text-sm rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700">Skip</button>
            <button onClick={next} className="px-4 py-2 text-sm rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white flex items-center gap-2">
              {index === total - 1 ? 'Finish' : 'Next'} <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
