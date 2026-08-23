// Utility functions
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDuration(hours: number): string {
  if (hours < 1) return `${Math.round(hours * 60)}min`;
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  return `${days}d`;
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
}

export function getDifficultyLabel(level: number): string {
  const labels = ['', 'Beginner', 'Easy', 'Intermediate', 'Advanced', 'Expert'];
  return labels[level] || 'Unknown';
}

export function getDifficultyColor(level: number): string {
  const colors = ['', 'text-green-600', 'text-blue-600', 'text-yellow-600', 'text-orange-600', 'text-red-600'];
  return colors[level] || 'text-gray-600';
}

export function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    critical: 'text-red-600 bg-red-50 border-red-200',
    high: 'text-orange-600 bg-orange-50 border-orange-200',
    medium: 'text-yellow-600 bg-yellow-50 border-yellow-200',
    low: 'text-green-600 bg-green-50 border-green-200',
  };
  return colors[priority] || 'text-gray-600 bg-gray-50';
}

export function getFormatIcon(format: string): string {
  const icons: Record<string, string> = {
    video: '🎥',
    article: '📄',
    course: '🎓',
    interactive: '💻',
    book: '📚',
    project: '🔨',
  };
  return icons[format] || '📌';
}

export function getScoreColor(score: number): string {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
}

export function getScoreBadge(score: number): string {
  if (score >= 85) return 'Perfect Match';
  if (score >= 70) return 'Great Match';
  if (score >= 55) return 'Good Match';
  if (score >= 40) return 'Fair Match';
  return 'Low Match';
}

export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

export function getStreakEmoji(streak: number): string {
  if (streak >= 30) return '🏆';
  if (streak >= 14) return '🔥';
  if (streak >= 7) return '⚡';
  if (streak >= 3) return '✨';
  return '💪';
}

export function calculateWeeksRemaining(totalWeeks: number, completionPercent: number): number {
  const completedWeeks = Math.floor((completionPercent / 100) * totalWeeks);
  return Math.max(0, totalWeeks - completedWeeks);
}

export function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 18) return 'Good afternoon';
  return 'Good evening';
}
