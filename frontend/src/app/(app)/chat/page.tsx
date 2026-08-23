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
      <div className="w-64 flex-shrink-0 border-r border-slate-800 bg-slate-900 flex flex-col hidden md:flex">
        <div className="p-4 border-b border-slate-800">
          <button onClick={startNewChat}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-xl transition-all text-sm">
            <Plus className="h-4 w-4" />
            New Conversation
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {(sessions || []).map((session: ChatSession) => (
            <button key={session.id}
              onClick={() => { setCurrentSessionId(session.id); setMessages([]); }}
              className={`w-full text-left px-3 py-2.5 rounded-xl text-sm transition-all ${currentSessionId === session.id
                ? 'bg-indigo-900/50 text-indigo-300 border border-indigo-700/50'
                : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`}>
              <p className="truncate font-medium">{session.title}</p>
              <p className="text-xs text-slate-500 mt-0.5">
                {new Date(session.updated_at).toLocaleDateString()}
              </p>
            </button>
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
              <p className="text-white font-semibold">LearnPath AI Mentor</p>
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
                {QUICK_PROMPTS.map((prompt) => (
                  <button key={prompt} onClick={() => { setInputText(prompt); }}
                    className="bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-indigo-500 text-slate-300 hover:text-white px-4 py-2 rounded-xl text-sm transition-all">
                    {prompt}
                  </button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Chat messages */}
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 ${msg.role === 'assistant' ? 'bg-indigo-900' : 'bg-slate-700'}`}>
                  {msg.role === 'assistant'
                    ? <Brain className="h-4 w-4 text-indigo-400" />
                    : <User className="h-4 w-4 text-slate-300" />
                  }
                </div>

                {/* Bubble */}
                <div className={`max-w-[75%] rounded-2xl px-5 py-4 ${msg.role === 'user'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-900 border border-slate-800 text-slate-200'
                }`}>
                  {msg.role === 'assistant' ? (
                    <div className="prose-ai text-sm leading-relaxed">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  ) : (
                    <p className="text-sm">{msg.content}</p>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          {sendMutation.isPending && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="flex gap-3">
              <div className="w-8 h-8 rounded-xl bg-indigo-900 flex items-center justify-center">
                <Brain className="h-4 w-4 text-indigo-400" />
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-2xl px-5 py-4">
                <div className="flex gap-1.5 items-center h-5">
                  {[0, 1, 2].map((i) => (
                    <div key={i} className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-4 sm:px-8 py-4 border-t border-slate-800 bg-slate-900">
          <div className="flex gap-3 max-w-3xl mx-auto">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask your AI mentor anything... (Enter to send)"
              className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none text-sm"
              rows={1}
              style={{ maxHeight: '120px', overflowY: 'auto' }}
            />
            <button onClick={handleSend}
              disabled={!inputText.trim() || sendMutation.isPending}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white p-3 rounded-xl transition-all flex items-center justify-center flex-shrink-0">
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
