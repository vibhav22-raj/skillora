'use client';

import { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { chatAPI } from '@/lib/api';
import { MessageCircle, Send, Plus, Brain, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import toast from 'react-hot-toast';
import type { ChatSession, ChatMessage } from '@/types';

const QUICK_PROMPTS = [
  'What should I study today?',
  'Explain my roadmap',
  "I'm struggling with statistics",
  'I only have 30 minutes today',
  'What project should I build?',
  'Why did you recommend this?',
];

export default function ChatPage() {
  const queryClient = useQueryClient();
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => { scrollToBottom(); }, [messages]);

  const { data: sessions } = useQuery({
    queryKey: ['chat-sessions'],
    queryFn: () => chatAPI.getSessions().then((r) => r.data.data),
  });

  const { data: sessionMessages, isLoading: loadingMessages } = useQuery({
    queryKey: ['chat-messages', currentSessionId],
    queryFn: () => currentSessionId ? chatAPI.getMessages(currentSessionId).then((r) => r.data.data) : Promise.resolve([]),
    enabled: !!currentSessionId,
  });

  useEffect(() => {
    if (sessionMessages) setMessages(sessionMessages);
  }, [sessionMessages]);

  const sendMutation = useMutation({
    mutationFn: (message: string) => chatAPI.sendMessage(message, currentSessionId || undefined),
    onMutate: (message) => {
      const userMsg: ChatMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: message,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMsg]);
    },
    onSuccess: (res) => {
      const { session_id, message } = res.data.data;
      setCurrentSessionId(session_id);
      setMessages((prev) => [...prev, message]);
      queryClient.invalidateQueries({ queryKey: ['chat-sessions'] });
    },
    onError: () => toast.error('Could not send message. Please try again.'),
  });

  const handleSend = () => {
    if (!inputText.trim() || sendMutation.isPending) return;
    const text = inputText.trim();
    setInputText('');
    sendMutation.mutate(text);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const startNewChat = async () => {
    setCurrentSessionId(null);
    setMessages([]);
  };

  return (
    <div className="flex h-full" style={{ height: 'calc(100vh - 56px)' }}>
      {/* Sessions sidebar */}
      <div className="w-64 shrink-0 border-r border-slate-800 bg-linear-to-b from-slate-900 to-slate-950 md:flex flex-col hidden">
        <div className="p-4 border-b border-slate-800/50">
          <motion.button 
            onClick={startNewChat}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full flex items-center justify-center gap-2 bg-linear-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-medium py-2.5 rounded-xl transition-all text-sm shadow-lg shadow-indigo-500/20">
            <Plus className="h-4 w-4" />
            New Conversation
          </motion.button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {(sessions || []).map((session: ChatSession) => (
            <motion.button 
              key={session.id}
              onClick={() => { setCurrentSessionId(session.id); setMessages([]); }}
              whileHover={{ scale: 1.02, x: 4 }}
              className={`w-full text-left px-3 py-2.5 rounded-xl text-sm transition-all ${currentSessionId === session.id
                ? 'bg-indigo-900/60 text-indigo-300 border border-indigo-700/50 shadow-lg shadow-indigo-900/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50 hover:border-slate-700/30 border border-slate-800/30'
              }`}>
              <p className="truncate font-medium">{session.title}</p>
              <p className="text-xs text-slate-500 mt-0.5">
                {new Date(session.updated_at).toLocaleDateString()}
              </p>
            </motion.button>
          ))}
          {(!sessions || sessions.length === 0) && (
            <p className="text-slate-600 text-xs text-center py-4">No conversations yet</p>
          )}
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col bg-slate-950">
        {/* Chat header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800 bg-slate-900">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-900 flex items-center justify-center">
              <Brain className="h-5 w-5 text-indigo-400" />
            </div>
            <div>
              <p className="text-white font-semibold">Skillora AI Mentor</p>
              <p className="text-slate-500 text-xs">Personalized learning guidance</p>
            </div>
          </div>
          <button onClick={startNewChat} className="md:hidden flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg text-xs transition-all">
            <Plus className="h-3.5 w-3.5" /> New
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 sm:px-8 py-6 space-y-6">
          {/* Welcome state */}
          {messages.length === 0 && !loadingMessages && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              className="text-center max-w-lg mx-auto pt-8">
              <div className="w-16 h-16 bg-indigo-900 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Brain className="h-8 w-8 text-indigo-400" />
              </div>
              <h2 className="text-xl font-bold text-white mb-2">Your AI Learning Mentor</h2>
              <p className="text-slate-400 mb-6">Ask me anything about your learning journey. I know your goals, skills, and roadmap.</p>
              <div className="flex flex-wrap gap-2 justify-center">
                {QUICK_PROMPTS.map((prompt, idx) => (
                  <motion.button 
                    key={prompt} 
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.08 }}
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => { setInputText(prompt); }}
                    className="bg-slate-900/80 backdrop-blur hover:bg-slate-800 border border-slate-700/50 hover:border-indigo-500/50 text-slate-300 hover:text-indigo-300 px-4 py-2.5 rounded-xl text-sm transition-all">
                    {prompt}
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Chat messages */}
          <AnimatePresence mode="popLayout">
            {messages.map((msg, idx) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 8, scale: 0.96 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ delay: idx * 0.02, duration: 0.3 }}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                {/* Avatar */}
                <motion.div 
                  whileHover={{ scale: 1.1 }}
                  className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1 ${msg.role === 'assistant' ? 'bg-linear-to-br from-indigo-600 to-indigo-700 shadow-lg shadow-indigo-500/20' : 'bg-slate-700 shadow-lg shadow-slate-500/10'}`}>
                  {msg.role === 'assistant'
                    ? <Brain className="h-4 w-4 text-white" />
                    : <User className="h-4 w-4 text-slate-300" />
                  }
                </motion.div>

                {/* Bubble */}
                <motion.div 
                  whileHover={{ scale: 1.02 }}
                  className={`max-w-xs sm:max-w-md lg:max-w-lg rounded-2xl px-5 py-4 transition-all ${msg.role === 'user'
                    ? 'bg-linear-to-br from-indigo-600 to-indigo-500 text-white shadow-lg shadow-indigo-500/20'
                    : 'bg-slate-900/80 border border-slate-800/50 hover:border-slate-700/50 text-slate-200 backdrop-blur'
                  }`}>
                  {msg.role === 'assistant' ? (
                    <div className="prose-ai text-sm leading-relaxed">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  ) : (
                    <p className="text-sm">{msg.content}</p>
                  )}
                </motion.div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          {sendMutation.isPending && (
            <motion.div 
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3">
              <motion.div 
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-8 h-8 rounded-xl bg-linear-to-br from-indigo-600 to-indigo-700 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                <Brain className="h-4 w-4 text-white" />
              </motion.div>
              <div className="bg-slate-900/80 border border-slate-800/50 backdrop-blur rounded-2xl px-5 py-4">
                <div className="flex gap-1.5 items-center h-5">
                  {[0, 1, 2].map((i) => (
                    <motion.div 
                      key={i} 
                      className="w-2 h-2 bg-indigo-400 rounded-full"
                      animate={{ y: [-6, 6, -6] }}
                      transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.15 }}
                    />
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-4 sm:px-8 py-4 border-t border-slate-800 bg-linear-to-t from-slate-950 to-slate-900/50">
          <div className="flex gap-3 max-w-3xl mx-auto">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask your AI mentor anything... (Enter to send)"
              className="flex-1 bg-slate-900/80 backdrop-blur border border-slate-700/50 hover:border-slate-600/50 focus:border-indigo-500/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none resize-none text-sm transition-all"
              rows={1}
              style={{ maxHeight: '120px', overflowY: 'auto' }}
            />
            <motion.button 
              onClick={handleSend}
              disabled={!inputText.trim() || sendMutation.isPending}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-linear-to-br from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 disabled:from-slate-700 disabled:to-slate-700 disabled:opacity-40 text-white p-3 rounded-xl transition-all flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20 disabled:shadow-none">
              <Send className="h-5 w-5" />
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  );
}
