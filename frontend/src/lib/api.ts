// Complete API client for LearnPath AI
import axios, { AxiosInstance } from 'axios';
import type {
  User, LearnerProfile, SkillGap, LearningResource, Project,
  Roadmap, Assessment, AssessmentResult, ChatMessage, ChatSession,
  DashboardData, ApiResponse, PaginatedResponse,
} from '@/types';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

// Auth token injection
// Auth token injection
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('learnpath_token');
    if (token) config.headers.Authorization = 'Bearer ' + token;
  }
  return config;
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('learnpath_token');
        localStorage.removeItem('learnpath_user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// â”€â”€â”€ Auth API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const authAPI = {
  register: (data: { name: string; email: string; password: string }) =>
    api.post<ApiResponse<{ user: User; access_token: string }>>('/api/auth/register', data),

  login: (email: string, password: string) =>
    api.post<ApiResponse<{ user: User; access_token: string }>>('/api/auth/login', { email, password }),

  me: () => api.get<ApiResponse<User>>('/api/auth/me'),

  logout: () => api.post('/api/auth/logout'),
};

// â”€â”€â”€ Profile API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const profileAPI = {
  get: () => api.get<ApiResponse<LearnerProfile>>('/api/profile/'),

  update: (data: Partial<LearnerProfile>) =>
    api.put<ApiResponse<LearnerProfile>>('/api/profile/', data),

  onboarding: (data: {
    goal: string;
    experience_level: string;
    current_skills: { name: string; level: number }[];
    weekly_hours: number;
    learning_style: string;
    target_deadline?: string;
  }) => api.post<ApiResponse<{ profile: LearnerProfile; skill_gaps: SkillGap[] }>>('/api/profile/onboarding', data),
};

// â”€â”€â”€ Dashboard API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const dashboardAPI = {
  get: () => api.get<ApiResponse<DashboardData>>('/api/dashboard/'),
};

// â”€â”€â”€ Learning Path API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const learningPathAPI = {
  generate: (data: {
    goal: string;
    free_text_goal?: string;
    experience_level: string;
    current_skills: { name: string; level: number }[];
    weekly_hours: number;
    learning_style: string;
    target_deadline?: string;
  }) => api.post<ApiResponse<{ roadmap: Roadmap; skill_gaps: SkillGap[] }>>('/api/learning-path/generate', data),

  get: () => api.get<ApiResponse<Roadmap>>('/api/learning-path/'),

  adapt: (feedback: string) =>
    api.post<ApiResponse<{ roadmap: Roadmap; adaptation: object }>>('/api/learning-path/adapt', { feedback }),
};

// â”€â”€â”€ Recommendations API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const recommendationsAPI = {
  get: (limit = 10) =>
    api.get<ApiResponse<LearningResource[]>>(`/api/recommendations/?limit=${limit}`),

  getNextAction: () =>
    api.get('/api/recommendations/next-best-action'),

  submitFeedback: (resourceId: string, data: { helpful: boolean; reason?: string; notes?: string }) =>
    api.post(`/api/recommendations/${resourceId}/feedback`, data),
};

// â”€â”€â”€ Skills API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const skillsAPI = {
  getAll: (category?: string) =>
    api.get<ApiResponse<import('@/types').Skill[]>>(`/api/skills/${category ? `?category=${category}` : ''}`),

  getMySkills: () =>
    api.get<ApiResponse<import('@/types').UserSkill[]>>('/api/skills/my-skills'),

  getGaps: () =>
    api.get<ApiResponse<SkillGap[]>>('/api/skills/gaps'),

  updateLevel: (skillName: string, level: number) =>
    api.put(`/api/skills/${encodeURIComponent(skillName)}/level`, { skill_name: skillName, level }),

  getRoles: () =>
    api.get<ApiResponse<string[]>>('/api/skills/roles'),
};

// â”€â”€â”€ Resources API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const resourcesAPI = {
  getAll: (params: {
    page?: number;
    per_page?: number;
    category?: string;
    difficulty?: number;
    format?: string;
    search?: string;
    free_only?: boolean;
  } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') query.set(k, String(v));
    });
    return api.get<ApiResponse<PaginatedResponse<LearningResource>>>(`/api/resources/?${query}`);
  },

  getOne: (id: string) =>
    api.get<ApiResponse<LearningResource>>(`/api/resources/${id}`),

  start: (id: string) =>
    api.post<ApiResponse<null>>(`/api/resources/${id}/start`),

  complete: (id: string) =>
    api.post<ApiResponse<null>>(`/api/resources/${id}/complete`),
};

// â”€â”€â”€ Projects API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const projectsAPI = {
  getAll: (params: { category?: string; difficulty?: number } = {}) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined) query.set(k, String(v));
    });
    return api.get<ApiResponse<Project[]>>(`/api/projects/?${query}`);
  },

  getRecommended: () =>
    api.get<ApiResponse<Project[]>>('/api/projects/recommended'),
};

// â”€â”€â”€ Assessment API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const assessmentAPI = {
  getAll: () =>
    api.get<ApiResponse<Assessment[]>>('/api/assessments/'),

  getOne: (id: string) =>
    api.get<ApiResponse<Assessment>>(`/api/assessments/${id}`),

  submit: (id: string, answers: Record<string, number>) =>
    api.post<ApiResponse<AssessmentResult>>(`/api/assessments/${id}/submit`, { answers }),

  getMyResults: () =>
    api.get('/api/assessments/results/my'),
};

// â”€â”€â”€ Chat API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const chatAPI = {
  sendMessage: (message: string, sessionId?: string) =>
    api.post<ApiResponse<{ session_id: string; message: ChatMessage }>>('/api/chat/message', {
      message,
      session_id: sessionId,
    }),

  getSessions: () =>
    api.get<ApiResponse<ChatSession[]>>('/api/chat/sessions'),

  getMessages: (sessionId: string) =>
    api.get<ApiResponse<ChatMessage[]>>(`/api/chat/sessions/${sessionId}/messages`),

  createSession: (title?: string) =>
    api.post<ApiResponse<{ id: string; title: string }>>('/api/chat/sessions', { title: title || 'New Conversation' }),
};

// â”€â”€â”€ Progress API â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
export const progressAPI = {
  get: () => api.get('/api/progress/'),
  update: (data: object) => api.post('/api/progress/update', data),
  getStreak: () => api.get('/api/progress/streak'),
};

export default api;
