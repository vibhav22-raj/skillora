"""Assessment API routes — assessments, submissions, results."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime

from backend.app.database.base import get_db
from backend.app.models import User, Assessment, AssessmentAttempt
from backend.app.schemas import ApiResponse, AssessmentSubmit
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/assessments", tags=["assessments"])


@router.get("/", response_model=ApiResponse)
async def get_assessments(db: AsyncSession = Depends(get_db)):
    """Get all available assessments."""
    result = await db.execute(select(Assessment))
    assessments = result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "id": a.id,
                "skill_name": a.skill_name,
                "title": a.title,
                "question_count": len(a.questions),
                "passing_score": a.passing_score,
                "estimated_minutes": a.estimated_minutes,
            }
            for a in assessments
        ],
    )


@router.get("/{assessment_id}", response_model=ApiResponse)
async def get_assessment(assessment_id: str, db: AsyncSession = Depends(get_db)):
    """Get assessment with questions (without correct answers)."""
    result = await db.execute(select(Assessment).where(Assessment.id == assessment_id))
    assessment = result.scalar_one_or_none()

    if not assessment:
        return ApiResponse(success=False, message="Assessment not found")

    # Strip correct answers before sending to client
    safe_questions = []
    for q in assessment.questions:
        safe_q = {k: v for k, v in q.items() if k != "correct_answer"}
        safe_questions.append(safe_q)

    return ApiResponse(
        success=True,
        data={
            "id": assessment.id,
            "skill_name": assessment.skill_name,
            "title": assessment.title,
            "questions": safe_questions,
            "passing_score": assessment.passing_score,
            "estimated_minutes": assessment.estimated_minutes,
        },
    )


@router.post("/{assessment_id}/submit", response_model=ApiResponse)
async def submit_assessment(
    assessment_id: str,
    submission: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit assessment answers and get scored result."""
    result = await db.execute(select(Assessment).where(Assessment.id == assessment_id))
    assessment = result.scalar_one_or_none()

    if not assessment:
        return ApiResponse(success=False, message="Assessment not found")

    # Score the submission
    questions = assessment.questions
    total = len(questions)
    correct = 0

    for question in questions:
        q_id = question["id"]
        if str(submission.answers.get(q_id)) == str(question.get("correct_answer")):
            correct += 1

    score = (correct / total) * 100 if total > 0 else 0
    passed = score >= assessment.passing_score
    skill_estimate = min(5, int(score / 20))  # 0-5 scale

    # Generate feedback
    if score >= 85:
        feedback = f"Excellent! Score: {score:.0f}%. You have a strong grasp of {assessment.skill_name}. Ready to advance!"
    elif score >= 70:
        feedback = f"Good job! Score: {score:.0f}%. You passed. Review the questions you missed and continue to the next topic."
    elif score >= 50:
        feedback = f"Score: {score:.0f}%. You're getting there! Focus on the areas where you got stuck. A quick review before retaking would help."
    else:
        feedback = f"Score: {score:.0f}%. It looks like more foundational work is needed. I've added prerequisite resources to your roadmap."

    recommendations = []
    if not passed:
        recommendations.append(f"Review {assessment.skill_name} fundamentals before retaking")
        recommendations.append("Check the prerequisite resources in your roadmap")

    # Save attempt
    attempt = AssessmentAttempt(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        assessment_id=assessment_id,
        answers=submission.answers,
        score=score,
        passed=passed,
        completed_at=datetime.utcnow(),
        skill_estimate=float(skill_estimate),
        feedback=feedback,
    )
    db.add(attempt)
    await db.commit()

    return ApiResponse(
        success=True,
        data={
            "score": round(score, 1),
            "passed": passed,
            "total_questions": total,
            "correct_answers": correct,
            "skill_estimate": skill_estimate,
            "feedback": feedback,
            "recommendations": recommendations,
        },
        message="Assessment completed!",
    )


@router.get("/results/my", response_model=ApiResponse)
async def get_my_results(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all assessment results for current user."""
    result = await db.execute(
        select(AssessmentAttempt)
        .where(AssessmentAttempt.user_id == current_user.id)
        .order_by(AssessmentAttempt.completed_at.desc())
    )
    attempts = result.scalars().all()

    return ApiResponse(
        success=True,
        data=[
            {
                "id": a.id,
                "assessment_id": a.assessment_id,
                "score": a.score,
                "passed": a.passed,
                "skill_estimate": a.skill_estimate,
                "feedback": a.feedback,
                "completed_at": a.completed_at.isoformat(),
            }
            for a in attempts
        ],
    )
