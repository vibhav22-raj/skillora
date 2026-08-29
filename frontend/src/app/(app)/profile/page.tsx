'use client';

import { ChangeEvent, useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Camera, CheckCircle2, Clock3, Flame, Pencil, Trash2, UserRound } from 'lucide-react';
import toast from 'react-hot-toast';
import { profileAPI } from '@/lib/api';
import { useAuthStore } from '@/store/auth';

const MAX_IMAGE_BYTES = 1024 * 1024;
const IMAGE_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp']);

export default function ProfilePage() {
  const { user, setUser } = useAuthStore();
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState<Record<string, string | number | null>>({});
  const profileQuery = useQuery({ queryKey: ['profile'], queryFn: () => profileAPI.get().then((r) => r.data.data) });
  const activityQuery = useQuery({ queryKey: ['profile-activity'], queryFn: () => profileAPI.activity().then((r) => r.data.data) });
  const completedQuery = useQuery({ queryKey: ['completed-courses'], queryFn: () => profileAPI.completedCourses().then((r) => r.data.data) });
  const profile = profileQuery.data;
  const activity = activityQuery.data;
  const initials = user?.name?.split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase() || 'U';

  const save = useMutation({
    mutationFn: (data: Record<string, unknown>) => profileAPI.update(data as never),
    onSuccess: (response) => {
      const data = response.data.data;
      if (form.name || form.email) setUser({ ...user!, name: String(form.name || user?.name), email: String(form.email || user?.email) });
      queryClient.invalidateQueries({ queryKey: ['profile'] });
      setEditing(false);
      toast.success('Profile updated');
      return data;
    },
    onError: () => toast.error('We could not update your profile. Please try again.'),
  });

  const days = useMemo(() => Array.from({ length: 364 }, (_, index) => {
    const date = new Date(); date.setHours(0, 0, 0, 0); date.setDate(date.getDate() - (363 - index));
    const key = date.toISOString().slice(0, 10); const value = activity?.activity?.[key];
    return { key, label: date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }), count: value?.count || 0, minutes: value?.minutes || 0 };
  }), [activity]);

  const beginEdit = () => { setForm({ name: user?.name || '', email: user?.email || '', target_role: profile?.target_role || '', career_goal: profile?.career_goal || '', bio: profile?.bio || '', experience_level: profile?.experience_level || 'beginner', weekly_hours: profile?.weekly_hours || 8, learning_style: profile?.learning_style || 'mixed' }); setEditing(true); };
  const updateField = (field: string, value: string | number) => setForm((current) => ({ ...current, [field]: value }));
  const handleImage = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!IMAGE_TYPES.has(file.type) || file.size > MAX_IMAGE_BYTES) { toast.error('Use a JPG, PNG, or WebP image smaller than 1 MB.'); event.target.value = ''; return; }
    const reader = new FileReader();
    reader.onload = () => save.mutate({ profile_image: String(reader.result) });
    reader.onerror = () => toast.error('That image could not be read.');
    reader.readAsDataURL(file);
  };

  const statCards: Array<{ label: string; value: string; Icon: typeof Flame }> = [
    { label: 'Current streak', value: `${activity?.current_streak || 0} days`, Icon: Flame },
    { label: 'Completed courses', value: String(completedQuery.data?.length || 0), Icon: CheckCircle2 },
    { label: 'Active learning days', value: String(activity?.total_active_days || 0), Icon: Clock3 },
    { label: 'Learning hours', value: `${Math.round((completedQuery.data || []).reduce((sum, item) => sum + (item.time_spent_hours || 0), 0))}h`, Icon: Clock3 },
  ];

  return <div className="p-4 sm:p-6 max-w-6xl mx-auto space-y-6">
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 sm:p-7">
      <div className="flex flex-col sm:flex-row sm:items-center gap-5">
        <div className="relative w-20 h-20 rounded-2xl overflow-hidden bg-indigo-600 flex items-center justify-center text-2xl font-bold text-white shrink-0">
          {profile?.profile_image ? <img src={profile.profile_image} alt={`${user?.name || 'User'} profile`} className="h-full w-full object-cover" /> : initials}
          <label className="absolute inset-x-0 bottom-0 bg-black/60 py-1 text-center cursor-pointer" aria-label="Change profile image"><Camera className="h-4 w-4 inline" /><input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleImage} className="sr-only" /></label>
        </div>
        <div className="flex-1 min-w-0"><h1 className="text-2xl font-bold text-white">{user?.name || 'Your profile'}</h1><p className="text-slate-400 mt-1">{user?.email}</p><div className="flex flex-wrap gap-2 mt-3"><span className="rounded-lg bg-indigo-950 text-indigo-300 px-2.5 py-1 text-sm">{profile?.target_role || 'Choose a target role'}</span><span className="rounded-lg bg-slate-800 text-slate-300 px-2.5 py-1 text-sm capitalize">{profile?.experience_level || 'New learner'}</span></div></div>
        <button onClick={beginEdit} className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 px-4 py-2.5 text-sm font-medium text-white"><Pencil className="h-4 w-4" /> Edit profile</button>
      </div>
    </section>

    <section className="grid grid-cols-2 lg:grid-cols-4 gap-3">{statCards.map(({ label, value, Icon }) => <div key={label} className="rounded-2xl border border-slate-800 bg-slate-900 p-4"><Icon className="h-5 w-5 text-indigo-400" /><p className="mt-3 text-xl font-bold text-white">{value}</p><p className="text-sm text-slate-400">{label}</p></div>)}</section>

    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 overflow-x-auto"><div className="flex items-start justify-between gap-4 mb-5"><div><h2 className="font-semibold text-white">Learning activity</h2><p className="text-sm text-slate-400">Daily study intensity for the last 12 weeks.</p></div><div className="text-right text-sm"><p className="text-white font-semibold">Longest: {activity?.longest_streak || 0} days</p><p className="text-slate-400">{activity?.total_active_days || 0} active days</p></div></div><div className="min-w-[560px] grid grid-flow-col grid-rows-7 gap-1 w-max">{days.map((day) => <div key={day.key} title={`${day.label}: ${day.count} activities, ${day.minutes} minutes`} aria-label={`${day.label}: ${day.count} learning activities, ${day.minutes} minutes`} className={`h-3 w-3 rounded-sm ${day.count === 0 ? 'bg-slate-800' : day.count === 1 ? 'bg-indigo-900' : day.count === 2 ? 'bg-indigo-700' : 'bg-indigo-400'}`} />)}</div></section>


    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5"><h2 className="font-semibold text-white">Completed learning</h2><p className="text-sm text-slate-400 mt-1">Courses and resources you have actually completed.</p><div className="mt-4 space-y-3">{completedQuery.isLoading ? <p className="text-slate-400">Loading completed learning…</p> : completedQuery.data?.length ? completedQuery.data.map((course) => <div key={course.id} className="rounded-xl bg-slate-800/70 p-4 flex flex-col sm:flex-row sm:items-center gap-3"><CheckCircle2 className="h-5 w-5 text-emerald-400" /><div className="flex-1"><p className="font-medium text-white">{course.title}</p><p className="text-sm text-slate-400">{course.provider} · {course.completed_at ? new Date(course.completed_at).toLocaleDateString() : 'Completed'}</p><p className="text-xs text-indigo-300 mt-1">{course.skills?.join(' · ')}</p></div><span className="text-sm text-slate-400">Level {course.difficulty}</span></div>) : <div className="py-8 text-center text-slate-400"><UserRound className="h-7 w-7 mx-auto mb-2 text-slate-600" />Your completed courses will appear here when you finish a learning resource.</div>}</div></section>

    {editing && <div className="fixed inset-0 z-50 bg-black/70 p-4 flex items-center justify-center"><form onSubmit={(event) => { event.preventDefault(); save.mutate(form); }} className="w-full max-w-lg rounded-2xl border border-slate-700 bg-slate-900 p-5 space-y-4 max-h-[90vh] overflow-y-auto"><div className="flex justify-between"><h2 className="font-semibold text-white">Edit profile</h2><button type="button" onClick={() => setEditing(false)} className="text-slate-400">Cancel</button></div>{[['name','Name'],['email','Email'],['target_role','Target career'],['career_goal','Learning goal']].map(([field,label]) => <label key={field} className="block text-sm text-slate-300">{label}<input required={field === 'name' || field === 'email'} value={String(form[field] || '')} onChange={(e) => updateField(field, e.target.value)} className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-white" /></label>)}<label className="block text-sm text-slate-300">Bio<textarea value={String(form.bio || '')} onChange={(e) => updateField('bio', e.target.value)} rows={3} className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-white" /></label><label className="block text-sm text-slate-300">Weekly learning hours<input type="number" min="1" max="80" value={Number(form.weekly_hours || 8)} onChange={(e) => updateField('weekly_hours', Number(e.target.value))} className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-white" /></label><label className="block text-sm text-slate-300">Experience<select value={String(form.experience_level)} onChange={(e) => updateField('experience_level', e.target.value)} className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-white"><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></label><label className="block text-sm text-slate-300">Learning style<select value={String(form.learning_style)} onChange={(e) => updateField('learning_style', e.target.value)} className="mt-1 w-full rounded-xl border border-slate-700 bg-slate-800 px-3 py-2 text-white"><option value="mixed">Mixed</option><option value="video">Video</option><option value="reading">Reading</option><option value="coding">Coding</option><option value="projects">Projects</option></select></label><button disabled={save.isPending} className="w-full rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 py-2.5 text-white font-medium">{save.isPending ? 'Saving…' : 'Save changes'}</button>{profile?.profile_image && <button type="button" onClick={() => save.mutate({ profile_image: null })} className="w-full text-sm text-rose-300 flex justify-center gap-2"><Trash2 className="h-4 w-4" /> Remove profile image</button>}</form></div>}
  </div>;
}
