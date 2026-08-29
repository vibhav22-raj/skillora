'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, LearnerProfile } from '@/types';
import { authAPI } from '@/lib/api';

interface AuthState {
  user: User | null;
  profile: LearnerProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: Partial<User> & Pick<User, 'id'>) => void;
  setProfile: (profile: LearnerProfile) => void;
  demoLogin: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      profile: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const { data } = await authAPI.login(email, password);
          const { user, access_token } = data.data;
          localStorage.setItem('learnpath_token', access_token);
          set({ user, token: access_token, isAuthenticated: true, isLoading: false });
        } catch (e) {
          set({ isLoading: false });
          throw e;
        }
      },

      register: async (name, email, password) => {
        set({ isLoading: true });
        try {
          const { data } = await authAPI.register({ name, email, password });
          const { user, access_token } = data.data;
          localStorage.setItem('learnpath_token', access_token);
          set({ user, token: access_token, isAuthenticated: true, isLoading: false });
        } catch (e) {
          set({ isLoading: false });
          throw e;
        }
      },

      logout: () => {
        localStorage.removeItem('learnpath_token');
        set({ user: null, profile: null, token: null, isAuthenticated: false });
      },

      setUser: (user) => set((state) => ({ user: state.user ? { ...state.user, ...user } : user as User })),

      setProfile: (profile) => set({ profile }),

      demoLogin: async () => {
        set({ isLoading: true });
        try {
          const { data } = await authAPI.login('demo@skillora.io', 'DemoPass123');
          const { user, access_token } = data.data;
          localStorage.setItem('learnpath_token', access_token);
          set({ user, token: access_token, isAuthenticated: true, isLoading: false });
        } catch (e) {
          set({ isLoading: false });
          throw e;
        }
      },
    }),
    {
      name: 'learnpath-auth',
      partialize: (state) => ({ user: state.user, token: state.token, isAuthenticated: state.isAuthenticated }),
    }
  )
);
