"""scikit-learn role recommender: TF-IDF + cosine similarity blended with skill coverage."""
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROLES: Dict[str, dict] = {
    "AI Engineer": {"description": "Build products powered by LLMs and machine learning.",
                    "skills": ["python", "machine learning", "deep learning", "llms", "apis", "docker"]},
    "Machine Learning Engineer": {"description": "Train, evaluate and deploy ML models.",
                    "skills": ["python", "machine learning", "statistics", "sql", "docker", "git"]},
    "Data Scientist": {"description": "Find insights and build predictive models from data.",
                    "skills": ["python", "statistics", "machine learning", "sql", "data visualization"]},
    "Data Analyst": {"description": "Turn data into reports and dashboards.",
                    "skills": ["sql", "excel", "power bi", "data visualization", "statistics", "python"]},
    "Frontend Developer": {"description": "Build the interface users see and use.",
                    "skills": ["html", "css", "javascript", "react", "git"]},
    "Backend Developer": {"description": "Build servers, APIs and databases.",
                    "skills": ["python", "node.js", "java", "sql", "apis", "docker", "git"]},
    "Full Stack Developer": {"description": "Work on both the interface and the server.",
                    "skills": ["html", "css", "javascript", "react", "node.js", "sql", "apis", "git"]},
    "DevOps / Cloud Engineer": {"description": "Automate deployment and run apps in the cloud.",
                    "skills": ["cloud", "docker", "git", "python", "apis"]},
    "UI/UX Designer": {"description": "Design clear, friendly interfaces.",
                    "skills": ["html", "css", "communication", "data visualization"]},
}

INTERESTS = {
    "Artificial Intelligence": ["AI Engineer", "Machine Learning Engineer", "Data Scientist"],
    "Data & Analytics": ["Data Analyst", "Data Scientist"],
    "Web Development": ["Frontend Developer", "Full Stack Developer", "Backend Developer"],
    "Backend & APIs": ["Backend Developer", "Full Stack Developer"],
    "Cloud & DevOps": ["DevOps / Cloud Engineer"],
    "Automation": ["DevOps / Cloud Engineer", "Backend Developer"],
    "Design & UI": ["UI/UX Designer", "Frontend Developer"],
    "Research": ["Data Scientist", "Machine Learning Engineer"],
}

ALIASES = {"js": "javascript", "reactjs": "react", "react.js": "react", "node": "node.js",
        "nodejs": "node.js", "ml": "machine learning", "dl": "deep learning",
        "llm": "llms", "api": "apis", "rest api": "apis", "rest apis": "apis",
        "powerbi": "power bi", "aws": "cloud", "azure": "cloud", "gcp": "cloud",
        "stats": "statistics", "html5": "html", "css3": "css"}

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
    boosted = {r for i in interests for r in INTERESTS.get(i, [])}
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
        if goal and (name.lower() in goal or goal in name.lower()):
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