"""TEMPORARY role matching so the UI works before the backend exists."""

ROLES = {
    "AI Engineer": {
        "description": "Builds and ships apps powered by ML and LLMs.",
        "skills": ["python", "machine learning", "deep learning", "apis", "llms", "docker", "sql", "git"],
    },
    "Machine Learning Engineer": {
        "description": "Trains, evaluates and deploys ML models.",
        "skills": ["python", "machine learning", "statistics", "deep learning", "docker", "cloud", "sql", "git"],
    },
    "Data Analyst": {
        "description": "Turns data into insight with SQL, Excel and dashboards.",
        "skills": ["sql", "excel", "statistics", "data visualization", "python", "power bi", "communication"],
    },
    "Data Scientist": {
        "description": "Uses statistics and ML to answer business questions.",
        "skills": ["python", "statistics", "machine learning", "sql", "data visualization", "communication"],
    },
    "Backend Developer": {
        "description": "Designs APIs, services and databases.",
        "skills": ["python", "apis", "sql", "docker", "git", "cloud", "java"],
    },
    "Full-Stack Developer": {
        "description": "Builds both the user interface and the server side.",
        "skills": ["javascript", "html", "css", "react", "node.js", "apis", "sql", "git"],
    },
    "Frontend Developer": {
        "description": "Builds fast, good-looking user interfaces.",
        "skills": ["html", "css", "javascript", "react", "git", "communication"],
    },
    "Cloud / DevOps Engineer": {
        "description": "Automates infrastructure, deployment and monitoring.",
        "skills": ["cloud", "docker", "git", "python", "apis"],
    },
}

ALIASES = {
    "ai": "machine learning", "ml": "machine learning", "api": "apis",
    "llm": "llms", "js": "javascript", "node": "node.js", "nodejs": "node.js",
    "aws": "cloud", "azure": "cloud", "gcp": "cloud", "mysql": "sql",
    "postgresql": "sql", "powerbi": "power bi",
}

# Which roles each interest points towards (used for a small score boost).
INTERESTS = {
    "Artificial Intelligence": ["AI Engineer", "Machine Learning Engineer", "Data Scientist"],
    "Data & Analytics": ["Data Analyst", "Data Scientist"],
    "Web Development": ["Full-Stack Developer", "Frontend Developer", "Backend Developer"],
    "Backend & APIs": ["Backend Developer", "AI Engineer"],
    "Cloud & DevOps": ["Cloud / DevOps Engineer", "Backend Developer"],
    "Automation": ["Cloud / DevOps Engineer", "AI Engineer"],
    "Design & UI": ["Frontend Developer", "Full-Stack Developer"],
    "Research": ["Machine Learning Engineer", "Data Scientist"],
}
INTEREST_OPTIONS = list(INTERESTS)

GOAL_BONUS = 12
INTEREST_BONUS = 4
INTEREST_BONUS_MAX = 8


def normalize(skills):
    out = []
    for s in skills:
        s = ALIASES.get(s.strip().lower(), s.strip().lower())
        if s and s not in out:
            out.append(s)
    return out


def match_roles(user_skills, career_goal="", interests=None):
    """Skills listed earlier for a role count more. A career goal and interests give a small boost.
    Returns roles sorted by match %."""
    have = normalize(user_skills)
    interests = interests or []
    results = []
    for role, info in ROLES.items():
        req = info["skills"]
        weights = [len(req) - i for i in range(len(req))]
        got = sum(w for s, w in zip(req, weights) if s in have)
        score = got / sum(weights) * 100
        reasons = []
        if career_goal and career_goal == role:
            score += GOAL_BONUS
            reasons.append("🎯 Your career goal")
        liked = [i for i in interests if role in INTERESTS.get(i, [])]
        if liked:
            score += min(INTEREST_BONUS * len(liked), INTEREST_BONUS_MAX)
            reasons.append("💡 Fits your interests: " + ", ".join(liked))
        results.append({
            "role": role,
            "description": info["description"],
            "score": min(100, round(score)),
            "matched": [s for s in req if s in have],
            "missing": [s for s in req if s not in have],
            "reasons": reasons,
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results