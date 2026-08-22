import os

base_dir = r"F:\github clone rep\HCL_Amplified\backend\app\recommender"

scorer = """def calculate_score(goal_relevance: float, skill_gap_relevance: float, 
                    prerequisite_fit: float, difficulty_fit: float, 
                    time_fit: float, preference_fit: float) -> float:
    score = (
        goal_relevance       * 0.25 +
        skill_gap_relevance  * 0.25 +
        prerequisite_fit     * 0.20 +
        difficulty_fit       * 0.15 +
        time_fit             * 0.10 +
        preference_fit       * 0.05
    ) * 100
    return round(score, 2)
"""
with open(os.path.join(base_dir, "scorer.py"), "w") as f:
    f.write(scorer)

skill_gap = """ROLE_SKILLS = {
  'AI/ML Engineer': [
    {'skill': 'Python', 'target_level': 4},
    {'skill': 'DSA', 'target_level': 3},
    {'skill': 'Statistics', 'target_level': 4},
    {'skill': 'Linear Algebra', 'target_level': 3},
    {'skill': 'SQL', 'target_level': 3},
    {'skill': 'Machine Learning', 'target_level': 5},
    {'skill': 'Deep Learning', 'target_level': 4},
    {'skill': 'Python Libraries (NumPy/Pandas)', 'target_level': 4},
    {'skill': 'Model Deployment', 'target_level': 3},
    {'skill': 'Git', 'target_level': 3},
  ],
  'Data Scientist': [
    {'skill': 'Python', 'target_level': 5},
    {'skill': 'SQL', 'target_level': 4},
    {'skill': 'Statistics', 'target_level': 5},
  ]
}

def calculate_gaps(target_role: str, current_skills: dict) -> list:
    required = ROLE_SKILLS.get(target_role, [])
    gaps = []
    for req in required:
        skill = req['skill']
        target = req['target_level']
        current = current_skills.get(skill, 0)
        gap = target - current
        if gap > 0:
            priority = 'high' if gap >= 3 else 'medium' if gap == 2 else 'low'
            gaps.append({
                'skill_name': skill,
                'current_level': current,
                'target_level': target,
                'gap': gap,
                'priority': priority,
                'recommended_resources': []
            })
    return gaps
"""
with open(os.path.join(base_dir, "skill_gap.py"), "w") as f:
    f.write(skill_gap)

prereq = """PREREQUISITE_GRAPH = {
  'Machine Learning': ['Python', 'Statistics', 'Linear Algebra', 'Python Libraries (NumPy/Pandas)'],
  'Deep Learning': ['Machine Learning'],
  'NLP': ['Deep Learning', 'Python'],
  'Computer Vision': ['Deep Learning']
}

def get_prerequisites(skill: str) -> list:
    res = []
    stack = [skill]
    while stack:
        curr = stack.pop()
        reqs = PREREQUISITE_GRAPH.get(curr, [])
        for r in reqs:
            if r not in res:
                res.append(r)
                stack.append(r)
    return res

def get_learning_order(skills: list) -> list:
    # simple topological sort logic mapping
    order = []
    visited = set()
    def dfs(s):
        if s in visited: return
        visited.add(s)
        for req in PREREQUISITE_GRAPH.get(s, []):
            dfs(req)
        order.append(s)
    for s in skills:
        dfs(s)
    return order

def check_prerequisite_fit(user_skills: list, resource_prerequisites: list) -> float:
    if not resource_prerequisites:
        return 1.0
    met = sum(1 for p in resource_prerequisites if p in user_skills)
    return met / len(resource_prerequisites)
"""
with open(os.path.join(base_dir, "prerequisite_graph.py"), "w") as f:
    f.write(prereq)

roadmap = """def generate_roadmap(target_role, skill_gaps, weekly_hours, deadline, style):
    phases = []
    total_weeks = 12
    # mock logic
    phases.append({
        "phase_number": 1,
        "title": f"Foundations for {target_role}",
        "description": "Getting started with basics",
        "weeks": 4,
        "skills": [g['skill_name'] for g in skill_gaps[:2]],
        "resources": [],
        "projects": [],
        "milestones": ["Complete basics"]
    })
    return {
        "phases": phases,
        "total_weeks": total_weeks,
        "milestones": ["Complete basics"]
    }
"""
with open(os.path.join(base_dir, "roadmap_generator.py"), "w") as f:
    f.write(roadmap)
    
print("Recommenders complete.")
