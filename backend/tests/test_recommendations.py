from backend.app.recommender.scorer import calculate_score

def test_scorer():
    score = calculate_score(1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
    assert score == 100.0
