"""
Next Best Action Engine — Determines the single most impactful action for the user.
Considers: goal, progress, skill gaps, prerequisites, recent activity, deadline.
"""
from typing import Dict, List, Optional, Any


ACTION_TYPES = {
    "lesson": "Watch Lesson",
    "quiz": "Take Quiz",
    "project": "Start Project",
    "assessment": "Take Assessment",
    "review": "Review Material",
    "practice": "Practice Coding",
}


def get_next_best_action(
    profile: Dict[str, Any],
    skill_gaps: List[Dict],
    progress: Dict[str, Any],
    roadmap_phases: List[Dict],
    recent_activity: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Determine the single best next action for the user.
    
    Priority logic:
    1. If user is in the middle of something — continue it
    2. If user has a critical skill gap with prerequisites met — address it
    3. If user just completed a resource — recommend assessment
    4. If user needs to start next phase — recommend first resource
    5. Default to the most impactful gap resource
    """
    recent_activity = recent_activity or []
    
    # Check for in-progress resources first
    in_progress = [a for a in recent_activity if a.get("status") == "in_progress"]
    if in_progress:
        item = in_progress[0]
        return {
            "title": f"Continue: {item.get('title', 'Current lesson')}",
            "description": f"You're {item.get('completion_percentage', 0):.0f}% through this resource. Keep the momentum!",
            "type": "lesson",
            "resource_id": item.get("resource_id"),
            "estimated_minutes": item.get("remaining_minutes", 30),
            "reason": "You were in the middle of this resource. Consistency is key to learning.",
        }
    
    # Find the current active phase
    active_phase = None
    for phase in roadmap_phases:
        if phase.get("status") == "in_progress":
            active_phase = phase
            break
        elif phase.get("status") == "not_started":
            active_phase = phase
            break
    
    # Find critical skill gaps
    critical_gaps = [g for g in skill_gaps if g.get("priority") in ("critical", "high")]
    
    if critical_gaps and active_phase:
        top_gap = critical_gaps[0]
        skill_name = top_gap["skill_name"]
        
        # Check if this gap is in the current phase
        phase_skills = active_phase.get("skills", [])
        if skill_name in phase_skills:
            resources = active_phase.get("resources", [])
            if resources:
                resource = resources[0]
                return {
                    "title": f"Learn {skill_name}: {resource.get('title', 'Start learning')}",
                    "description": (
                        f"Your {skill_name} skill is at level {top_gap['current_level']}/5 "
                        f"but needs to reach {top_gap['target_level']}/5 for your goal. "
                        f"This resource directly addresses your highest-priority gap."
                    ),
                    "type": "lesson",
                    "resource_id": resource.get("id"),
                    "estimated_minutes": int(resource.get("duration_hours", 1) * 60),
                    "skill": skill_name,
                    "reason": (
                        f"You have a {top_gap['priority'].upper()} priority gap in {skill_name}. "
                        f"Closing this gap will unlock the next phase of your roadmap."
                    ),
                }
    
    # If no specific resource found, return phase-level recommendation
    if active_phase:
        projects = active_phase.get("projects", [])
        if projects and progress.get("phase_completion", 0) > 0.7:
            # >70% through phase — recommend the project
            project = projects[0]
            return {
                "title": f"Start Project: {project.get('title', 'Phase project')}",
                "description": (
                    "You've completed most lessons in this phase. "
                    "Now it's time to apply what you've learned with a real project!"
                ),
                "type": "project",
                "resource_id": None,
                "estimated_minutes": int(project.get("duration_hours", 8) * 60),
                "skill": "Project",
                "reason": "Projects are the best way to solidify your skills and build your portfolio.",
            }
        
        return {
            "title": f"Continue Phase {active_phase.get('phase_number', 1)}: {active_phase.get('title', 'Learning')}",
            "description": f"Focus on {', '.join(active_phase.get('skills', [])[:2])} to advance your roadmap.",
            "type": "lesson",
            "resource_id": None,
            "estimated_minutes": 45,
            "skill": active_phase.get('skills', ['Learning'])[0] if active_phase.get('skills') else 'Learning',
            "reason": f"You're in Phase {active_phase.get('phase_number', 1)}. Consistent daily practice is the fastest path to your goal.",
        }
    
    # Fallback
    return {
        "title": "Take a skill assessment",
        "description": "Assess your current skill levels to get better recommendations.",
        "type": "assessment",
        "resource_id": None,
        "estimated_minutes": 15,
        "reason": "Knowing your exact skill levels helps us personalize your roadmap.",
    }


def get_today_focus(
    profile: Dict[str, Any],
    roadmap_phases: List[Dict],
    available_hours: float = 2.0,
) -> List[Dict]:
    """
    Generate a focused list of tasks for today based on available time.
    """
    available_minutes = int(available_hours * 60)
    tasks = []
    remaining_minutes = available_minutes
    
    # Find active phase
    active_phase = None
    for phase in roadmap_phases:
        if phase.get("status") in ("in_progress", "not_started"):
            active_phase = phase
            break
    
    if not active_phase:
        return [{
            "title": "Explore available resources",
            "type": "lesson",
            "estimated_minutes": 30,
            "completed": False,
        }]
    
    resources = active_phase.get("resources", [])
    
    # Add primary learning task
    if resources and remaining_minutes >= 25:
        r = resources[0]
        task_minutes = min(remaining_minutes - 15, int(r.get("duration_hours", 1) * 60))
        tasks.append({
            "title": f"Study: {r.get('title', 'Current lesson')}",
            "type": "lesson",
            "estimated_minutes": task_minutes,
            "resource_id": r.get("id"),
            "completed": False,
        })
        remaining_minutes -= task_minutes
    
    # Add practice / quiz
    if remaining_minutes >= 15:
        tasks.append({
            "title": f"Practice: {', '.join(active_phase.get('skills', ['coding'])[:1])} exercises",
            "type": "quiz",
            "estimated_minutes": min(remaining_minutes, 20),
            "completed": False,
        })
        remaining_minutes -= 20
    
    # Add mini-project session if time allows
    if remaining_minutes >= 30 and active_phase.get("projects"):
        project = active_phase["projects"][0]
        tasks.append({
            "title": f"Work on: {project.get('title', 'Phase project')}",
            "type": "project",
            "estimated_minutes": min(remaining_minutes, 45),
            "completed": False,
        })
    
    return tasks if tasks else [{
        "title": "Review your learning roadmap",
        "type": "review",
        "estimated_minutes": 15,
        "completed": False,
    }]
