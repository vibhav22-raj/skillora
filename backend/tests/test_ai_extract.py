import asyncio
from app.ai.demo_provider import DemoProvider


def test_demo_extract_profile_basic():
    demo = DemoProvider()
    text = "I want to become a Data Scientist. I'm a beginner and I can study 10 hours a week. I know basic Python and SQL."
    result = asyncio.get_event_loop().run_until_complete(demo.extract_profile(text))
    assert isinstance(result, dict)
    assert 'target_role' in result
    assert result['target_role'] in [
        'AI/ML Engineer', 'Data Scientist', 'Data Analyst', 'Software Engineer',
        'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
        'Cloud Engineer', 'DevOps Engineer', 'Cybersecurity Analyst'
    ]
    assert 'experience_level' in result
    assert 'weekly_hours' in result
    assert 'current_skills' in result
    assert isinstance(result['current_skills'], dict)
