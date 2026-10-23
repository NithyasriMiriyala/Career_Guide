from utils.local_matcher import (EDUCATION_INTERESTS, INTEREST_OPTIONS, INTERESTS, ROLES,
                                interests_for, match_roles, skills_in_text)


def test_ece_gets_electronics_interests():
    opts = interests_for("B.Tech / BE - Electronics & Communication (ECE)")
    assert "Embedded Systems & IoT" in opts and "VLSI & Chip Design" in opts
    assert "Finance & Fintech" not in opts


def test_unknown_education_gets_every_interest():
    assert interests_for("something else") == INTEREST_OPTIONS


def test_every_education_interest_exists_and_points_to_real_roles():
    for edu, items in EDUCATION_INTERESTS.items():
        for i in items:
            assert i in INTERESTS, (edu, i)
    for roles in INTERESTS.values():
        assert all(r in ROLES for r in roles)


def test_ece_interest_boosts_embedded_role():
    plain = {r["role"]: r["score"] for r in match_roles(["c programming"])}
    boosted = {r["role"]: r["score"] for r in match_roles(["c programming"], interests=["Embedded Systems & IoT"])}
    assert boosted["Embedded Systems Engineer"] > plain["Embedded Systems Engineer"]


def test_skills_found_in_experience_text():
    found = skills_in_text("Built a Python API with SQL at an internship; used Git daily")
    assert {"python", "apis", "sql", "git"} <= set(found)