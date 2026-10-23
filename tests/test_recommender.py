from backend.recommender import recommend


def top(skills, **kw):
    return recommend(skills, **kw)


def test_ai_skills_rank_ai_roles_first():
    names = [r["role"] for r in top(["Python", "Machine Learning", "Deep Learning", "LLMs"])[:3]]
    assert "AI Engineer" in names


def test_web_skills_rank_web_roles_first():
    names = [r["role"] for r in top(["HTML", "CSS", "JavaScript", "React"])[:2]]
    assert "Frontend Developer" in names


def test_scores_are_between_0_and_100_and_sorted():
    result = top(["Python", "SQL"])
    scores = [r["score"] for r in result]
    assert all(0 <= s <= 100 for s in scores)
    assert scores == sorted(scores, reverse=True)


def test_matched_and_missing_are_consistent():
    r = top(["Python", "SQL"])[0]
    assert r["matched"] or r["missing"]
    assert not set(m.lower() for m in r["matched"]) & set(m.lower() for m in r["missing"])


def test_aliases_are_understood():
    result = top(["ml", "Python"])
    assert any(m.lower() == "ml" or m.lower() == "machine learning"
            for r in result for m in r["matched"])


def test_career_goal_adds_bonus():
    base = {r["role"]: r["score"] for r in top(["Python"])}
    boosted = {r["role"]: r["score"] for r in top(["Python"], career_goal="Data Scientist")}
    assert boosted["Data Scientist"] >= base["Data Scientist"]


def test_interest_adds_reason():
    r = [x for x in top(["Python"], interests=["Data & Analytics"]) if x["role"] == "Data Analyst"][0]
    assert any("interest" in why.lower() for why in r["reasons"])


def test_empty_skills_does_not_crash():
    assert len(top([])) > 0