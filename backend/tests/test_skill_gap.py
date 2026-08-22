from backend.app.recommender.skill_gap import calculate_gaps

def test_skill_gaps():
    gaps = calculate_gaps('AI/ML Engineer', {'Python': 2})
    assert len(gaps) > 0
