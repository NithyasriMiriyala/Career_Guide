"""scikit-learn role recommender: TF-IDF + cosine similarity blended with skill coverage.
Roles, aliases and interests come from utils/local_matcher.py (one source of truth)."""
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.local_matcher import ALIASES as _BASE_ALIASES
from utils.local_matcher import INTERESTS, ROLES

ALIASES = {**_BASE_ALIASES,
        "reactjs": "react", "react.js": "react", "dl": "deep learning",
        "rest api": "apis", "rest apis": "apis", "stats": "statistics",
        "html5": "html", "css3": "css", "artificial intelligence": "machine learning"}

GOAL_BONUS, INTEREST_BONUS, INTEREST_BONUS_MAX = 12, 4, 8


def _norm(skill: str) -> str:
    s = skill.strip().lower()
    return ALIASES.get(s, s)


def _tok(skill: str) -> str:
    return skill.replace(" ", "_")


def recommend(skills: List[str], career_goal: str = "", interests: List[str] = None) -> List[dict]:
    interests = interests or []
    pretty = {_norm(s): s.strip() for s in skills if s.strip()}
    have = set(pretty)

    names = list(ROLES)
    role_docs = [" ".join(_tok(s) for s in ROLES[n]["skills"]) for n in names]
    user_doc = " ".join(_tok(s) for s in have) or "none"

    vec = TfidfVectorizer(token_pattern=r"[^ ]+")
    matrix = vec.fit_transform(role_docs + [user_doc])
    sims = cosine_similarity(matrix[-1], matrix[:-1])[0]

    goal = (career_goal or "").lower()
    out = []
    for name, sim in zip(names, sims):
        need = ROLES[name]["skills"]
        matched = [s for s in need if s in have]
        missing = [s for s in need if s not in have]
        coverage = len(matched) / len(need)
        score = 100 * (0.6 * coverage + 0.4 * min(1.0, float(sim) * 2))
        reasons = []
        if matched:
            reasons.append(f"You know {len(matched)} of {len(need)} core skills")
        if goal and goal == name.lower():
            score += GOAL_BONUS
            reasons.append("Matches your career goal")
        hits = [i for i in interests if name in INTERESTS.get(i, [])]
        if hits:
            score += min(INTEREST_BONUS * len(hits), INTEREST_BONUS_MAX)
            reasons.append("Fits your interest in " + ", ".join(hits))
        out.append({"role": name, "description": ROLES[name]["description"],
                    "score": min(100, round(score)),
                    "matched": [pretty.get(s, s.title()) for s in matched],
                    "missing": [s.title() for s in missing],
                    "reasons": reasons})
    return sorted(out, key=lambda r: r["score"], reverse=True)