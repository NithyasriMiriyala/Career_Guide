import re

import streamlit as st

from utils import api
from utils.ats import build_resume_text, score_resume
from utils.local_matcher import match_roles

WELCOME = ("Hi! I'm your CareerGuide AI assistant. Ask me about careers, skills or interviews, "
           "or say **\"build my resume\"** and I'll guide you step by step.")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

RB_STEPS = [
    ("name", "What is your full name?"),
    ("email", "What is your email address?"),
    ("phone", "Your phone number? (Indian mobile, 10 digits. For other countries use the Resume Builder page.)"),
    ("location", "Which city do you live in? (or type skip)"),
    ("education", "Tell me about your education: degree, college, year, CGPA. Separate items with a semicolon (;)."),
    ("skills", "Which skills should go on your resume? (comma separated)"),
    ("experience", "Any work experience or internships? Start each with a verb and add numbers, "
                   "e.g. *Reduced report time by 30%*. Separate items with ; (or skip)"),
    ("projects", "Tell me about your projects, separated by ; (or skip)"),
    ("certificates", "Any certificates? Separate with ; (or skip)"),
    ("volunteer", "Any volunteer work? Separate with ; (or skip)"),
    ("hobbies", "Hobbies, languages, awards or anything else you'd like to add? (or skip)"),
]
REQUIRED = {"name", "email", "phone", "education"}
MULTILINE = {"education", "experience", "projects", "certificates", "volunteer", "hobbies"}


def _reply(message: str) -> str:
    res = api.chat(st.session_state.get("uid", "guest"), message)
    if res is None:
        return "I can't reach the backend right now. Make sure the server is running on port 8000."
    text = res["reply"]
    if res.get("sources"):
        text += "\n\n*Sources: " + ", ".join(res["sources"]) + "*"
    return text


def _next_question(data: dict):
    return next((q for k, q in RB_STEPS if k not in data), None)


def _start_resume() -> str:
    profile = st.session_state.get("profile", {})
    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    data = {}
    if profile.get("name"):
        data["name"] = profile["name"]
    if skills:
        data["skills"] = ", ".join(skills)
    st.session_state["rb"] = {"data": data}
    known = ""
    if data:
        known = "I'll use these from your Profile: " + ", ".join(
            f"{k} ({v})" for k, v in data.items()) + ".\n\n"
    return ("Great, let's build your ATS-friendly resume. Type **skip** to skip optional questions "
            "or **cancel** to stop.\n\n" + known + _next_question(data))


def _finish(data: dict) -> str:
    skills = [s.strip() for s in data.get("skills", "").split(",") if s.strip()]
    role = match_roles(skills)[0]["role"] if skills else "AI Engineer"
    digits = data["phone"]
    d = {
        "name": data["name"], "role": role, "email": data["email"],
        "phone": f"+91 {digits}", "phone_code": "🇮🇳 +91 India", "phone_number": digits,
        "location": data.get("location", ""), "linkedin": "",
        "skills_text": ", ".join(skills), "skills": skills, "summary": "",
        "education": data.get("education", ""), "experience": data.get("experience", ""),
        "projects": data.get("projects", ""), "certificates": data.get("certificates", ""),
        "volunteer": data.get("volunteer", ""), "hobbies": data.get("hobbies", ""),
    }
    st.session_state["resume"] = d                     # the Resume Builder page shows it too
    api.save_resume(st.session_state.get("uid", "guest"), d)
    result = score_resume(d, role)
    text = build_resume_text(d, role)
    tips = [f"- **{p['label']}**: {p['tip']}" for p in result["parts"] if p["got"] < p["max"]]
    st.session_state["rb"] = None
    reply = f"✅ Your resume is ready for **{role}**.\n\n**ATS score: {result['total']} / 100**\n\n"
    if tips:
        reply += "To improve it:\n" + "\n".join(tips) + "\n\n"
    return reply + "```\n" + text + "\n```\nOpen **📄 Resume Builder** to edit it and download."


def _resume_step(rb: dict, message: str) -> str:
    data = rb["data"]
    key, question = next((k, q) for k, q in RB_STEPS if k not in data)
    text = message.strip()
    skip = text.lower() == "skip"

    if skip and key in REQUIRED:
        return "I need that one for the resume. " + question
    if key == "email" and not EMAIL_RE.match(text):
        return "That doesn't look like a valid email. " + question
    if key == "phone":
        digits = re.sub(r"[\s\-]", "", text).removeprefix("+91")
        if not digits.isdigit() or len(digits) != 10 or digits[0] not in "789":
            return "Indian numbers must be exactly 10 digits and start with 7, 8 or 9. " + question
        data[key] = digits
    elif skip:
        data[key] = ""
    elif key in MULTILINE:
        data[key] = "\n".join(p.strip() for p in text.split(";") if p.strip())
    else:
        data[key] = text

    nxt = _next_question(data)
    return nxt if nxt else _finish(data)


def _handle(message: str) -> str:
    rb = st.session_state.get("rb")
    low = message.lower().strip()
    if rb:
        if low in ("cancel", "stop", "exit"):
            st.session_state["rb"] = None
            return "No problem, I've stopped the resume builder. Ask me anything else."
        return _resume_step(rb, message)
    if "resume" in low and any(w in low for w in ("build", "create", "make", "write", "generate", "prepare")):
        return _start_resume()
    return _reply(message)


def render_chat_popup() -> None:
    history = st.session_state.setdefault(
        "chat_history", [{"role": "assistant", "content": WELCOME}]
    )

    with st.container(key="chatpop"):
        with st.popover("💬 Ask CareerGuide AI"):
            st.markdown("**CareerGuide AI Assistant**")
            box = st.container(height=320)  # messages appear here

            with st.form("chat_form", clear_on_submit=True):
                msg = st.text_input(
                    "Message", placeholder="Ask me anything…", label_visibility="collapsed"
                )
                sent = st.form_submit_button("Send")

            if sent and msg.strip():
                history.append({"role": "user", "content": msg.strip()})
                history.append({"role": "assistant", "content": _handle(msg.strip())})

            with box:
                for m in history:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])