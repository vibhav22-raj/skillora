"""
Roadmap Generator — Creates personalized multi-phase learning roadmaps.
Dynamically generates phases based on skill gaps, timeline, and preferences.
"""
from typing import Dict, List, Optional, Any
from app.recommender.skill_gap import ROLE_SKILLS, calculate_gaps
from app.recommender.prerequisite_graph import get_learning_order


# ─── Phase Templates per Role ──────────────────────────────────────────────
ROLE_PHASE_TEMPLATES: Dict[str, List[Dict]] = {
    "AI/ML Engineer": [
        {"title": "Python & Programming Foundations", "skills": ["Python", "DSA"], "weeks_base": 4, "priority": 1},
        {"title": "Mathematics for AI", "skills": ["Statistics", "Linear Algebra"], "weeks_base": 4, "priority": 2},
        {"title": "Data Manipulation", "skills": ["NumPy/Pandas", "SQL"], "weeks_base": 3, "priority": 3},
        {"title": "Machine Learning Fundamentals", "skills": ["Machine Learning"], "weeks_base": 6, "priority": 4},
        {"title": "Deep Learning", "skills": ["Deep Learning"], "weeks_base": 6, "priority": 5},
        {"title": "ML Projects & Portfolio", "skills": ["Machine Learning", "Deep Learning"], "weeks_base": 6, "priority": 6},
        {"title": "Model Deployment & MLOps", "skills": ["Model Deployment", "Docker"], "weeks_base": 4, "priority": 7},
        {"title": "Interview Preparation", "skills": ["DSA", "System Design"], "weeks_base": 4, "priority": 8},
    ],
    "Data Scientist": [
        {"title": "Python & Programming Basics", "skills": ["Python"], "weeks_base": 3, "priority": 1},
        {"title": "SQL & Database Fundamentals", "skills": ["SQL"], "weeks_base": 3, "priority": 2},
        {"title": "Statistics & Probability", "skills": ["Statistics"], "weeks_base": 5, "priority": 3},
        {"title": "Data Manipulation & EDA", "skills": ["NumPy/Pandas", "Data Visualization"], "weeks_base": 4, "priority": 4},
        {"title": "Machine Learning", "skills": ["Machine Learning"], "weeks_base": 8, "priority": 5},
        {"title": "Data Science Projects", "skills": ["Machine Learning", "Statistics"], "weeks_base": 6, "priority": 6},
        {"title": "A/B Testing & Experimentation", "skills": ["A/B Testing"], "weeks_base": 3, "priority": 7},
        {"title": "Career & Interview Prep", "skills": [], "weeks_base": 4, "priority": 8},
    ],
    "Data Analyst": [
        {"title": "SQL Mastery", "skills": ["SQL"], "weeks_base": 5, "priority": 1},
        {"title": "Excel & Business Tools", "skills": ["Excel/Sheets"], "weeks_base": 3, "priority": 2},
        {"title": "Python for Analysis", "skills": ["Python", "NumPy/Pandas"], "weeks_base": 4, "priority": 3},
        {"title": "Data Visualization", "skills": ["Data Visualization", "Power BI/Tableau"], "weeks_base": 4, "priority": 4},
        {"title": "Statistics for Analysis", "skills": ["Statistics"], "weeks_base": 3, "priority": 5},
        {"title": "Analytics Projects", "skills": ["SQL", "Data Visualization"], "weeks_base": 4, "priority": 6},
    ],
    "Software Engineer": [
        {"title": "Programming Foundations", "skills": ["Python"], "weeks_base": 3, "priority": 1},
        {"title": "Data Structures & Algorithms", "skills": ["DSA"], "weeks_base": 8, "priority": 2},
        {"title": "Database & SQL", "skills": ["SQL"], "weeks_base": 3, "priority": 3},
        {"title": "Software Engineering Practices", "skills": ["Git", "Testing", "REST APIs"], "weeks_base": 4, "priority": 4},
        {"title": "System Design", "skills": ["System Design"], "weeks_base": 5, "priority": 5},
        {"title": "DevOps Basics", "skills": ["Docker", "Linux"], "weeks_base": 3, "priority": 6},
        {"title": "Interview Preparation", "skills": ["DSA", "System Design"], "weeks_base": 6, "priority": 7},
    ],
    "Frontend Developer": [
        {"title": "HTML & CSS Fundamentals", "skills": ["HTML/CSS"], "weeks_base": 4, "priority": 1},
        {"title": "JavaScript Mastery", "skills": ["JavaScript"], "weeks_base": 6, "priority": 2},
        {"title": "React Framework", "skills": ["React"], "weeks_base": 5, "priority": 3},
        {"title": "TypeScript & Advanced Patterns", "skills": ["TypeScript"], "weeks_base": 3, "priority": 4},
        {"title": "Performance & Testing", "skills": ["Testing", "Performance"], "weeks_base": 3, "priority": 5},
        {"title": "Projects & Portfolio", "skills": ["React", "JavaScript"], "weeks_base": 5, "priority": 6},
    ],
    "Backend Developer": [
        {"title": "Python & Programming", "skills": ["Python"], "weeks_base": 4, "priority": 1},
        {"title": "Databases & SQL", "skills": ["SQL"], "weeks_base": 4, "priority": 2},
        {"title": "REST APIs & Web Framework", "skills": ["REST APIs"], "weeks_base": 4, "priority": 3},
        {"title": "DSA & Problem Solving", "skills": ["DSA"], "weeks_base": 5, "priority": 4},
        {"title": "System Design", "skills": ["System Design"], "weeks_base": 5, "priority": 5},
        {"title": "DevOps & Deployment", "skills": ["Docker", "Linux"], "weeks_base": 4, "priority": 6},
        {"title": "Projects & Interview Prep", "skills": [], "weeks_base": 5, "priority": 7},
    ],
}

# Project recommendations per phase skill
PHASE_PROJECTS: Dict[str, str] = {
    "Python": "Build a command-line expense tracker with file persistence",
    "DSA": "Implement a custom data structure library with tests",
    "Statistics": "Analyze a real dataset and write a statistics report",
    "NumPy/Pandas": "Build a sales analytics dashboard from CSV data",
    "Machine Learning": "Customer churn prediction model with 80%+ accuracy",
    "Deep Learning": "Image classification model with transfer learning",
    "SQL": "Design and query a multi-table business database",
    "React": "Build a responsive task management application",
    "JavaScript": "Interactive quiz application with score tracking",
    "HTML/CSS": "Clone a popular website homepage (pixel-perfect)",
    "Docker": "Containerize and deploy a web application",
    "System Design": "Design a URL shortener with capacity planning",
    "REST APIs": "Build a RESTful blog API with authentication",
    "Data Visualization": "Create an interactive COVID-19 data dashboard",
    "Model Deployment": "Deploy an ML model as a REST API on the cloud",
}

MILESTONE_TEMPLATES: Dict[str, str] = {
    1: "Foundation Complete — Ready to build on core skills",
    2: "Intermediate Skills Acquired — Starting practical projects",
    3: "Core Competency Achieved — Solving real problems",
    4: "Advanced Topics Mastered — Building production-quality work",
    5: "Job Ready — Portfolio and interview preparation complete",
}


def generate_roadmap(
    target_role: str,
    skill_gaps: List[Dict],
    weekly_hours: float = 10.0,
    target_deadline_months: Optional[int] = None,
    learning_style: str = "mixed",
    current_skills: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """
    Generate a personalized learning roadmap.
    
    Args:
        target_role: Target career role
        skill_gaps: List of skill gaps from skill_gap engine
        weekly_hours: Hours available per week
        target_deadline_months: Target deadline in months (optional)
        learning_style: User's learning preference
        current_skills: Dict of {skill: level} for skipping known skills
    
    Returns:
        Complete roadmap with phases, milestones, timeline
    """
    templates = ROLE_PHASE_TEMPLATES.get(target_role, ROLE_PHASE_TEMPLATES.get("Software Engineer", []))
    current_skills = current_skills or {}
    
    # Get skills that need to be learned (gap > 0)
    gap_skill_names = {g["skill_name"] for g in skill_gaps}
    
    # Build phases — only include phases where user has gaps
    phases = []
    total_weeks = 0
    phase_num = 1
    
    for template in templates:
        phase_skills = template["skills"]
        
        # Check if any skills in this phase need work
        needs_work = any(s in gap_skill_names for s in phase_skills) or not phase_skills
        
        # Even if skills are known, include advanced phases
        if not needs_work and template["priority"] <= 3:
            # Mark as already complete
            phase = _build_phase(template, phase_num, 0, "completed", current_skills, learning_style, skill_gaps)
            phase["status"] = "completed"
            phase["weeks"] = 0  # No time needed
            phases.append(phase)
            phase_num += 1
            continue
        
        # Adjust weeks based on weekly hours (more hours = fewer weeks needed)
        base_weeks = template["weeks_base"]
        hours_factor = 10.0 / max(weekly_hours, 1.0)  # baseline is 10h/week
        adjusted_weeks = max(1, int(base_weeks * hours_factor))
        
        phase = _build_phase(template, phase_num, adjusted_weeks, "not_started", current_skills, learning_style, skill_gaps)
        phases.append(phase)
        total_weeks += adjusted_weeks
        phase_num += 1
    
    # If user has a deadline that's shorter, compress
    if target_deadline_months and total_weeks > target_deadline_months * 4:
        phases, total_weeks = _compress_roadmap(phases, target_deadline_months * 4)
    
    # Generate milestones
    milestones = _generate_milestones(phases, target_role)
    
    # Calculate estimated hours
    estimated_total_hours = total_weeks * weekly_hours
    
    return {
        "title": f"Road to {target_role}",
        "description": f"A personalized {total_weeks}-week roadmap to become a {target_role}",
        "target_role": target_role,
        "total_weeks": total_weeks,
        "estimated_total_hours": estimated_total_hours,
        "weekly_hours": weekly_hours,
        "phases": phases,
        "milestones": milestones,
        "learning_style": learning_style,
    }


def _build_phase(
    template: Dict,
    phase_num: int,
    weeks: int,
    status: str,
    current_skills: Dict[str, int],
    learning_style: str,
    skill_gaps: List[Dict],
) -> Dict[str, Any]:
    """Build a single phase dict from a template."""
    # Find relevant skill gaps for this phase
    phase_gaps = [g for g in skill_gaps if g["skill_name"] in template["skills"]]
    
    # Get project for this phase
    project = None
    for skill in template["skills"]:
        if skill in PHASE_PROJECTS:
            project = {
                "title": PHASE_PROJECTS[skill],
                "skill": skill,
                "difficulty": 3,
            }
            break
    
    # Generate resources list (placeholder — filled by recommendation engine)
    resources = []
    
    # Estimated hours = weeks * avg_weekly_hours
    estimated_hours = weeks * 10  # assume 10h/week as default
    
    return {
        "phase_number": phase_num,
        "title": template["title"],
        "description": _phase_description(template["title"], template["skills"], weeks),
        "weeks": weeks,
        "skills": template["skills"],
        "resources": resources,
        "projects": [project] if project else [],
        "milestones": [],
        "status": status,
        "estimated_hours": estimated_hours,
        "skill_gaps": [g["skill_name"] for g in phase_gaps],
    }


def _phase_description(title: str, skills: List[str], weeks: int) -> str:
    if skills:
        skills_str = ", ".join(skills[:3])
        return f"Build strong {skills_str} skills over {weeks} weeks with hands-on practice and real projects."
    return f"Advanced phase spanning {weeks} weeks with integrated projects and assessments."


def _generate_milestones(phases: List[Dict], target_role: str) -> List[Dict]:
    """Generate milestone checkpoints for the roadmap."""
    milestones = []
    cumulative_weeks = 0
    
    # Place milestones at key phase transitions
    active_phases = [p for p in phases if p["weeks"] > 0]
    
    milestone_positions = [
        len(active_phases) // 4,
        len(active_phases) // 2,
        3 * len(active_phases) // 4,
        len(active_phases) - 1,
    ]
    
    for i, phase in enumerate(active_phases):
        cumulative_weeks += phase["weeks"]
        
        if i in milestone_positions or i == len(active_phases) - 1:
            milestone_num = len(milestones) + 1
            milestones.append({
                "id": f"milestone-{milestone_num}",
                "title": f"Milestone {milestone_num}: {phase['title']} Complete",
                "description": MILESTONE_TEMPLATES.get(milestone_num, "Major milestone reached"),
                "week": cumulative_weeks,
                "skills_gained": phase["skills"],
                "phase": phase["phase_number"],
                "completion_criteria": f"Complete all resources and project in Phase {phase['phase_number']}",
            })
    
    return milestones


def _compress_roadmap(phases: List[Dict], max_weeks: int) -> tuple:
    """Compress roadmap to fit within deadline."""
    active_phases = [p for p in phases if p["weeks"] > 0]
    current_total = sum(p["weeks"] for p in active_phases)
    
    if current_total <= max_weeks:
        return phases, current_total
    
    factor = max_weeks / current_total
    new_total = 0
    
    for phase in active_phases:
        phase["weeks"] = max(1, int(phase["weeks"] * factor))
        new_total += phase["weeks"]
    
    return phases, new_total


def adapt_roadmap_for_time_change(roadmap: Dict, new_weekly_hours: float) -> Dict:
    """
    Adapt an existing roadmap when user's available time changes.
    The WOW feature: dynamically recalculate timeline.
    """
    old_weekly = roadmap.get("weekly_hours", 10)
    factor = old_weekly / max(new_weekly_hours, 1)
    
    new_total = 0
    for phase in roadmap.get("phases", []):
        if phase.get("status") == "completed":
            continue
        phase["weeks"] = max(1, int(phase["weeks"] * factor))
        new_total += phase["weeks"]
    
    roadmap["total_weeks"] = new_total
    roadmap["weekly_hours"] = new_weekly_hours
    
    return roadmap
