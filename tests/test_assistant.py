from backend.assistant import detect_skills, quick_answer


def test_detects_skills_and_aliases():
    found = detect_skills("my skills are python,ai,ml and llm")
    assert "python" in found and "machine learning" in found and "llms" in found


def test_skill_question_gets_recommendations():
    reply = quick_answer("if my skills are python,ai,ml what are the job recommendations", {})
    assert reply and "match" in reply


def test_resume_interview_is_not_intercepted():
    assert quick_answer("build my resume", {}) is None


def test_unrelated_question_falls_through():
    assert quick_answer("tell me a joke", {}) is None


def test_uses_profile_skills_when_asked():
    reply = quick_answer("what jobs suit my skills?", {"skills": ["Python", "SQL"], "extra_skills": []})
    assert reply and "match" in reply


def test_site_help_for_skill_gap():
    assert quick_answer("what is the skill gap page?", {}) is not None
def test_new_skills_are_detected():
    found = detect_skills("I know embedded c, iot and verilog")
    assert "iot" in found and "verilog" in found