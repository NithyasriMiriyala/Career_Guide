"""Builds an ATS-friendly plain-text resume and scores it out of 100."""
import re

from utils.local_matcher import ALIASES, ROLES

ACTION_VERBS = {
    "built", "developed", "designed", "created", "implemented", "led", "managed", "analyzed",
    "improved", "reduced", "increased", "automated", "launched", "delivered", "optimized",
    "organized", "trained", "deployed", "wrote", "collaborated", "coordinated", "engineered",
    "streamlined", "conducted", "presented", "mentored", "volunteered", "achieved", "tested",
    "researched", "configured", "integrated", "migrated", "supported", "taught", "completed",
}


def _lines(text: str) -> list:
    return [l.strip(" -•*\t") for l in (text or "").splitlines() if l.strip(" -•*\t")]


def _has(text: str, skill: str) -> bool:
    names = [skill] + [a for a, c in ALIASES.items() if c == skill]
    return any(re.search(r"(?<![a-z0-9])" + re.escape(n) + r"(?![a-z0-9])", text) for n in names)


def build_resume_text(d: dict, role: str) -> str:
    skills = d.get("skills", [])
    summary = d.get("summary") or (
        f"Aspiring {role} with skills in {', '.join(skills[:5]) or 'technology'}. "
        "Motivated to learn quickly and deliver measurable results."
    )
    contact = " | ".join(x for x in [d.get("email"), d.get("phone"), d.get("location"), d.get("linkedin")] if x)
    out = [d.get("name", "").upper(), contact, "", "PROFESSIONAL SUMMARY", summary, "", "SKILLS", ", ".join(skills)]
    for title, key in [("EXPERIENCE", "experience"), ("PROJECTS", "projects"), ("EDUCATION", "education"),
                    ("CERTIFICATIONS", "certificates"), ("VOLUNTEER WORK", "volunteer"),
                ("INTERESTS & ADDITIONAL", "hobbies")]:
        items = _lines(d.get(key, ""))
        if items:
            out += ["", title] + [f"- {i}" for i in items]
    return "\n".join(out).strip()


def score_resume(d: dict, role: str) -> dict:
    text = build_resume_text(d, role).lower()
    parts = []

    def add(label, got, mx, tip):
        parts.append({"label": label, "got": round(got, 1), "max": mx, "tip": tip})

    # 1. Contact details (10)
    phone_digits = re.sub(r"\D", "", d.get("phone", ""))
    c = (4 if d.get("name", "").strip() else 0)
    c += (3 if re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", d.get("email", "")) else 0)
    c += (3 if len(phone_digits) >= 10 else 0)
    add("Contact details", c, 10, "Add your full name, a valid email and a 10-digit phone number." if c < 10 else "Complete")

    # 2. Key sections (20)
    s = (5 if _lines(d.get("education")) else 0) + (5 if d.get("skills") else 0)
    has_exp, has_proj = bool(_lines(d.get("experience"))), bool(_lines(d.get("projects")))
    s += 10 if (has_exp and has_proj) else 6 if (has_exp or has_proj) else 0
    add("Key sections", s, 20, "Include education, skills, and both experience and projects." if s < 20 else "Complete")

    # 3. Keywords for the target role (25)
    wanted = ROLES[role]["skills"]
    found = [k for k in wanted if _has(text, k)]
    missing = [k for k in wanted if k not in found]
    add(f"Keywords for {role}", 25 * len(found) / len(wanted), 25,
        ("Add these if true for you: " + ", ".join(missing)) if missing else "All key skills present")

    # 4. Action verbs (15) and 5. Numbers (15)
    bullets = _lines(d.get("experience")) + _lines(d.get("projects")) + _lines(d.get("volunteer"))
    if bullets:
        verbs = sum(1 for b in bullets if b.split()[0].lower().strip(",.:") in ACTION_VERBS)
        nums = sum(1 for b in bullets if re.search(r"\d", b))
        add("Action verbs", 15 * verbs / len(bullets), 15,
            "Start each line with a verb like Built, Led, Improved." if verbs < len(bullets) else "Great")
        add("Measurable results", 15 * nums / len(bullets), 15,
            "Add numbers: %, users, time saved, team size." if nums < len(bullets) else "Great")
    else:
        add("Action verbs", 0, 15, "Add experience or project lines starting with action verbs.")
        add("Measurable results", 0, 15, "Add numbers to your achievements.")

    # 6. Length (10)
    words = len(text.split())
    l = 10 if 250 <= words <= 700 else 6 if 150 <= words < 250 or 700 < words <= 900 else 3 if words else 0
    add("Length", l, 10, f"{words} words. Aim for 250-700." if l < 10 else f"{words} words - ideal")

    # 7. Extras (5)
    e = (3 if _lines(d.get("certificates")) else 0) + (2 if _lines(d.get("volunteer")) else 0)
    add("Certificates & volunteer work", e, 5, "Add certificates and volunteer work if you have them." if e < 5 else "Complete")

    return {"total": round(sum(p["got"] for p in parts)), "parts": parts}