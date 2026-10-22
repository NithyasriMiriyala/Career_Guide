from urllib.parse import quote_plus
import os

import requests
import streamlit as st

from utils import api
from utils.local_matcher import match_roles
from utils.theme import chips


def _slug(text: str) -> str:
    return "-".join("".join(c if c.isalnum() else " " for c in text.lower()).split())


# name, icon, what it is good for, URL builder(query, location, kind)
PORTALS = [
    ("LinkedIn", "💼", "Jobs, internships and recruiters",
    lambda q, l, k: f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(q)}"
                    f"&location={quote_plus(l)}" + ("&f_JT=I" if k == "Internships" else "")),
    ("Indeed", "🔎", "Large job board, easy filters",
    lambda q, l, k: f"https://in.indeed.com/jobs?q={quote_plus(q + (' internship' if k == 'Internships' else ''))}"
                    f"&l={quote_plus(l)}"),
    ("Naukri", "🇮🇳", "Popular in India for freshers and experienced",
    lambda q, l, k: f"https://www.naukri.com/{_slug(q)}{'-internship' if k == 'Internships' else ''}-jobs"
                    f"{'-in-' + _slug(l) if l else ''}"),
    ("Wellfound", "🚀", "Startup jobs and internships",
    lambda q, l, k: "https://www.google.com/search?q=" +
                quote_plus(f"site:wellfound.com/jobs {q} {'internship' if k == 'Internships' else ''} {l}")),
    ("Internshala", "🎓", "Internships and fresher jobs",
    lambda q, l, k: f"https://internshala.com/{'internships' if k == 'Internships' else 'jobs'}"
                    f"/keywords-{_slug(q)}/"),
    ("Glassdoor", "🏢", "Jobs with salary and company reviews",
    lambda q, l, k: f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword="
                    f"{quote_plus(q + (' internship' if k == 'Internships' else ''))}"),
        ("Foundit", "🧭", "Formerly Monster India",
    lambda q, l, k: "https://www.google.com/search?q=" +
                    quote_plus(f"site:foundit.in {q} {'internship' if k == 'Internships' else 'jobs'} {l}")),
    ("Google Jobs", "🌐", "Combines listings from many sites",
    lambda q, l, k: "https://www.google.com/search?ibp=htl;jobs&q=" +
                quote_plus(f"{q} {'internship' if k == 'Internships' else 'jobs'} {l}")),
]


def _record(uid: str, portal: str, role: str, kind: str, loc: str, url: str, skills: list) -> None:
    job = {"id": f"link-{_slug(portal)}-{_slug(role)}-{_slug(kind)}",
        "title": f"{role} ({kind[:-1] if kind.endswith('s') else kind})",
        "company": portal, "location": loc or "Any", "url": url,
        "source": portal, "kind": "search"}
    try:
        api.mark_applied(uid, job, skills)
        st.toast(f"Saved: applied via {portal} ✅")
    except api.ApiError as e:
        st.toast(f"Could not save: {e}", icon="⚠️")

@st.cache_data(ttl=300, show_spinner=False)
def _backend_rank(skills: tuple, goal: str, interests: tuple):
    base = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    r = requests.post(f"{base}/recommend", timeout=30,
                    json={"skills": list(skills), "career_goal": goal, "interests": list(interests)})
    r.raise_for_status()
    return r.json()["roles"]


def _rank(skills, goal, interests):
    try:
        return _backend_rank(tuple(skills), goal, tuple(interests)), "scikit-learn"
    except Exception:
        return match_roles(skills, goal, interests), "rule-based"
def render(profile: dict) -> None:
    st.title("💼 Recommendations")
    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    if not skills:
        st.info("Add your skills in **👤 Profile** (top right) to get recommendations.")
        return

    ranked, engine = _rank(skills, profile.get("career_goal", ""), profile.get("interests", []))

    st.subheader("Best-fit roles for you")
    st.caption(f"Ranked by the {engine} matcher.")
    cols = st.columns(3)
    for col, r in zip(cols, ranked[:3]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{r['role']}**")
                st.markdown(f"{r['score']}% match")
                for why in r.get("reasons", []):
                    st.caption(why)
                st.markdown(chips(r["matched"], "have"), unsafe_allow_html=True)

    st.divider()
    st.subheader("🔗 Find jobs and internships")
    st.caption("Pick what you want, then open any portal. Each one opens a ready-made search "
            "in a new tab, and you apply on the company's own listing.")

    role_names = [r["role"] for r in ranked]
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        role = st.selectbox("Role", role_names + ["Other (type below)"])
    with c2:
        loc = st.text_input("Location", value="India", placeholder="e.g. Hyderabad, Remote")
    with c3:
        kind = st.radio("Looking for", ["Jobs", "Internships"], horizontal=True)

    if role.startswith("Other"):
        role = st.text_input("Type the role", placeholder="e.g. Frontend Developer").strip()
    add_skills = st.checkbox("Add my top skills to the search", value=False)

    if not role:
        st.info("Type a role to see the search links.")
        return

    query = role + (" " + " ".join(skills[:2]) if add_skills else "")
    uid = profile.get("user_id", "")

    for i in range(0, len(PORTALS), 2):
        row = st.columns(2)
        for col, (name, icon, blurb, build) in zip(row, PORTALS[i:i + 2]):
            url = build(query, loc.strip(), kind)
            with col:
                with st.container(border=True):
                    st.markdown(f"### {icon} {name}")
                    st.caption(blurb)
                    b1, b2 = st.columns(2)
                    with b1:
                        st.link_button(f"Search {kind.lower()} ↗", url, use_container_width=True)
                    with b2:
                        if st.button("I applied ✅", key=f"ap-{name}-{role}-{kind}",
                                    use_container_width=True):
                            _record(uid, name, role, kind, loc, url, skills)

    st.caption("Tip: after you apply on a portal, press **I applied ✅** on its card so your "
            "Home graph stays accurate.")