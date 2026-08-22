"""
Skill Gap Engine — Compares user's current skills vs target role requirements.
Calculates gap scores and priorities for each skill.
"""
from typing import Dict, List, Optional

# ─── Role Skill Requirements ───────────────────────────────────────────────
ROLE_SKILLS: Dict[str, List[Dict]] = {
    "AI/ML Engineer": [
        {"skill": "Python", "target_level": 4, "weight": 1.0},
        {"skill": "DSA", "target_level": 3, "weight": 0.7},
        {"skill": "Statistics", "target_level": 4, "weight": 0.9},
        {"skill": "Linear Algebra", "target_level": 3, "weight": 0.8},
        {"skill": "SQL", "target_level": 3, "weight": 0.6},
        {"skill": "Machine Learning", "target_level": 5, "weight": 1.0},
        {"skill": "Deep Learning", "target_level": 4, "weight": 0.9},
        {"skill": "NumPy/Pandas", "target_level": 4, "weight": 0.85},
        {"skill": "Model Deployment", "target_level": 3, "weight": 0.7},
        {"skill": "Git", "target_level": 3, "weight": 0.6},
        {"skill": "Docker", "target_level": 2, "weight": 0.5},
    ],
    "Data Scientist": [
        {"skill": "Python", "target_level": 5, "weight": 1.0},
        {"skill": "SQL", "target_level": 4, "weight": 0.9},
        {"skill": "Statistics", "target_level": 5, "weight": 1.0},
        {"skill": "Linear Algebra", "target_level": 3, "weight": 0.8},
        {"skill": "Machine Learning", "target_level": 4, "weight": 0.9},
        {"skill": "NumPy/Pandas", "target_level": 5, "weight": 0.95},
        {"skill": "Data Visualization", "target_level": 4, "weight": 0.8},
        {"skill": "Deep Learning", "target_level": 3, "weight": 0.7},
        {"skill": "Git", "target_level": 3, "weight": 0.6},
        {"skill": "A/B Testing", "target_level": 3, "weight": 0.7},
    ],
    "Data Analyst": [
        {"skill": "SQL", "target_level": 5, "weight": 1.0},
        {"skill": "Python", "target_level": 3, "weight": 0.8},
        {"skill": "Statistics", "target_level": 3, "weight": 0.8},
        {"skill": "Data Visualization", "target_level": 4, "weight": 0.9},
        {"skill": "NumPy/Pandas", "target_level": 3, "weight": 0.8},
        {"skill": "Excel/Sheets", "target_level": 4, "weight": 0.9},
        {"skill": "Power BI/Tableau", "target_level": 3, "weight": 0.8},
        {"skill": "Git", "target_level": 2, "weight": 0.5},
    ],
    "Software Engineer": [
        {"skill": "Python", "target_level": 4, "weight": 0.9},
        {"skill": "DSA", "target_level": 5, "weight": 1.0},
        {"skill": "System Design", "target_level": 4, "weight": 0.9},
        {"skill": "SQL", "target_level": 3, "weight": 0.7},
        {"skill": "Git", "target_level": 4, "weight": 0.9},
        {"skill": "Docker", "target_level": 3, "weight": 0.7},
        {"skill": "REST APIs", "target_level": 4, "weight": 0.85},
        {"skill": "Testing", "target_level": 3, "weight": 0.7},
        {"skill": "Linux", "target_level": 3, "weight": 0.7},
    ],
    "Frontend Developer": [
        {"skill": "HTML/CSS", "target_level": 5, "weight": 1.0},
        {"skill": "JavaScript", "target_level": 5, "weight": 1.0},
        {"skill": "React", "target_level": 4, "weight": 0.9},
        {"skill": "TypeScript", "target_level": 3, "weight": 0.8},
        {"skill": "Git", "target_level": 3, "weight": 0.7},
        {"skill": "UI/UX Design", "target_level": 3, "weight": 0.7},
        {"skill": "Testing", "target_level": 3, "weight": 0.6},
        {"skill": "Performance", "target_level": 3, "weight": 0.7},
    ],
    "Backend Developer": [
        {"skill": "Python", "target_level": 4, "weight": 0.9},
        {"skill": "DSA", "target_level": 4, "weight": 0.85},
        {"skill": "SQL", "target_level": 4, "weight": 0.9},
        {"skill": "REST APIs", "target_level": 5, "weight": 1.0},
        {"skill": "System Design", "target_level": 4, "weight": 0.9},
        {"skill": "Git", "target_level": 4, "weight": 0.8},
        {"skill": "Docker", "target_level": 3, "weight": 0.7},
        {"skill": "Linux", "target_level": 3, "weight": 0.7},
        {"skill": "Security", "target_level": 3, "weight": 0.7},
    ],
    "Full Stack Developer": [
        {"skill": "HTML/CSS", "target_level": 4, "weight": 0.85},
        {"skill": "JavaScript", "target_level": 4, "weight": 0.9},
        {"skill": "React", "target_level": 3, "weight": 0.8},
        {"skill": "Python", "target_level": 3, "weight": 0.8},
        {"skill": "SQL", "target_level": 3, "weight": 0.75},
        {"skill": "REST APIs", "target_level": 4, "weight": 0.9},
        {"skill": "Git", "target_level": 4, "weight": 0.85},
        {"skill": "Docker", "target_level": 2, "weight": 0.6},
        {"skill": "DSA", "target_level": 3, "weight": 0.7},
    ],
    "Cloud Engineer": [
        {"skill": "Linux", "target_level": 4, "weight": 0.9},
        {"skill": "Python", "target_level": 3, "weight": 0.7},
        {"skill": "AWS/GCP/Azure", "target_level": 5, "weight": 1.0},
        {"skill": "Docker", "target_level": 4, "weight": 0.9},
        {"skill": "Kubernetes", "target_level": 4, "weight": 0.9},
        {"skill": "Terraform", "target_level": 3, "weight": 0.8},
        {"skill": "CI/CD", "target_level": 4, "weight": 0.85},
        {"skill": "Networking", "target_level": 3, "weight": 0.7},
        {"skill": "Security", "target_level": 3, "weight": 0.7},
    ],
    "DevOps Engineer": [
        {"skill": "Linux", "target_level": 5, "weight": 1.0},
        {"skill": "Docker", "target_level": 5, "weight": 1.0},
        {"skill": "Kubernetes", "target_level": 4, "weight": 0.9},
        {"skill": "CI/CD", "target_level": 5, "weight": 1.0},
        {"skill": "Python", "target_level": 3, "weight": 0.7},
        {"skill": "AWS/GCP/Azure", "target_level": 4, "weight": 0.9},
        {"skill": "Terraform", "target_level": 4, "weight": 0.85},
        {"skill": "Monitoring", "target_level": 3, "weight": 0.7},
        {"skill": "Git", "target_level": 4, "weight": 0.85},
    ],
    "Cybersecurity Analyst": [
        {"skill": "Networking", "target_level": 5, "weight": 1.0},
        {"skill": "Linux", "target_level": 4, "weight": 0.9},
        {"skill": "Security", "target_level": 5, "weight": 1.0},
        {"skill": "Python", "target_level": 3, "weight": 0.7},
        {"skill": "Ethical Hacking", "target_level": 4, "weight": 0.9},
        {"skill": "Cryptography", "target_level": 3, "weight": 0.8},
        {"skill": "SQL", "target_level": 2, "weight": 0.5},
    ],
}

# ─── Skill Descriptions ────────────────────────────────────────────────────
SKILL_DESCRIPTIONS: Dict[str, str] = {
    "Python": "Core programming language for AI/ML, data science, and general development",
    "Machine Learning": "Algorithms for teaching machines to learn from data",
    "Deep Learning": "Neural networks for complex pattern recognition tasks",
    "Statistics": "Mathematical foundation for data analysis and ML",
    "DSA": "Data Structures and Algorithms — foundation for software engineering",
    "SQL": "Database querying language essential for data roles",
    "NumPy/Pandas": "Python libraries for numerical computing and data manipulation",
}


def calculate_priority(gap: int, weight: float) -> str:
    """Determine priority based on gap size and role importance weight."""
    weighted_gap = gap * weight
    if weighted_gap >= 3.5:
        return "critical"
    elif weighted_gap >= 2.5:
        return "high"
    elif weighted_gap >= 1.0:
        return "medium"
    return "low"


def calculate_gaps(target_role: str, current_skills: Dict[str, int]) -> List[Dict]:
    """
    Calculate skill gaps for a target role.
    
    Args:
        target_role: Target job role
        current_skills: {skill_name: current_level (0-5)}
    
    Returns:
        List of gap objects sorted by priority
    """
    required = ROLE_SKILLS.get(target_role, [])
    gaps = []

    for req in required:
        skill = req["skill"]
        target = req["target_level"]
        weight = req.get("weight", 1.0)
        current = current_skills.get(skill, 0)
        gap = max(0, target - current)

        if gap > 0:
            priority = calculate_priority(gap, weight)
            gaps.append({
                "skill_name": skill,
                "current_level": current,
                "target_level": target,
                "gap": gap,
                "priority": priority,
                "weight": weight,
                "recommended_resources": [],
                "description": SKILL_DESCRIPTIONS.get(skill, ""),
            })

    # Sort: critical > high > medium > low, then by gap size
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    gaps.sort(key=lambda x: (priority_order.get(x["priority"], 4), -x["gap"]))
    return gaps


def get_available_roles() -> List[str]:
    return list(ROLE_SKILLS.keys())


def get_role_skills(role: str) -> List[Dict]:
    return ROLE_SKILLS.get(role, [])
