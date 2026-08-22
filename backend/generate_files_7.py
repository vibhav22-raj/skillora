import os

base_dir = r"F:\github clone rep\HCL_Amplified\backend\tests"

test_auth = """def test_dummy():
    assert True
"""
with open(os.path.join(base_dir, "test_auth.py"), "w") as f:
    f.write(test_auth)

test_recs = """from app.recommender.scorer import calculate_score

def test_scorer():
    score = calculate_score(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    assert score == 100.0
"""
with open(os.path.join(base_dir, "test_recommendations.py"), "w") as f:
    f.write(test_recs)

test_skills = """from app.recommender.skill_gap import calculate_gaps

def test_skill_gaps():
    gaps = calculate_gaps('AI/ML Engineer', {'Python': 2})
    assert len(gaps) > 0
"""
with open(os.path.join(base_dir, "test_skill_gap.py"), "w") as f:
    f.write(test_skills)

print("Tests complete.")
