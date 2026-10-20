import uuid
from datetime import date

import streamlit as st

from utils import api
from utils.theme import inject_css, nav_scroll_behavior
from views import home, recommendations, resume, roadmap, skill_gap

st.set_page_config(
    page_title="CareerGuide AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()

PAGES = ["🏠 Home", "💼 Recommendations", "🧩 Skill Gap", "🗺️ Learning Roadmap", "📄 Resume Builder"]

SKILL_OPTIONS = [
    "Python", "SQL", "Java", "JavaScript", "HTML", "CSS", "React", "Node.js",
    "Machine Learning", "Deep Learning", "LLMs", "APIs", "Docker", "Git",
    "Cloud", "Excel", "Power BI", "Statistics", "Data Visualization", "Communication",
]
LEVELS = ["Beginner", "Intermediate", "Advanced"]

# ---------- User id (kept in the web address) and saved profile ----------
uid = st.query_params.get("uid")
if not uid:
    uid = uuid.uuid4().hex[:8]
    st.query_params["uid"] = uid
st.session_state["uid"] = uid

if "profile" not in st.session_state:
    saved = api.get_profile(uid)
    if saved:
        st.session_state["targets"] = saved.pop("targets", {})
    st.session_state["profile"] = saved or {}


# ---------- Profile dialog (closes automatically after saving) ----------
@st.dialog("👤 Your Profile")
def profile_dialog():
    p = st.session_state["profile"]
    name = st.text_input("Name", p.get("name", ""), key="p_name")
    if "p_dob" not in st.session_state:  # load the saved date once
        st.session_state["p_dob"] = p.get("dob", date(2003, 1, 1))
    dob = st.date_input(
        "Date of birth",
        min_value=date(1950, 1, 1),
        max_value=date.today(),
        format="DD/MM/YYYY",
        key="p_dob",
    )
    grad_year = st.number_input(
        "Graduated year", 1990, 2040, int(p.get("grad_year", 2026)),
        step=1, format="%d", key="p_grad",
    )
    skills = st.multiselect("Skillset", SKILL_OPTIONS, default=p.get("skills", []), key="p_skills")
    extra = st.text_input(
        "Other skills (comma separated)", ", ".join(p.get("extra_skills", [])), key="p_extra"
    )
    taken = [s.lower() for s in skills]
    extra_list = []
    for s in extra.split(","):
        s = s.strip()
        if s and s.lower() not in taken and s.lower() not in [e.lower() for e in extra_list]:
            extra_list.append(s)

    levels = {}
    all_skills = skills + extra_list
    if all_skills:
        st.markdown("**How well do you know each skill?**")
        saved_levels = p.get("levels", {})
        for s in all_skills:
            left, right = st.columns([2, 3])
            left.markdown(f"**{s}**")
            levels[s] = right.selectbox(
                s, LEVELS,
                index=LEVELS.index(saved_levels.get(s, "Beginner")),
                key=f"lvl_{s}", label_visibility="collapsed",
            )

    if st.button("Save profile", type="primary"):
        new_profile = {
            "name": name.strip(),
            "dob": dob,
            "grad_year": int(grad_year),
            "skills": skills,
            "extra_skills": extra_list,
            "levels": levels,
        }
        st.session_state["profile"] = new_profile
        ok = api.save_profile(uid, new_profile, st.session_state.get("targets", {}))
        st.session_state["flash"] = "ok" if ok else "fail"
        st.rerun()  # closes the dialog


# ---------- Top bar: brand | menu | profile (top-right) ----------
brand_col, nav_col, profile_col = st.columns([1.6, 9, 1.2])
with brand_col:
    st.markdown('<div class="cg-brand">🎯 CareerGuide AI</div>', unsafe_allow_html=True)
with nav_col:
    page = st.radio("Navigate", PAGES, horizontal=True, label_visibility="collapsed")
with profile_col:
    if st.button("👤 Profile"):
        profile_dialog()

flash = st.session_state.pop("flash", None)
if flash == "ok":
    st.toast("Profile saved to the backend ✅", icon="✅")
elif flash == "fail":
    st.toast("Saved on this page only. The backend isn't reachable.", icon="⚠️")

profile = st.session_state["profile"]

# ---------- Page body ----------
if page == "🏠 Home":
    home.render(profile)
elif page == "💼 Recommendations":
    recommendations.render(profile)
elif page == "🧩 Skill Gap":
    skill_gap.render(profile)
elif page == "🗺️ Learning Roadmap":
    roadmap.render(profile)
elif page == "📄 Resume Builder":
    resume.render(profile)

nav_scroll_behavior()