'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Target, Clock, BookOpen, ChevronRight, ChevronLeft, Check } from 'lucide-react';
import { learningPathAPI, profileAPI } from '@/lib/api';
import { useAuthStore } from '@/store/auth';
import toast from 'react-hot-toast';
import Link from 'next/link';

const ROLES = [
  'AI/ML Engineer', 'Data Scientist', 'Data Analyst', 'Software Engineer',
  'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
  'Cloud Engineer', 'DevOps Engineer', 'Cybersecurity Analyst',
];

const EXPERIENCE_LEVELS = [
  { value: 'beginner', label: 'Beginner', desc: 'Just starting out, minimal experience' },
  { value: 'intermediate', label: 'Intermediate', desc: 'Some experience, know the basics' },
  { value: 'advanced', label: 'Advanced', desc: 'Strong foundation, looking to specialize' },
];

const WEEKLY_HOURS = [
  { value: 5, label: '< 1 hr/day', desc: '~5 hours per week' },
  { value: 10, label: '1-2 hrs/day', desc: '~10 hours per week' },
  { value: 20, label: '2-3 hrs/day', desc: '~20 hours per week' },
  { value: 35, label: '4+ hrs/day', desc: '35+ hours per week' },
];

const LEARNING_STYLES = [
  { value: 'video', label: '🎥 Video', desc: 'YouTube, Coursera, Udemy' },
  { value: 'reading', label: '📄 Reading', desc: 'Docs, blogs, books' },
  { value: 'coding', label: '💻 Hands-on', desc: 'Interactive coding exercises' },
  { value: 'projects', label: '🔨 Projects', desc: 'Learn by building' },
  { value: 'mixed', label: '🎯 Mixed', desc: 'A bit of everything' },
];

const COMMON_SKILLS = [
  'Python', 'JavaScript', 'SQL', 'HTML/CSS', 'React', 'Machine Learning',
  'Statistics', 'Linear Algebra', 'Docker', 'Git', 'DSA', 'NumPy/Pandas',
  'Deep Learning', 'Node.js', 'TypeScript', 'AWS/GCP/Azure', 'Linux',
  'System Design', 'Data Visualization', 'REST APIs',
];

export default function OnboardingPage() {
  const router = useRouter();
  const { isAuthenticated, login, demoLogin } = useAuthStore();
  const [step, setStep] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [form, setForm] = useState({
    goal: '',
    free_text_goal: '',
    experience_level: '',
    weekly_hours: 10,
    learning_style: 'mixed',
    target_deadline: '12',
    current_skills: [] as { name: string; level: number }[],
    guestEmail: '',
    guestPassword: '',
    guestName: '',
  });

  const totalSteps = 5;
  const progress = (step / totalSteps) * 100;

  const toggleSkill = (skillName: string) => {
    setForm((f) => {
      const exists = f.current_skills.find((s) => s.name === skillName);
      if (exists) {
        return { ...f, current_skills: f.current_skills.filter((s) => s.name !== skillName) };
      } else {
        return { ...f, current_skills: [...f.current_skills, { name: skillName, level: 2 }] };
      }
    });
  };

  const setSkillLevel = (skillName: string, level: number) => {
    setForm((f) => ({
      ...f,
      current_skills: f.current_skills.map((s) => s.name === skillName ? { ...s, level } : s),
    }));
  };

  const canNext = () => {
    if (step === 1) return !!form.goal;
    if (step === 2) return !!form.experience_level;
    if (step === 3) return true;
    if (step === 4) return true;
    if (step === 5) return isAuthenticated || (form.guestName && form.guestEmail && form.guestPassword);
    return true;
  };

  const handleNext = () => { if (step < totalSteps) setStep((s) => s + 1); };
  const handleBack = () => { if (step > 1) setStep((s) => s - 1); };

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      // Authenticate first if not already
      if (!isAuthenticated) {
        if (form.guestEmail === 'demo@learnpath.ai') {
          await demoLogin();
        } else {
          const { authAPI } = await import('@/lib/api');
          const { data } = await authAPI.register({
            name: form.guestName,
            email: form.guestEmail,
            password: form.guestPassword,
          });
          const { useAuthStore: store } = await import('@/store/auth');
          localStorage.setItem('learnpath_token', data.data.access_token);
        }
      }

      // Generate roadmap
      const { data } = await learningPathAPI.generate({
        goal: form.goal || 'Software Engineer',
        free_text_goal: form.free_text_goal || undefined,
        experience_level: form.experience_level || 'intermediate',
        current_skills: form.current_skills,
        weekly_hours: form.weekly_hours,
        learning_style: form.learning_style,
        target_deadline: form.target_deadline,
      });

      toast.success('🎉 Your personalized roadmap is ready!');
      router.push('/dashboard');
    } catch (error: any) {
      toast.error(error?.response?.data?.detail || 'Failed to generate roadmap. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const stepVariants = {
    enter: { opacity: 0, x: 40 },
    center: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -40 },
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
        <Link href="/" className="flex items-center gap-2">
          <Brain className="h-6 w-6 text-indigo-500" />
          <span className="font-bold text-lg">LearnPath AI</span>
        </Link>
        <span className="text-slate-400 text-sm">Step {step} of {totalSteps}</span>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-slate-800">
        <motion.div
          className="h-full bg-indigo-500"
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.4 }}
        />
      </div>

      {/* Content */}
      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl">
          <AnimatePresence mode="wait">
            <motion.div
              key={step}
              variants={stepVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.3 }}
            >
              {/* Step 1: Goal */}
              {step === 1 && (
                <div>
                  <div className="text-center mb-8">
                    <Target className="h-12 w-12 text-indigo-400 mx-auto mb-3" />
                    <h2 className="text-3xl font-bold mb-2">What's your career goal?</h2>
                    <p className="text-slate-400">Choose the role you want to land or describe it in your own words.</p>
                  </div>

                  <div className="grid sm:grid-cols-2 gap-3 mb-4">
                    {ROLES.map((role) => (
                      <button key={role} onClick={() => setForm((f) => ({ ...f, goal: role, free_text_goal: '' }))}
                        className={`text-left px-5 py-4 rounded-xl border transition-all font-medium ${form.goal === role
                          ? 'bg-indigo-600 border-indigo-500 text-white'
                          : 'bg-slate-900 border-slate-700 text-slate-300 hover:border-indigo-500 hover:bg-indigo-950'}`}>
                        {form.goal === role && <Check className="h-4 w-4 inline mr-2" />}
                        {role}
                      </button>
                    ))}
                  </div>

                  <div className="mb-4">
                    <label className="block text-slate-400 text-sm mb-2">Or describe your goal (optional)</label>
                    <textarea value={form.free_text_goal} onChange={(e) => setForm((f) => ({ ...f, free_text_goal: e.target.value, goal: '' }))}
                      placeholder="E.g., I want to become a machine learning engineer focusing on NLP and deployment; I can study 10 hours/week"
                      className="w-full bg-slate-800 border border-slate-700 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500" rows={3} />
                  </div>
                </div>
              )}

              {/* Step 2: Experience */}
              {step === 2 && (
                <div>
                  <div className="text-center mb-8">
                    <BookOpen className="h-12 w-12 text-indigo-400 mx-auto mb-3" />
                    <h2 className="text-3xl font-bold mb-2">What's your experience level?</h2>
                    <p className="text-slate-400">For <span className="text-indigo-400 font-semibold">{form.goal}</span> specifically.</p>
                  </div>
                  <div className="space-y-3">
                    {EXPERIENCE_LEVELS.map((lvl) => (
                      <button key={lvl.value} onClick={() => setForm((f) => ({ ...f, experience_level: lvl.value }))}
                        className={`w-full text-left px-6 py-5 rounded-xl border transition-all ${form.experience_level === lvl.value
                          ? 'bg-indigo-600 border-indigo-500' : 'bg-slate-900 border-slate-700 hover:border-indigo-500 hover:bg-indigo-950'}`}>
                        <div className="font-semibold text-lg">{lvl.label}</div>
                        <div className="text-sm text-slate-300 mt-1">{lvl.desc}</div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Step 3: Skills */}
              {step === 3 && (
                <div>
                  <div className="text-center mb-8">
                    <Check className="h-12 w-12 text-indigo-400 mx-auto mb-3" />
                    <h2 className="text-3xl font-bold mb-2">What do you already know?</h2>
                    <p className="text-slate-400">Select skills you're comfortable with. We'll skip the basics for those.</p>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-6">
                    {COMMON_SKILLS.map((skill) => {
                      const selected = form.current_skills.find((s) => s.name === skill);
                      return (
                        <button key={skill} onClick={() => toggleSkill(skill)}
                          className={`px-4 py-2 rounded-lg border text-sm font-medium transition-all ${selected
                            ? 'bg-indigo-600 border-indigo-500 text-white'
                            : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-indigo-500'}`}>
                          {skill}
                        </button>
                      );
                    })}
                  </div>

                  {form.current_skills.length > 0 && (
                    <div className="bg-slate-900 border border-slate-700 rounded-xl p-4">
                      <p className="text-slate-400 text-sm mb-3">Rate your level for selected skills:</p>
                      <div className="space-y-2">
                        {form.current_skills.map((s) => (
                          <div key={s.name} className="flex items-center justify-between">
                            <span className="text-slate-300 text-sm">{s.name}</span>
                            <div className="flex gap-1">
                              {[1, 2, 3, 4, 5].map((lvl) => (
                                <button key={lvl} onClick={() => setSkillLevel(s.name, lvl)}
                                  className={`w-7 h-7 rounded text-xs font-bold transition-all ${s.level >= lvl ? 'bg-indigo-600 text-white' : 'bg-slate-700 text-slate-400'}`}>
                                  {lvl}
                                </button>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Step 4: Schedule & Style */}
              {step === 4 && (
                <div>
                  <div className="text-center mb-8">
                    <Clock className="h-12 w-12 text-indigo-400 mx-auto mb-3" />
                    <h2 className="text-3xl font-bold mb-2">How much time can you commit?</h2>
                    <p className="text-slate-400">Your roadmap duration will automatically adjust.</p>
                  </div>

                  <div className="grid grid-cols-2 gap-3 mb-8">
                    {WEEKLY_HOURS.map((h) => (
                      <button key={h.value} onClick={() => setForm((f) => ({ ...f, weekly_hours: h.value }))}
                        className={`text-left px-5 py-4 rounded-xl border transition-all ${form.weekly_hours === h.value
                          ? 'bg-indigo-600 border-indigo-500' : 'bg-slate-900 border-slate-700 hover:border-indigo-500 hover:bg-indigo-950'}`}>
                        <div className="font-semibold">{h.label}</div>
                        <div className="text-xs text-slate-300 mt-0.5">{h.desc}</div>
                      </button>
                    ))}
                  </div>

                  <div>
                    <p className="text-slate-300 mb-3 font-medium">Preferred learning style:</p>
                    <div className="grid grid-cols-5 gap-2">
                      {LEARNING_STYLES.map((style) => (
                        <button key={style.value} onClick={() => setForm((f) => ({ ...f, learning_style: style.value }))}
                          className={`text-center p-3 rounded-xl border text-sm transition-all ${form.learning_style === style.value
                            ? 'bg-indigo-600 border-indigo-500' : 'bg-slate-900 border-slate-700 hover:border-indigo-500'}`}>
                          <div className="text-lg mb-1">{style.label.split(' ')[0]}</div>
                          <div className="text-xs text-slate-300 leading-tight">{style.label.split(' ').slice(1).join(' ')}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Step 5: Account */}
              {step === 5 && (
                <div>
                  <div className="text-center mb-8">
                    <Brain className="h-12 w-12 text-indigo-400 mx-auto mb-3" />
                    <h2 className="text-3xl font-bold mb-2">Almost there! 🎉</h2>
                    <p className="text-slate-400">Create a free account to save your personalized roadmap.</p>
                  </div>

                  {isAuthenticated ? (
                    <div className="bg-indigo-950 border border-indigo-700 rounded-xl p-6 text-center">
                      <Check className="h-12 w-12 text-indigo-400 mx-auto mb-3" />
                      <p className="text-lg font-semibold text-white">You're logged in!</p>
                      <p className="text-slate-400">Click "Generate My Roadmap" below to build your personalized plan.</p>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {/* Demo option */}
                      <div className="bg-amber-950/50 border border-amber-700/50 rounded-xl p-4">
                        <p className="text-amber-300 text-sm font-medium mb-2">⚡ Quick Demo Access</p>
                        <button onClick={() => setForm((f) => ({ ...f, guestEmail: 'demo@learnpath.ai', guestPassword: 'Demo@12345', guestName: 'Alex Chen' }))}
                          className="text-amber-400 hover:text-amber-300 text-sm underline">
                          Use demo account (demo@learnpath.ai / Demo@12345)
                        </button>
                      </div>

                      <input
                        type="text"
                        placeholder="Full Name"
                        value={form.guestName}
                        onChange={(e) => setForm((f) => ({ ...f, guestName: e.target.value }))}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                      />
                      <input
                        type="email"
                        placeholder="Email address"
                        value={form.guestEmail}
                        onChange={(e) => setForm((f) => ({ ...f, guestEmail: e.target.value }))}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                      />
                      <input
                        type="password"
                        placeholder="Password (min 8 chars)"
                        value={form.guestPassword}
                        onChange={(e) => setForm((f) => ({ ...f, guestPassword: e.target.value }))}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                      />
                      <p className="text-xs text-slate-500">Already have an account? <Link href="/login" className="text-indigo-400 hover:underline">Sign in instead</Link></p>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          <div className="flex items-center justify-between mt-10">
            <button onClick={handleBack} disabled={step === 1}
              className="flex items-center gap-2 px-5 py-3 rounded-xl border border-slate-700 text-slate-300 hover:border-slate-500 disabled:opacity-30 transition-all">
              <ChevronLeft className="h-4 w-4" />
              Back
            </button>

            {step < totalSteps ? (
              <button onClick={handleNext} disabled={!canNext()}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold px-6 py-3 rounded-xl transition-all">
                Continue
                <ChevronRight className="h-4 w-4" />
              </button>
            ) : (
              <button onClick={handleGenerate}
                disabled={isGenerating || !canNext()}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold px-6 py-3 rounded-xl transition-all">
                {isGenerating ? (
                  <>
                    <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Generating Roadmap...
                  </>
                ) : (
                  <>Generate My Roadmap 🚀</>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
