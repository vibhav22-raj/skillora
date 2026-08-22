"""
Prerequisite Graph — Directed Acyclic Graph of skill dependencies.
Used for topological ordering and prerequisite validation.
"""
from typing import Dict, List, Set


# ─── Prerequisite Graph ────────────────────────────────────────────────────
# Key = skill, Value = list of prerequisite skills
PREREQUISITE_GRAPH: Dict[str, List[str]] = {
    # Python ecosystem
    "NumPy/Pandas": ["Python"],
    "Data Visualization": ["Python", "NumPy/Pandas"],
    "Web Scraping": ["Python"],
    
    # ML prerequisites
    "Machine Learning": ["Python", "Statistics", "Linear Algebra", "NumPy/Pandas"],
    "Deep Learning": ["Machine Learning"],
    "NLP": ["Deep Learning", "Python"],
    "Computer Vision": ["Deep Learning"],
    "Generative AI": ["Deep Learning", "NLP"],
    "Reinforcement Learning": ["Deep Learning"],
    "Model Deployment": ["Machine Learning", "Docker"],
    
    # Math
    "Linear Algebra": ["Mathematics"],
    "Statistics": ["Mathematics"],
    
    # Web
    "React": ["HTML/CSS", "JavaScript"],
    "TypeScript": ["JavaScript"],
    "Next.js": ["React", "JavaScript"],
    "Node.js": ["JavaScript"],
    "REST APIs": ["Programming Basics"],
    
    # Backend / DevOps
    "FastAPI": ["Python"],
    "Django": ["Python"],
    "Docker": ["Linux"],
    "Kubernetes": ["Docker"],
    "CI/CD": ["Git", "Docker"],
    "Terraform": ["AWS/GCP/Azure", "Linux"],
    
    # DSA
    "Advanced DSA": ["DSA"],
    "System Design": ["DSA", "SQL", "REST APIs"],
    
    # Data
    "Power BI/Tableau": ["SQL", "Data Visualization"],
    "A/B Testing": ["Statistics"],
    
    # Security
    "Ethical Hacking": ["Networking", "Linux", "Security"],
    "Cryptography": ["Mathematics", "Security"],
    
    # Base skills (no prerequisites)
    "Python": [],
    "JavaScript": [],
    "HTML/CSS": [],
    "SQL": [],
    "Git": [],
    "Linux": [],
    "Networking": [],
    "Mathematics": [],
    "Programming Basics": [],
    "DSA": [],
    "Security": [],
    "AWS/GCP/Azure": ["Linux"],
    "Monitoring": ["Docker", "Linux"],
}


def get_prerequisites(skill: str, visited: Set[str] = None) -> List[str]:
    """Get all transitive prerequisites for a skill (DFS)."""
    if visited is None:
        visited = set()
    if skill in visited:
        return []
    visited.add(skill)
    
    direct_prereqs = PREREQUISITE_GRAPH.get(skill, [])
    all_prereqs = list(direct_prereqs)
    
    for prereq in direct_prereqs:
        transitive = get_prerequisites(prereq, visited)
        for t in transitive:
            if t not in all_prereqs:
                all_prereqs.append(t)
    
    return all_prereqs


def get_learning_order(skills: List[str]) -> List[str]:
    """
    Topological sort — returns skills in learning order.
    Prerequisites come before skills that depend on them.
    """
    order = []
    visited: Set[str] = set()

    def dfs(skill: str) -> None:
        if skill in visited:
            return
        visited.add(skill)
        for prereq in PREREQUISITE_GRAPH.get(skill, []):
            dfs(prereq)
        order.append(skill)

    for skill in skills:
        dfs(skill)

    return order


def check_prerequisite_fit(user_skills: List[str], resource_prerequisites: List[str]) -> float:
    """
    Calculate how well user's skills meet resource prerequisites.
    Returns 0.0-1.0 (1.0 = all prerequisites met).
    """
    if not resource_prerequisites:
        return 1.0
    met = sum(1 for p in resource_prerequisites if p in user_skills)
    return met / len(resource_prerequisites)


def get_missing_prerequisites(user_skills: List[str], skill: str) -> List[str]:
    """Get prerequisites for a skill that the user hasn't learned yet."""
    all_prereqs = get_prerequisites(skill)
    return [p for p in all_prereqs if p not in user_skills]


def are_prerequisites_met(user_skills: List[str], skill: str) -> bool:
    """Check if user has all direct prerequisites for a skill."""
    direct_prereqs = PREREQUISITE_GRAPH.get(skill, [])
    return all(p in user_skills for p in direct_prereqs)
