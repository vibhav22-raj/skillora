"""
Recommendation Scorer — Weighted multi-factor scoring for learning resources.

Score = (
    goal_relevance       * 0.25 +
    skill_gap_relevance  * 0.25 +
    prerequisite_fit     * 0.20 +
    difficulty_fit       * 0.15 +
    time_fit             * 0.10 +
    preference_fit       * 0.05
) * 100
"""
from typing import Dict, List, Optional, Any
try:
    from backend.app.recommender.prerequisite_graph import check_prerequisite_fit
    from backend.app.recommender.skill_gap import ROLE_SKILLS
except ImportError:
    from app.recommender.prerequisite_graph import check_prerequisite_fit
    from app.recommender.skill_gap import ROLE_SKILLS


# ─── Scoring Weights ───────────────────────────────────────────────────────
DEFAULT_WEIGHTS = {
    "goal_relevance": 0.25,
    "skill_gap_relevance": 0.25,
    "prerequisite_fit": 0.20,
    "difficulty_fit": 0.15,
    "time_fit": 0.10,
    "preference_fit": 0.05,
}

# Format preferences mapping
FORMAT_STYLE_MAP = {
    "video": ["video"],
    "reading": ["article", "book"],
    "coding": ["interactive", "coding"],
    "projects": ["project"],
    "mixed": ["video", "article", "interactive", "course"],
}


def calculate_goal_relevance(
    resource_skills: List[str],
    role_skills: List[Dict],
) -> float:
    """
    How relevant is this resource to the user's target role?
    Based on overlap between resource skills and role-required skills.
    """
    if not resource_skills or not role_skills:
        return 0.3  # default relevance

    role_skill_names = {rs["skill"].lower() for rs in role_skills}
    resource_skill_lower = {s.lower() for s in resource_skills}
    overlap = role_skill_names.intersection(resource_skill_lower)

    if not overlap:
        return 0.1
    
    # Weight by importance
    total_weight = sum(rs["weight"] for rs in role_skills if rs["skill"].lower() in resource_skill_lower)
    max_weight = sum(rs["weight"] for rs in role_skills)
    
    return min(1.0, total_weight / max_weight) if max_weight > 0 else 0.0


def calculate_skill_gap_relevance(
    resource_skills: List[str],
    skill_gaps: List[Dict],
) -> float:
    """
    How well does this resource address the user's highest-priority skill gaps?
    """
    if not resource_skills or not skill_gaps:
        return 0.3

    # Assign gap scores: critical=4, high=3, medium=2, low=1
    priority_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    
    resource_lower = {s.lower() for s in resource_skills}
    total_gap_score = 0.0
    matched_gap_score = 0.0

    for gap in skill_gaps:
        gap_score = priority_scores.get(gap["priority"], 1) * gap["gap"]
        total_gap_score += gap_score
        if gap["skill_name"].lower() in resource_lower:
            matched_gap_score += gap_score

    if total_gap_score == 0:
        return 0.0

    return min(1.0, matched_gap_score / total_gap_score)


def calculate_prerequisite_fit(
    user_skill_names: List[str],
    resource_prerequisites: List[str],
) -> float:
    """How well does user meet prerequisites for this resource?"""
    return check_prerequisite_fit(user_skill_names, resource_prerequisites)


def calculate_difficulty_fit(
    resource_difficulty: int,
    user_experience_level: str,
    user_skill_level: float = 2.5,
) -> float:
    """
    How well does resource difficulty match user's current level?
    Slightly above user level is ideal (zone of proximal development).
    """
    # Map experience to target difficulty
    level_map = {
        "beginner": 1.5,
        "intermediate": 2.5,
        "advanced": 4.0,
    }
    target_diff = level_map.get(user_experience_level, 2.5)
    
    # Optimal is resource_difficulty == target_diff + 0.5
    ideal = target_diff + 0.5
    distance = abs(resource_difficulty - ideal)
    
    # Penalty for too easy or too hard
    if distance == 0:
        return 1.0
    elif distance <= 1:
        return 0.8
    elif distance <= 2:
        return 0.5
    else:
        return 0.2


def calculate_time_fit(
    resource_duration_hours: float,
    weekly_hours: float,
    preferred_duration: str = "medium",
) -> float:
    """
    How well does resource duration fit user's available time and preferences?
    """
    duration_prefs = {
        "short": (0, 5),      # 0-5 hours
        "medium": (2, 20),    # 2-20 hours
        "long": (10, 100),    # 10+ hours
    }
    
    min_h, max_h = duration_prefs.get(preferred_duration, (2, 20))
    
    if min_h <= resource_duration_hours <= max_h:
        return 1.0
    elif resource_duration_hours < min_h:
        # Too short — penalty proportional to shortfall
        return max(0.4, resource_duration_hours / min_h)
    else:
        # Too long — penalty
        return max(0.3, max_h / resource_duration_hours)


def calculate_preference_fit(
    resource_format: Optional[str],
    learning_style: str,
) -> float:
    """How well does resource format match user's learning style preference?"""
    if not resource_format:
        return 0.5
    
    preferred_formats = FORMAT_STYLE_MAP.get(learning_style, [])
    if not preferred_formats or learning_style == "mixed":
        return 0.8  # mixed accepts all
    
    if resource_format.lower() in preferred_formats:
        return 1.0
    elif resource_format == "course":
        return 0.7  # courses are generally always relevant
    return 0.3


def calculate_total_score(
    goal_relevance: float,
    skill_gap_relevance: float,
    prerequisite_fit: float,
    difficulty_fit: float,
    time_fit: float,
    preference_fit: float,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """Calculate final recommendation score (0-100)."""
    w = weights or DEFAULT_WEIGHTS
    score = (
        goal_relevance      * w["goal_relevance"] +
        skill_gap_relevance * w["skill_gap_relevance"] +
        prerequisite_fit    * w["prerequisite_fit"] +
        difficulty_fit      * w["difficulty_fit"] +
        time_fit            * w["time_fit"] +
        preference_fit      * w["preference_fit"]
    ) * 100
    return round(min(100.0, max(0.0, score)), 2)


def calculate_score(
    goal_relevance: float,
    skill_gap_relevance: float,
    prerequisite_fit: float,
    difficulty_fit: float,
    time_fit: float,
    preference_fit: float,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """Backward-compatible alias for the legacy scorer API."""
    return calculate_total_score(
        goal_relevance,
        skill_gap_relevance,
        prerequisite_fit,
        difficulty_fit,
        time_fit,
        preference_fit,
        weights,
    )


def score_resource(
    resource: Dict[str, Any],
    profile: Dict[str, Any],
    skill_gaps: List[Dict],
    user_skill_names: List[str],
) -> Dict[str, Any]:
    """
    Score a single resource against user's profile.
    Returns score breakdown dict.
    """
    target_role = profile.get("target_role", "")
    role_skills = ROLE_SKILLS.get(target_role, [])
    
    goal_rel = calculate_goal_relevance(resource.get("skills", []), role_skills)
    gap_rel = calculate_skill_gap_relevance(resource.get("skills", []), skill_gaps)
    prereq_fit = calculate_prerequisite_fit(user_skill_names, resource.get("prerequisites", []))
    diff_fit = calculate_difficulty_fit(
        resource.get("difficulty", 1),
        profile.get("experience_level", "intermediate"),
    )
    time_fit = calculate_time_fit(
        resource.get("duration_hours", 5),
        profile.get("weekly_hours", 10),
        profile.get("preferred_duration", "medium"),
    )
    pref_fit = calculate_preference_fit(
        resource.get("format"),
        profile.get("learning_style", "mixed"),
    )
    
    total = calculate_total_score(goal_rel, gap_rel, prereq_fit, diff_fit, time_fit, pref_fit)
    
    return {
        "score": total,
        "goal_relevance": round(goal_rel, 3),
        "skill_gap_relevance": round(gap_rel, 3),
        "prerequisite_fit": round(prereq_fit, 3),
        "difficulty_fit": round(diff_fit, 3),
        "time_fit": round(time_fit, 3),
        "preference_fit": round(pref_fit, 3),
    }
