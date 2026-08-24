'use client';

import Link from 'next/link';

export default function RoleCard({ role, href, variant = 0 }: { role: string; href: string; variant?: number }) {
  const gradients = [
    'linearGradient(45deg,#7c3aed33 0%,#06b6d433 100%)',
    'linearGradient(45deg,#06b6d433 0%,#60a5fa33 100%)',
    'linearGradient(45deg,#8b5cf633 0%,#06b6d433 100%)',
  ];

  const bgColors = ['from-indigo-900/40', 'from-cyan-900/30', 'from-violet-900/30'];

  // derived colors for glow/variants
  const glowColors = ['rgba(124,58,237,0.18)', 'rgba(6,182,212,0.18)', 'rgba(139,92,246,0.18)'];
  const glowBox = { boxShadow: `0 12px 40px ${glowColors[variant] ?? glowColors[0]}` };

  return (
    <Link href={href} className="relative group inline-block w-52 sm:w-56 md:w-60">
      <div className="relative overflow-hidden rounded-2xl p-4 border border-slate-800 bg-slate-900/40 hover:border-transparent transition-all">
        {/* abstract svg background */}
        <svg className="absolute inset-0 w-full h-full opacity-20 pointer-events-none" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id={`g-${role.replace(/\s+/g,'')}-${variant}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={variant === 1 ? '#06b6d4' : variant === 2 ? '#8b5cf6' : '#7c3aed'} stopOpacity="0.18" />
              <stop offset="100%" stopColor={variant === 1 ? '#7c3aed' : variant === 2 ? '#06b6d4' : '#60a5fa'} stopOpacity="0.08" />
            </linearGradient>
          </defs>
          <rect x="-10" y="-10" width="220" height="140" fill={`url(#g-${role.replace(/\s+/g,'')}-${variant})`} />
          <g stroke={variant === 1 ? '#06b6d4' : variant === 2 ? '#8b5cf6' : '#7c3aed'} strokeWidth="0.6" fill="none">
            <path d="M10 80 C40 20, 80 10, 120 50" opacity="0.6" />
            <path d="M20 100 C60 40, 100 30, 140 70" opacity="0.45" />
            <circle cx="150" cy="30" r="2" />
            <circle cx="30" cy="20" r="1.6" />
            <circle cx="80" cy="60" r="1.8" />
          </g>
        </svg>

        <div className="relative z-10 flex items-center justify-between gap-2">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center bg-slate-800 border border-slate-700 z-10`}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-white opacity-90">
                  <path d="M12 2L15 8L22 9L17 14L18 21L12 18L6 21L7 14L2 9L9 8L12 2Z" fill="currentColor" />
                </svg>
              </div>

              {/* glow behind icon, appears on hover */}
              <div className="absolute -inset-1 rounded-lg z-0 opacity-0 group-hover:opacity-80 transition-opacity" style={{ background: variant === 1 ? 'radial-gradient(circle, rgba(6,182,212,0.18), rgba(6,182,212,0))' : variant === 2 ? 'radial-gradient(circle, rgba(139,92,246,0.18), rgba(139,92,246,0))' : 'radial-gradient(circle, rgba(124,58,237,0.18), rgba(124,58,237,0))', filter: 'blur(12px)' }} />
            </div>

            <div>
              <div className="text-sm text-slate-300">{role}</div>
              <div className="text-xs text-slate-500 mt-0.5">Explore path</div>
            </div>
          </div>
          <div className="opacity-0 group-hover:opacity-100 transition-opacity text-xs text-indigo-300">→</div>
        </div>
      </div>

      {/* glow outline around the card, appears on hover */}
      <div className="absolute inset-0 rounded-2xl pointer-events-none transition-all transform group-hover:scale-105 group-hover:opacity-100 opacity-0"
        style={{ ...glowBox, borderRadius: '12px' }} />
    </Link>
  );
}
