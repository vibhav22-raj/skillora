// All TypeScript types for LearnPath AI frontend

export interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
  is_demo: boolean;
}

export interface LearnerProfile {
  id: string;
  user_id: string;
  target_role: string | null;
  experience_level: 'beginner' | 'intermediate' | 'advanced' | null;
  education: string | null;
  career_goal: string | null;
  weekly_hours: number | null;
  learning_style: 'video' | 'reading' | 'coding' | 'projects' | 'mixed' | null;
  target_deadline: string | null;
  preferred_duration: 'short' | 'medium' | 'long' | null;
  strengths: string[];
  weaknesses: string[];
  bio: string | null;
  profile_image: string | null;
}


export interface Skill {
  id: string;
  name: string;
  category: string;
  description: string | null;
  difficulty: number;
  prerequisites: string[];
  tags: string[];
}

export interface UserSkill {
  skill_id: string;
  skill_name: string;
  current_level: number;
  target_level: number;
  gap_score: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

export interface SkillGap {
  skill_name: string;
  current_level: number;
  target_level: number;
  gap: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
  recommended_resources: string[];
  description?: string;
}

export interface LearningResource {
  id: string;
  title: string;
  description: string | null;
  provider: string | null;
  url: string;
  category: string | null;
  skills: string[];
  difficulty: number;
  duration_hours: number;
  format: 'video' | 'article' | 'course' | 'interactive' | 'book' | null;
  rating: number;
  tags: string[];
  is_free: boolean;
  prerequisites: string[];
  // Scoring fields (when recommended)
  score?: number;
  goal_relevance?: number;
  skill_gap_relevance?: number;
  prerequisite_fit?: number;
  difficulty_fit?: number;
  time_fit?: number;
  preference_fit?: number;
  explanation?: string;
}

export interface Project {
  id: string;
  title: string;
  description: string | null;
  skills: string[];
  difficulty: number;
  duration_hours: number;
  category: string | null;
  tags: string[];
  github_template_url: string | null;
  domain?: string | null;
  problem_statement?: string | null;
  business_value?: string | null;
  resume_value?: string | null;
  technologies?: string[] | null;
  architecture?: string | null;
  resume_bullet?: string | null;
}

export interface RoadmapPhase {
  phase_number: number;
  title: string;
  description: string;
  weeks: number;
  skills: string[];
  resources: Partial<LearningResource>[];
  projects: Partial<Project>[];
  milestones: string[];
  status: 'not_started' | 'in_progress' | 'completed';
  estimated_hours: number;
}

export interface Milestone {
  id: string;
  title: string;
  description: string;
  week: number;
  skills_gained: string[];
  phase: number;
  completion_criteria?: string;
}

export interface Roadmap {
  id: string;
  title: string;
  description: string | null;
  total_weeks: number;
  phases: RoadmapPhase[];
  milestones: Milestone[];
  generated_at: string;
  is_active: boolean;
}

export interface AssessmentQuestion {
  id: string;
  question: string;
  options: string[];
  type: string;
  difficulty?: string;
  topic?: string;
  explanation?: string;
}

export interface Assessment {
  id: string;
  skill_name: string | null;
  title: string;
  questions: AssessmentQuestion[];
  passing_score: number;
  estimated_minutes: number;
}

export interface AssessmentResult {
  score: number;
  passed: boolean;
  total_questions: number;
  correct_answers: number;
  skill_estimate: number;
  feedback: string;
  recommendations: string[];
  strong_areas?: string[];
  weak_areas?: string[];
  next_recommended_action?: string | null;
  recommended_resources?: string[];
  overall_feedback?: string;
  question_review?: {
    id: string;
    question: string;
    selected_answer: number;
    correct_answer: number;
    is_correct: boolean;
    explanation?: string;
    topic?: string;
    difficulty?: string;
  }[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface ChatSession {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Progress {
  id: string;
  resource_id: string | null;
  project_id: string | null;
  status: 'not_started' | 'in_progress' | 'completed' | 'skipped';
  completion_percentage: number;
  time_spent_hours: number;
}

export interface NextBestAction {
  title: string;
  description: string;
  type: string;
  resource_id: string | null;
  estimated_minutes: number;
  reason: string;
}

export interface TodayTask {
  title: string;
  type: string;
  estimated_minutes: number;
  resource_id?: string | null;
  completed: boolean;
}

export interface WeeklyActivity {
  day: string;
  date: string;
  hours: number;
  resources_completed: number;
}

export interface DashboardData {
  user_name: string;
  target_role: string | null;
  overall_progress: number;
  current_streak: number;
  hours_learned: number;
  skills_improved: number;
  completed_resources: number;
  in_progress_resources: number;
  next_best_action: NextBestAction | null;
  today_focus: TodayTask[];
  skill_gaps: SkillGap[];
  weekly_activity: WeeklyActivity[];
  current_milestone: Milestone | null;
  recent_recommendations: LearningResource[];
  roadmap_summary: {
    total_phases: number;
    total_weeks: number;
    title: string | null;
  };
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  data: T;
  message: string;
}

export interface PaginatedResponse<T> {
  resources: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
