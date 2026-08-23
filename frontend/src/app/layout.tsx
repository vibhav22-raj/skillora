import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'LearnPath AI – Personalized Learning Path Recommender',
  description:
    'AI-powered learning path recommender that creates personalized roadmaps based on your skills, goals, and learning style.',
  keywords: ['learning', 'AI', 'education', 'roadmap', 'skills', 'courses'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
