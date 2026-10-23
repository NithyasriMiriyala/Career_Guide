"""Role data and rule-based matching (also the single source of roles for the backend recommender)."""
import re

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
    "Embedded Systems Engineer": {
        "description": "Writes software that runs inside electronic devices.",
        "skills": ["c programming", "embedded systems", "microcontrollers", "c++", "iot", "git"],
    },
    "IoT Engineer": {
        "description": "Connects sensors and devices to apps and the cloud.",
        "skills": ["iot", "microcontrollers", "c programming", "python", "cloud", "apis"],
    },
    "VLSI / Hardware Engineer": {
        "description": "Designs and verifies digital chips and circuits.",
        "skills": ["verilog", "embedded systems", "c programming", "matlab", "signal processing"],
    },
    "Network / Telecom Engineer": {
        "description": "Builds and maintains communication and data networks.",
        "skills": ["networking", "signal processing", "python", "cloud", "apis"],
    },
    "Robotics / Automation Engineer": {
        "description": "Builds machines and systems that work automatically.",
        "skills": ["python", "c++", "matlab", "microcontrollers", "iot"],
    },
    "Mechanical Design Engineer": {
        "description": "Designs parts and products using CAD and analysis.",
        "skills": ["cad", "matlab", "excel", "communication"],
    },
    "Business Analyst": {
        "description": "Connects business needs with data and solutions.",
        "skills": ["excel", "sql", "power bi", "communication", "data visualization", "statistics"],
    },
}

ALIASES = {
    "ai": "machine learning", "ml": "machine learning", "api": "apis",
    "llm": "llms", "js": "javascript", "node": "node.js", "nodejs": "node.js",
    "aws": "cloud", "azure": "cloud", "gcp": "cloud", "mysql": "sql",
    "postgresql": "sql", "powerbi": "power bi", "c": "c programming",
    "embedded c": "c programming", "embedded": "embedded systems",
    "autocad": "cad", "solidworks": "cad", "vlsi": "verilog",
}

# Which roles each interest points towards (used for a small score boost).
INTERESTS = {
    "Artificial Intelligence": ["AI Engineer", "Machine Learning Engineer", "Data Scientist"],
    "Data & Analytics": ["Data Analyst", "Data Scientist"],
    "Web Development": ["Full-Stack Developer", "Frontend Developer", "Backend Developer"],
    "Backend & APIs": ["Backend Developer", "AI Engineer"],
    "Cloud & DevOps": ["Cloud / DevOps Engineer", "Backend Developer"],
    "Automation": ["Cloud / DevOps Engineer", "AI Engineer", "Robotics / Automation Engineer"],
    "Design & UI": ["Frontend Developer", "Full-Stack Developer"],
    "Research": ["Machine Learning Engineer", "Data Scientist"],
    "Embedded Systems & IoT": ["Embedded Systems Engineer", "IoT Engineer"],
    "VLSI & Chip Design": ["VLSI / Hardware Engineer", "Embedded Systems Engineer"],
    "Telecom & Networking": ["Network / Telecom Engineer", "Cloud / DevOps Engineer"],
    "Signal & Image Processing": ["Machine Learning Engineer", "Network / Telecom Engineer"],
    "Robotics & Automation": ["Robotics / Automation Engineer", "IoT Engineer"],
    "CAD & Product Design": ["Mechanical Design Engineer", "Robotics / Automation Engineer"],
    "Manufacturing & Industry 4.0": ["Mechanical Design Engineer", "Robotics / Automation Engineer"],
    "Business Analytics": ["Business Analyst", "Data Analyst"],
    "Finance & Fintech": ["Business Analyst", "Data Analyst"],
    "Marketing Analytics": ["Business Analyst", "Data Analyst"],
    "Product & Strategy": ["Business Analyst"],
}
INTEREST_OPTIONS = list(INTERESTS)

# Education choice -> interests that make sense for it.
EDUCATION_INTERESTS = {
    "B.Tech / BE - Computer Science / IT": [
        "Artificial Intelligence", "Data & Analytics", "Web Development", "Backend & APIs",
        "Cloud & DevOps", "Automation", "Research"],
    "B.Tech / BE - AI & Data Science": [
        "Artificial Intelligence", "Data & Analytics", "Research", "Backend & APIs", "Automation"],
    "B.Tech / BE - Electronics & Communication (ECE)": [
        "Embedded Systems & IoT", "VLSI & Chip Design", "Telecom & Networking",
        "Signal & Image Processing", "Robotics & Automation", "Artificial Intelligence", "Data & Analytics"],
    "B.Tech / BE - Electrical & Electronics (EEE)": [
        "Embedded Systems & IoT", "Robotics & Automation", "Automation", "VLSI & Chip Design",
        "Data & Analytics"],
    "B.Tech / BE - Mechanical": [
        "CAD & Product Design", "Robotics & Automation", "Manufacturing & Industry 4.0",
        "Automation", "Data & Analytics"],
    "B.Tech / BE - Civil": [
        "CAD & Product Design", "Manufacturing & Industry 4.0", "Data & Analytics", "Automation"],
    "BCA / MCA": [
        "Web Development", "Backend & APIs", "Cloud & DevOps", "Data & Analytics",
        "Artificial Intelligence", "Design & UI"],
    "B.Sc / M.Sc (Maths, Stats, Physics, etc.)": [
        "Data & Analytics", "Artificial Intelligence", "Research", "Business Analytics"],
    "BBA / MBA / B.Com": [
        "Business Analytics", "Finance & Fintech", "Marketing Analytics", "Product & Strategy",
        "Data & Analytics"],
    "Design (B.Des / Arts)": [
        "Design & UI", "Web Development", "Product & Strategy", "Marketing Analytics"],
    "Other": INTEREST_OPTIONS,
}
EDUCATION_OPTIONS = list(EDUCATION_INTERESTS)
EXPERIENCE_LEVELS = ["Student / Fresher", "Internship experience", "0-2 years", "2-5 years", "5+ years"]


def interests_for(education: str) -> list:
    """Interest choices that fit the chosen education (all of them if it is unknown)."""
    return list(EDUCATION_INTERESTS.get(education, INTEREST_OPTIONS))


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


_VOCAB = sorted({s for r in ROLES.values() for s in r["skills"]} | set(ALIASES), key=len, reverse=True)


def skills_in_text(text: str) -> list:
    """Skills mentioned in free text (for example the Experience box), as lower-case names."""
    t = (text or "").lower()
    found = []
    for term in _VOCAB:
        if term == "c":  # a single letter is too easy to match by accident
            continue
        if re.search(r"(?<![a-z0-9.+#])" + re.escape(term) + r"(?![a-z0-9+#])", t):
            canon = ALIASES.get(term, term)
            if canon not in found:
                found.append(canon)
    return found


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