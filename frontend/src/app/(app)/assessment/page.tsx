'use client';

import { useMemo, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { assessmentAPI } from '@/lib/api';
import { ClipboardList, CheckCircle, XCircle, Clock, ChevronRight, TrendingUp } from 'lucide-react';
import toast from 'react-hot-toast';
import type { Assessment, AssessmentResult } from '@/types';

function AssessmentTaker({ assessment, onDone }: { assessment: Assessment; onDone: (result: AssessmentResult) => void }) {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [currentQ, setCurrentQ] = useState(0);

  const sessionQuestions = useMemo(() => {
    const shuffled = [...assessment.questions];
    for (let i = shuffled.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled.slice(0, 15);
  }, [assessment]);

  const queryClient = useQueryClient();

  const submitMutation = useMutation({
    mutationFn: () => assessmentAPI.submit(assessment.id, answers),
    onSuccess: (res) => {
      const r = res.data.data;
      setResult(r);
      setSubmitted(true);
      onDone(r);
      toast.success(`Assessment complete! Score: ${r.score.toFixed(0)}%`);
      // Invalidate so dashboard/skills/recommendations reflect updated skill level
      queryClient.invalidateQueries({ queryKey: ['dashboard'] });
      queryClient.invalidateQueries({ queryKey: ['skill-gaps'] });
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
    },
    onError: () => toast.error('Could not submit assessment. Please try again.'),
  });

  const question = sessionQuestions[currentQ];
  const totalQ = sessionQuestions.length;
  const allAnswered = Object.keys(answers).length === totalQ;

  if (submitted && result) {
    return (
      <div className="text-center py-8 max-w-lg mx-auto">
        <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-4 ${result.passed ? 'bg-green-900' : 'bg-red-900'}`}>
          {result.passed
            ? <CheckCircle className="h-12 w-12 text-green-400" />
            : <XCircle className="h-12 w-12 text-red-400" />
          }
        </div>
        <h2 className="text-3xl font-bold text-white mb-2">{result.score.toFixed(0)}%</h2>
        <p className={`text-lg font-semibold mb-4 ${result.passed ? 'text-green-400' : 'text-red-400'}`}>
          {result.passed ? '✅ Passed!' : '❌ Not Passed'}
        </p>
        <p className="text-slate-300 leading-relaxed mb-4">{result.feedback}</p>
        <p className="text-slate-400 text-sm mb-2">{result.correct_answers}/{result.total_questions} correct</p>
        <div className="grid sm:grid-cols-2 gap-3 text-left mb-4">
          <div className="bg-slate-800 rounded-xl p-4">
            <p className="text-emerald-300 font-medium text-sm mb-2">Strong areas</p>
            <p className="text-slate-400 text-sm">{result.strong_areas?.length ? result.strong_areas.join(', ') : 'Keep practicing to build clear strengths.'}</p>
          </div>
          <div className="bg-slate-800 rounded-xl p-4">
            <p className="text-amber-300 font-medium text-sm mb-2">Weak areas</p>
            <p className="text-slate-400 text-sm">{result.weak_areas?.length ? result.weak_areas.join(', ') : 'No major weak areas in this attempt.'}</p>
          </div>
        </div>
        {result.next_recommended_action && (
          <div className="bg-indigo-950/60 border border-indigo-800 rounded-xl p-4 text-left mb-4">
            <p className="text-indigo-200 font-medium text-sm mb-1">Next recommended action</p>
            <p className="text-slate-300 text-sm">{result.next_recommended_action}</p>
          </div>
        )}
        {result.recommendations.length > 0 && (
          <div className="bg-slate-800 rounded-xl p-4 text-left mt-4">
            <p className="text-slate-300 font-medium text-sm mb-2">Recommendations:</p>
            {result.recommendations.map((rec, i) => (
              <p key={i} className="text-slate-400 text-sm">• {rec}</p>
            ))}
          </div>
        )}
        <div className="bg-gradient-to-r from-indigo-950/50 to-violet-950/50 border border-indigo-800/50 rounded-xl p-4 text-left mt-4">
          <p className="text-indigo-300 font-medium text-sm mb-2 flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Adaptive Learning Update
          </p>
          <p className="text-slate-300 text-sm leading-relaxed">
            Your skill level has been updated based on this assessment. Your personalized recommendations and next best action have been recalculated to match your new skill state.
          </p>
          <button onClick={() => window.location.href = '/dashboard'}
            className="mt-3 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-all">
            View Updated Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="mb-6">
        <div className="flex justify-between text-sm text-slate-400 mb-2">
          <span>Question {currentQ + 1} of {totalQ}</span>
          <span>{Object.keys(answers).length} answered</span>
        </div>
        <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full bg-indigo-500 rounded-full transition-all duration-300" style={{ width: `${((currentQ + 1) / totalQ) * 100}%` }} />
        </div>
      </div>

      {/* Question */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-4">
        <p className="text-white text-lg font-medium mb-6 leading-relaxed">{question.question}</p>
        <div className="space-y-3">
          {question.options.map((option, optIdx) => (
            <button key={optIdx}
              onClick={() => {
                setAnswers((a) => ({ ...a, [question.id]: optIdx }));
              }}
              className={`w-full text-left px-5 py-4 rounded-xl border transition-all ${
                answers[question.id] === optIdx
                  ? 'bg-indigo-600 border-indigo-500 text-white'
                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-indigo-500 hover:bg-indigo-950'
              }`}>
              <span className="font-medium mr-3">{String.fromCharCode(65 + optIdx)}.</span>
              {option}
            </button>
          ))}
        </div>
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button onClick={() => setCurrentQ((q) => Math.max(0, q - 1))}
          disabled={currentQ === 0}
          className="bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 px-5 py-2.5 rounded-xl text-sm transition-all">
          ← Previous
        </button>

        {currentQ < totalQ - 1 ? (
          <button onClick={() => setCurrentQ((q) => Math.min(totalQ - 1, q + 1))}
            disabled={answers[question.id] === undefined}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-medium px-5 py-2.5 rounded-xl text-sm transition-all">
            Next →
          </button>
        ) : (
          <button onClick={() => submitMutation.mutate()}
            disabled={!allAnswered || submitMutation.isPending}
            className="bg-green-600 hover:bg-green-500 disabled:opacity-40 text-white font-semibold px-6 py-2.5 rounded-xl text-sm transition-all flex items-center gap-2">
            {submitMutation.isPending ? 'Submitting...' : '✅ Submit Assessment'}
          </button>
        )}
      </div>
    </div>
  );
}

export default function AssessmentPage() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [done, setDone] = useState<Record<string, AssessmentResult>>({});

  const { data: assessments, isLoading } = useQuery({
    queryKey: ['assessments'],
    queryFn: () => assessmentAPI.getAll().then((r) => r.data.data),
  });

  const { data: selectedAssessment } = useQuery({
    queryKey: ['assessment', selectedId],
    queryFn: () => selectedId ? assessmentAPI.getOne(selectedId).then((r) => r.data.data) : null,
    enabled: !!selectedId,
  });

  if (selectedId && selectedAssessment) {
    return (
      <div className="p-6 max-w-3xl mx-auto">
        <button onClick={() => setSelectedId(null)}
          className="flex items-center gap-2 text-slate-400 hover:text-white mb-6 text-sm transition-colors">
          ← Back to Assessments
        </button>
        <h1 className="text-2xl font-bold text-white mb-2">{selectedAssessment.title}</h1>
        <p className="text-slate-400 text-sm mb-6">
          {Math.min(selectedAssessment.questions.length, 15)} questions from a {selectedAssessment.questions.length}-question bank · {selectedAssessment.estimated_minutes} min · Pass: {selectedAssessment.passing_score}%
        </p>
        <AssessmentTaker assessment={selectedAssessment} onDone={(result) => setDone((d) => ({ ...d, [selectedId]: result }))} />
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <ClipboardList className="h-6 w-6 text-indigo-400" />
          Skill Assessments
        </h1>
        <p className="text-slate-400 mt-1">Test your knowledge and let AI calibrate your roadmap based on real results.</p>
      </div>

      {isLoading ? (
        <div className="grid sm:grid-cols-2 gap-4">
          {[1,2,3].map((i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse">
              <div className="h-5 bg-slate-700 rounded w-1/2 mb-3" />
              <div className="h-4 bg-slate-700 rounded w-1/3" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 gap-4">
          {(!assessments || assessments.length === 0) && (
            <div className="sm:col-span-2 rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400">
              Assessments will appear here once the backend seed data has loaded. Restart the API if this stays empty.
            </div>
          )}
          {(assessments || []).map((assessment: any, i: number) => {
            const result = done[assessment.id];
            return (
              <motion.div key={assessment.id}
                initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
                className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 transition-all">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-white font-semibold">{assessment.title}</h3>
                    <p className="text-indigo-400 text-sm mt-0.5">{assessment.skill_name}</p>
                  </div>
                  {result && (
                    <span className={`text-sm font-bold px-2.5 py-1 rounded-full ${result.passed ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400'}`}>
                      {result.score.toFixed(0)}%
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-4 text-sm text-slate-400 mb-4">
                  <span className="flex items-center gap-1"><ClipboardList className="h-4 w-4" /> {assessment.question_count} questions</span>
                  <span className="flex items-center gap-1"><Clock className="h-4 w-4" /> ~{assessment.estimated_minutes} min</span>
                  <span className="flex items-center gap-1">⭐ Pass: {assessment.passing_score}%</span>
                </div>

                <button onClick={() => setSelectedId(assessment.id)}
                  className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-xl transition-all text-sm">
                  {result ? 'Retake Assessment' : 'Start Assessment'}
                  <ChevronRight className="h-4 w-4" />
                </button>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
