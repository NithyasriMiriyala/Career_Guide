"""Rule-based helper that answers site questions and skill-based role questions before the RAG search."""
import re
from typing import List, Optional

from .recommender import ALIASES, ROLES, recommend

NICE = {"llms": "LLMs", "apis": "APIs", "sql": "SQL", "html": "HTML", "css": "CSS",
        "node.js": "Node.js", "power bi": "Power BI", "javascript": "JavaScript"}

VOCAB = sorted({s for r in ROLES.values() for s in r["skills"]} | set(ALIASES), key=len, reverse=True)

RECO_WORDS = re.compile(r"recommend|job|role|career|suitable|suit|fit|what can i|which|opportunit|"
                        r"work as|become|internship|opening|hire|position|apply")

SITE_HELP = [
    (r"skill gap|target level|i want to reach|completed skill|tick",
    "**Skill Gap page:** it shows each skill's current level and lets you choose a target level. "
    "Tick a skill when you've finished it and it counts toward your Home graph. "
     "Targets are saved when you press **Save profile** in 👤 Profile."),
    (r"roadmap|learning path",
    "**Learning Roadmap:** for each skill you want to improve, it shows a top-to-bottom path from your "
    "current level to your target, with topics, YouTube channels, certifications and project ideas. "
    "Change a target on the Skill Gap page to get a new roadmap."),
    (r"resume builder|ats score|download.*(pdf|word|resume)|generate resume",
    "**Resume Builder:** fill in the form (name, email, phone, skills, education, and experience or projects), "
     "then press **Generate resume & ATS score**. You get a score out of 100 with tips, plus PDF, Word and text downloads. "
    "The form must be filled in before a score appears."),
    (r"i applied|applied graph|jobs applied|graph|home page",
     "**Home graph:** it counts the jobs you mark with **I applied ✅** on the Recommendations page and the skills "
    "you tick on the Skill Gap page, month by month."),
    (r"apply button|apply link|where.*apply|job link|jobs and internships|internship",
     "**Applying:** on **💼 Recommendations**, pick a role, location and Jobs or Internships. Each portal card "
    "(LinkedIn, Indeed, Naukri, Wellfound, Internshala and more) opens a ready search in a new tab. Apply there, "
     "then press **I applied ✅** so your progress is tracked."),
    (r"profile|date of birth|dob|interests|career goal|education",
     "**Profile:** open **👤 Profile** (top right) to set your name, date of birth, graduation year, education, "
     "interests, career goal, skills and a level for each skill. Press **Save profile** so recommendations use it."),
    (r"log ?out|log ?in|sign ?in|password|email login",
     "**Login:** you sign in with just your email, with no password. Use **🚪 Log out** (top right) to leave. "
    "Using the same email brings back your saved data."),
    (r"slow|loading|not loading|backend|server|wake|error|not reachable",
    "**Slow or an error?** The server is on a free plan and sleeps when idle, so the first request after a quiet "
    "period can take about a minute. Wait a moment and try again."),
]


def _nice(skill: str) -> str:
    s = skill.lower()
    return NICE.get(s, s.title())


def detect_skills(text: str) -> List[str]:
    t = text.lower()
    found = []
    for term in VOCAB:
        if re.search(r"(?<![a-z0-9.+#])" + re.escape(term) + r"(?![a-z0-9+#])", t):
            canon = ALIASES.get(term, term)
            if canon not in found:
                found.append(canon)
    return found


def _reco_reply(skills: List[str]) -> str:
    names = [_nice(s) for s in skills]
    roles = recommend(names)[:3]
    out = [f"Based on **{', '.join(names)}**, these roles fit you best:", ""]
    for i, r in enumerate(roles, 1):
        line = f"{i}. **{r['role']}** - {r['score']}% match"
        if r["matched"]:
            line += f" (you have: {', '.join(r['matched'])})"
        out.append(line)
        if r["missing"]:
            out.append(f"   - To level up, learn: {', '.join(_nice(m) for m in r['missing'][:4])}")
    out += ["", "Next steps: open **💼 Recommendations** for job and internship links, **🧩 Skill Gap** "
            "to set targets, and **🗺️ Learning Roadmap** for what to study. Save your skills in "
            "**👤 Profile** to personalise everything."]
    return "\n".join(out)


def quick_answer(message: str, profile: Optional[dict] = None) -> Optional[str]:
    """Return a ready answer, or None to let the knowledge-base search handle it."""
    m = (message or "").lower().strip()
    if not m or "build my resume" in m or "resume interview" in m:
        return None  # keep the existing resume interview flow

    # 1. Role recommendations from skills in the message (or from the saved profile)
    if RECO_WORDS.search(m):
        skills = detect_skills(m)
        if not skills and re.search(r"my skills|my profile|based on my", m) and profile:
            skills = [s for s in (profile.get("skills", []) + profile.get("extra_skills", [])) if s]
        if skills:
            return _reco_reply(skills)

    # 2. Questions about using the website
    for pattern, answer in SITE_HELP:
        if re.search(pattern, m):
            return answer
    return None