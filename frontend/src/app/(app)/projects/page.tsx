'use client';

import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { projectsAPI } from '@/lib/api';
import { Folder, Clock, Star, ExternalLink, BriefcaseBusiness } from 'lucide-react';
import { getDifficultyLabel, getDifficultyColor } from '@/lib/utils';
import type { Project } from '@/types';

export default function ProjectsPage() {
  const { data: recommended, isLoading: loadingRec } = useQuery({
    queryKey: ['projects-recommended'],
    queryFn: () => projectsAPI.getRecommended().then((r) => r.data.data),
  });

  const { data: allProjects, isLoading: loadingAll } = useQuery({
    queryKey: ['projects-all'],
    queryFn: () => projectsAPI.getAll().then((r) => r.data.data),
  });
  const [domain, setDomain] = useState('All');
  const domains = useMemo(() => {
    const values = new Set((allProjects || []).map((project) => project.domain || project.category || 'Other'));
    return ['All', ...Array.from(values).sort()];
  }, [allProjects]);
  const visibleProjects = useMemo(() => {
    if (domain === 'All') return allProjects || [];
    return (allProjects || []).filter((project) => (project.domain || project.category) === domain);
  }, [allProjects, domain]);

  const DifficultyStars = ({ level }: { level: number }) => (
    <div className="flex gap-0.5">
      {[1,2,3,4,5].map((s) => (
        <Star key={s} className={`h-3.5 w-3.5 ${s <= level ? 'text-amber-400 fill-amber-400' : 'text-slate-700'}`} />
      ))}
    </div>
  );

  const ProjectCard = ({ project, index }: { project: Project; index: number }) => (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.07 }}
      className="bg-slate-900 border border-slate-800 hover:border-indigo-500/50 rounded-2xl p-5 flex flex-col transition-all group">
      {/* Category & difficulty */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded-lg">{project.domain || project.category}</span>
        <DifficultyStars level={project.difficulty} />
      </div>

      {/* Title */}
      <h3 className="text-white font-semibold leading-snug mb-2">{project.title}</h3>
      {project.description && (
        <p className="text-slate-400 text-sm leading-relaxed mb-3 flex-1 line-clamp-3">{project.description}</p>
      )}

      {/* Skills */}
      <div className="flex flex-wrap gap-1.5 mb-4">
        {(project.skills || []).slice(0, 4).map((s) => (
          <span key={s} className="bg-indigo-950/50 text-indigo-300 border border-indigo-800/50 text-xs px-2.5 py-0.5 rounded-lg">{s}</span>
        ))}
      </div>

      {project.business_value && (
        <div className="mb-4 rounded-xl bg-slate-800/70 border border-slate-700 p-3">
          <p className="text-xs font-medium text-slate-300 flex items-center gap-1.5 mb-1">
            <BriefcaseBusiness className="h-3.5 w-3.5 text-emerald-400" />
            Industry value
          </p>
          <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">{project.business_value}</p>
        </div>
      )}

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm text-slate-400 mb-4">
        <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> ~{project.duration_hours}h</span>
        <span className={getDifficultyColor(project.difficulty)}>{getDifficultyLabel(project.difficulty)}</span>
      </div>

      {/* Tags */}
      {project.tags?.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-4">
          {project.tags.slice(0, 3).map((t) => (
            <span key={t} className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">#{t}</span>
          ))}
        </div>
      )}

      {project.technologies && project.technologies.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-4">
          {project.technologies.slice(0, 4).map((tech) => (
            <span key={tech} className="text-xs text-cyan-300 bg-cyan-950/40 border border-cyan-900 px-2 py-0.5 rounded">{tech}</span>
          ))}
        </div>
      )}

      {project.resume_value && (
        <p className="text-xs text-emerald-300 mb-4">Resume value: {project.resume_value}</p>
      )}

      {/* Action */}
      {project.github_template_url ? (
        <a href={project.github_template_url} target="_blank" rel="noopener noreferrer"
          className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-indigo-900/50 border border-slate-700 hover:border-indigo-500 text-slate-300 hover:text-indigo-300 py-2.5 rounded-xl text-sm transition-all">
          <ExternalLink className="h-4 w-4" />
          View Template
        </a>
      ) : (
        <div className="flex items-center justify-center gap-2 bg-slate-800 border border-slate-700 text-slate-500 py-2.5 rounded-xl text-sm">
          Build from scratch
        </div>
      )}
    </motion.div>
  );

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Folder className="h-6 w-6 text-indigo-400" />
          Portfolio Projects
        </h1>
        <p className="text-slate-400 mt-1">50+ industry-oriented projects to build real skills and credible portfolio proof.</p>
      </div>

      {/* Recommended */}
      {!loadingRec && recommended && recommended.length > 0 && (
        <section className="mb-10">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Star className="h-5 w-5 text-amber-400" />
            Recommended for You
          </h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommended.slice(0, 3).map((p: Project, i: number) => (
              <ProjectCard key={p.id} project={p} index={i} />
            ))}
          </div>
        </section>
      )}

      {/* All projects */}
      <section>
        <h2 className="text-lg font-semibold text-white mb-4">All Projects</h2>
        <div className="flex gap-2 overflow-x-auto pb-4 mb-2">
          {domains.map((item) => (
            <button
              key={item}
              onClick={() => setDomain(item)}
              className={`whitespace-nowrap rounded-xl px-3 py-1.5 text-sm border ${domain === item ? 'bg-indigo-600 border-indigo-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-400'}`}
            >
              {item}
            </button>
          ))}
        </div>
        {loadingAll ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1,2,3,4,5,6].map((i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse">
                <div className="h-5 bg-slate-700 rounded w-2/3 mb-3" />
                <div className="h-4 bg-slate-700 rounded w-full mb-2" />
                <div className="h-4 bg-slate-700 rounded w-3/4" />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {visibleProjects.length === 0 && (
              <div className="sm:col-span-2 lg:col-span-3 rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400">
                No projects in this domain yet. Try another filter.
              </div>
            )}
            {(visibleProjects || []).map((p: Project, i: number) => (
              <ProjectCard key={p.id} project={p} index={i} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
