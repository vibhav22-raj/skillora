"""
Backend tests for LearnPath AI.
Tests: auth, recommendation scoring, skill gap engine.
"""
import pytest
import asyncio
from backend.app.recommender.scorer import (
    calculate_goal_relevance,
    calculate_skill_gap_relevance,
    calculate_prerequisite_fit,
    calculate_difficulty_fit,
    calculate_time_fit,
    calculate_preference_fit,
    calculate_total_score,
    score_resource,
)
from backend.app.recommender.skill_gap import calculate_gaps, ROLE_SKILLS
from backend.app.recommender.prerequisite_graph import (
    get_prerequisites,
    get_learning_order,
    check_prerequisite_fit,
)
from backend.app.recommender.roadmap_generator import generate_roadmap
from backend.app.services.auth_service import get_password_hash, verify_password, create_access_token, decode_token


# ─── Auth Tests ────────────────────────────────────────────────────────────
class TestAuth:
    def test_password_hashing(self):
        password = "TestPassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed)

    def test_wrong_password_fails(self):
        hashed = get_password_hash("correct-password")
        assert not verify_password("wrong-password", hashed)

    def test_jwt_token_creation(self):
        token = create_access_token({"sub": "user-123"})
        assert token is not None
        payload = decode_token(token)
        assert payload["sub"] == "user-123"

    def test_invalid_token_fails(self):
        result = decode_token("invalid.token.here")
        assert result is None


# ─── Skill Gap Tests ────────────────────────────────────────────────────────
class TestSkillGap:
    def test_no_gaps_when_skilled(self):
        """User who knows everything has no gaps."""
        current_skills = {
            "Python": 4, "Statistics": 4, "Linear Algebra": 3,
            "Machine Learning": 5, "Deep Learning": 4, "NumPy/Pandas": 4,
            "SQL": 3, "Model Deployment": 3, "Git": 3, "DSA": 3, "Docker": 2,
        }
        gaps = calculate_gaps("AI/ML Engineer", current_skills)
        assert len(gaps) == 0

    def test_complete_gaps_for_beginner(self):
        """Complete beginner has gaps for all skills."""
        gaps = calculate_gaps("AI/ML Engineer", {})
        assert len(gaps) > 0
        for gap in gaps:
            assert gap["current_level"] == 0
            assert gap["gap"] > 0

    def test_priority_ordering(self):
        """Critical gaps should come before low priority."""
        gaps = calculate_gaps("AI/ML Engineer", {"Python": 3, "Git": 2})
        priorities = [g["priority"] for g in gaps]
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        ordered = sorted(priorities, key=lambda x: priority_order.get(x, 4))
        assert priorities == ordered

    def test_partial_skills(self):
        """Partial skill knowledge reduces gap correctly."""
        gaps = calculate_gaps("AI/ML Engineer", {"Python": 3})
        python_gap = next((g for g in gaps if g["skill_name"] == "Python"), None)
        if python_gap:
            assert python_gap["current_level"] == 3
            assert python_gap["gap"] == 1  # target is 4

    def test_available_roles(self):
        """All expected roles exist in ROLE_SKILLS."""
        expected = ["AI/ML Engineer", "Data Scientist", "Frontend Developer", "Backend Developer"]
        for role in expected:
            assert role in ROLE_SKILLS


# ─── Recommendation Scorer Tests ───────────────────────────────────────────
class TestScorer:
    def test_score_range(self):
        """Score must always be 0-100."""
        score = calculate_total_score(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        assert 0 <= score <= 100

    def test_perfect_score(self):
        """Perfect match gives ~100."""
        score = calculate_total_score(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
        assert score == 100.0

    def test_zero_score(self):
        """Zero match gives 0."""
        score = calculate_total_score(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        assert score == 0.0

    def test_goal_relevance_no_overlap(self):
        """No overlap between resource skills and role skills gives low relevance."""
        resource_skills = ["Haskell", "COBOL"]
        role_skills = [{"skill": "Python", "target_level": 4, "weight": 1.0}]
        relevance = calculate_goal_relevance(resource_skills, role_skills)
        assert relevance < 0.3

    def test_prerequisite_fit_all_met(self):
        """All prerequisites met gives 1.0."""
        fit = calculate_prerequisite_fit(["Python", "Statistics"], ["Python", "Statistics"])
        assert fit == 1.0

    def test_prerequisite_fit_none_met(self):
        """No prerequisites met gives 0.0."""
        fit = calculate_prerequisite_fit([], ["Python", "Statistics"])
        assert fit == 0.0

    def test_difficulty_fit_exact_match(self):
        """Difficulty slightly above user level is ideal."""
        # Intermediate user (target ~3), difficulty 3 is ideal
        fit = calculate_difficulty_fit(3, "intermediate")
        assert fit >= 0.7

    def test_preference_fit_mixed_accepts_all(self):
        """Mixed learning style accepts all formats."""
        fit = calculate_preference_fit("video", "mixed")
        assert fit >= 0.5

    def test_score_resource_returns_all_components(self):
        """score_resource returns all scoring components."""
        resource = {
            "skills": ["Python"], "difficulty": 2, "duration_hours": 10,
            "format": "video", "prerequisites": [],
        }
        profile = {
            "target_role": "AI/ML Engineer", "experience_level": "intermediate",
            "weekly_hours": 10, "learning_style": "mixed", "preferred_duration": "medium",
        }
        skill_gaps = [{"skill_name": "Python", "gap": 1, "priority": "medium", "current_level": 3, "target_level": 4}]
        result = score_resource(resource, profile, skill_gaps, ["Python"])
        
        assert "score" in result
        assert "goal_relevance" in result
        assert "skill_gap_relevance" in result
        assert "prerequisite_fit" in result
        assert "difficulty_fit" in result
        assert "time_fit" in result
        assert "preference_fit" in result
        assert 0 <= result["score"] <= 100


# ─── Prerequisite Graph Tests ─────────────────────────────────────────────
class TestPrerequisiteGraph:
    def test_prerequisites_of_ml(self):
        """Machine Learning requires Python, Statistics, Linear Algebra."""
        prereqs = get_prerequisites("Machine Learning")
        assert "Python" in prereqs
        assert "Statistics" in prereqs
        assert "Linear Algebra" in prereqs

    def test_no_prerequisites_for_python(self):
        """Python has no prerequisites."""
        prereqs = get_prerequisites("Python")
        assert len(prereqs) == 0

    def test_topological_order(self):
        """Python comes before Machine Learning in learning order."""
        order = get_learning_order(["Machine Learning", "Python"])
        assert order.index("Python") < order.index("Machine Learning")

    def test_prerequisite_fit_partial(self):
        """Partial prerequisites gives 0.5."""
        fit = check_prerequisite_fit(["Python"], ["Python", "Statistics"])
        assert fit == 0.5


# ─── Roadmap Generator Tests ──────────────────────────────────────────────
class TestRoadmapGenerator:
    def test_roadmap_generated(self):
        """Roadmap generator returns valid structure."""
        gaps = calculate_gaps("AI/ML Engineer", {"Python": 3})
        roadmap = generate_roadmap("AI/ML Engineer", gaps, weekly_hours=10)
        
        assert "phases" in roadmap
        assert "milestones" in roadmap
        assert "total_weeks" in roadmap
        assert len(roadmap["phases"]) > 0

    def test_roadmap_skips_known_skills(self):
        """User who knows Python gets Python phase marked complete."""
        current_skills = {"Python": 4, "DSA": 3}
        gaps = calculate_gaps("AI/ML Engineer", current_skills)
        roadmap = generate_roadmap("AI/ML Engineer", gaps, current_skills=current_skills)
        
        # First phase (Python/DSA) should be completed since user knows it
        first_phase = roadmap["phases"][0]
        assert first_phase.get("status") == "completed" or first_phase["weeks"] == 0

    def test_roadmap_adjusts_for_more_hours(self):
        """More hours per week = fewer weeks needed."""
        gaps = calculate_gaps("AI/ML Engineer", {})
        roadmap_slow = generate_roadmap("AI/ML Engineer", gaps, weekly_hours=5)
        roadmap_fast = generate_roadmap("AI/ML Engineer", gaps, weekly_hours=20)
        assert roadmap_fast["total_weeks"] < roadmap_slow["total_weeks"]
