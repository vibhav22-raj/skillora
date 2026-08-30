'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  LayoutDashboard, Map, BookOpen, Star, MessageCircle,
  ClipboardList, TrendingUp, Brain, LogOut, Menu, User,
} from 'lucide-react';
import { useAuthStore } from '@/store/auth';
import { useState } from 'react';
import { cn } from '@/lib/utils';
import toast from 'react-hot-toast';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/roadmap', label: 'My Roadmap', icon: Map },
  { href: '/recommendations', label: 'Recommendations', icon: Star },
  { href: '/resources', label: 'Resources', icon: BookOpen },
  { href: '/skills', label: 'Skills & Gaps', icon: TrendingUp },
  { href: '/projects', label: 'Projects', icon: ClipboardList },
  { href: '/assessment', label: 'Assessments', icon: ClipboardList },
  { href: '/chat', label: 'AI Mentor', icon: MessageCircle },
  { href: '/profile', label: 'Profile', icon: User },
];

const mobileNavItems = [
  { href: '/dashboard', icon: LayoutDashboard, label: 'Home' },
  { href: '/roadmap', icon: Map, label: 'Roadmap' },
  { href: '/recommendations', icon: Star, label: 'Learn' },
  { href: '/chat', icon: MessageCircle, label: 'AI' },
  { href: '/profile', icon: User, label: 'Profile' },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { isAuthenticated, user, logout } = useAuthStore();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) return null;

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    router.push('/');
  };

  const initials = user?.name?.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2) || 'U';

  const Sidebar = ({ mobile = false }) => (
    <div className={cn(
      'flex flex-col h-full bg-slate-900 border-r border-slate-800',
      mobile ? 'w-64' : 'w-64'
    )}>
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-5 py-5 border-b border-slate-800">
        <Brain className="h-7 w-7 text-indigo-500 flex-shrink-0" />
        <span className="font-bold text-lg text-white">Skillora <span className="text-indigo-400">AI</span></span>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link key={item.href} href={item.href}
              onClick={() => setSidebarOpen(false)}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all',
                active
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'
              )}>
              <item.icon className="h-5 w-5 flex-shrink-0" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* User — clickable to profile */}
      <div className="px-3 py-4 border-t border-slate-800">
        <Link href="/profile" onClick={() => setSidebarOpen(false)}
          className="flex items-center gap-3 px-3 py-2 rounded-xl mb-2 hover:bg-slate-800 transition-all group">
          <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold text-white flex-shrink-0 group-hover:bg-indigo-500 transition-colors">
            {initials}
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-white truncate">{user?.name || 'User'}</p>
            <p className="text-xs text-slate-500 truncate">{user?.email}</p>
          </div>
        </Link>
        <button onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-slate-400 hover:text-white hover:bg-slate-800 transition-all w-full">
          <LogOut className="h-5 w-5" />
          Sign Out
        </button>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-slate-950 text-white overflow-hidden">
      {/* Desktop sidebar */}
      <div className="hidden md:flex flex-shrink-0">
        <Sidebar />
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div className="absolute inset-0 bg-black/60" onClick={() => setSidebarOpen(false)} />
          <motion.div initial={{ x: -256 }} animate={{ x: 0 }} exit={{ x: -256 }}
            className="absolute left-0 top-0 h-full">
            <Sidebar mobile />
          </motion.div>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Mobile topbar */}
        <div className="flex md:hidden items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900">
          <button onClick={() => setSidebarOpen(true)}><Menu className="h-6 w-6" /></button>
          <span className="font-bold text-white">Skillora</span>
          <Link href="/profile">
            <div className="w-7 h-7 rounded-full bg-indigo-600 flex items-center justify-center text-xs font-bold text-white">
              {initials}
            </div>
          </Link>
        </div>

        {/* Page content — padding-bottom on mobile to avoid overlap with bottom nav */}
        <main className="flex-1 overflow-y-auto pb-16 md:pb-0 space-shell">
          <div className="p-6 max-w-7xl mx-auto">
            {children}
          </div>
        </main>

        {/* Mobile bottom navigation */}
        <nav className="fixed bottom-0 left-0 right-0 z-40 md:hidden bg-slate-900/95 backdrop-blur-md border-t border-slate-800">
          <div className="flex items-center justify-around px-2 py-2">
            {mobileNavItems.map((item) => {
              const active = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'flex flex-col items-center gap-1 px-3 py-1.5 rounded-xl transition-all min-w-0',
                    active ? 'text-indigo-400' : 'text-slate-500 hover:text-slate-300'
                  )}
                >
                  <item.icon className={cn('h-5 w-5', active && 'scale-110')} />
                  <span className="text-[10px] font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>
        </nav>
      </div>
    </div>
  );
}

