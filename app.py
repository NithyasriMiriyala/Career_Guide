import hashlib
import re
from datetime import date

import streamlit as st
import streamlit.components.v1 as components

from utils import api
from utils.local_matcher import EDUCATION_OPTIONS, EXPERIENCE_LEVELS, ROLES, interests_for
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
    "C Programming", "C++", "Embedded Systems", "Microcontrollers", "IoT", "Verilog",
    "MATLAB", "Signal Processing", "Networking", "CAD",
]
LEVELS = ["Beginner", "Intermediate", "Advanced"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------- Login screen (shown when there is no ?uid= in the address) ----------
def _submit_auth(email: str, password: str, create: bool) -> None:
    e = email.strip().lower()
    if not EMAIL_RE.match(e):
        st.error("Please enter a valid email address.")
        return
    if not password:
        st.error("Please enter your password.")
        return
    if create and len(password) < 8:
        st.error("Use at least 8 characters for the password.")
        return
    with st.spinner("Contacting the server... the first request can take up to a minute."):
        new_uid, error = (api.register if create else api.login)(e, password)
    if error:
        st.error(error)
        return
    st.session_state["email"] = e
    st.session_state["flash"] = "login"
    st.query_params["uid"] = new_uid
    st.rerun()


def login_screen() -> None:
    # make sure the slim left bar from an earlier visit doesn't affect this page
    components.html(
        "<script>const P=window.parent; if(P.__cgNavTimer){P.clearInterval(P.__cgNavTimer);}"
        "P.document.body.classList.remove('cg-scrolled');</script>",
        height=0,
    )
    st.markdown('<div class="cg-brand">🎯 CareerGuide AI</div>', unsafe_allow_html=True)
    st.title("Welcome 👋")
    st.caption("Log in to open your saved profile, applications and progress, or create an account.")
    tab_in, tab_up = st.tabs(["🔑 Log in", "✨ Create account"])
    with tab_in:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password")
            go = st.form_submit_button("Log in", type="primary")
        if go:
            _submit_auth(email, password, create=False)
    with tab_up:
        with st.form("signup_form"):
            s_email = st.text_input("Email", placeholder="you@example.com", key="su_email")
            s_pw = st.text_input("Choose a password (at least 8 characters)", type="password", key="su_pw")
            s_pw2 = st.text_input("Confirm password", type="password", key="su_pw2")
            go2 = st.form_submit_button("Create account", type="primary")
        if go2:
            if s_pw != s_pw2:
                st.error("The two passwords don't match.")
            else:
                _submit_auth(s_email, s_pw, create=True)
        st.caption("Used this site before with just your email? Create an account with the same "
                "email and your saved data will be kept.")
    st.stop()


# ---------- User id (kept in the web address) and saved profile ----------
uid = st.query_params.get("uid")
if not uid:
    login_screen()
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
    email = st.session_state.get("email")
    if p.get("name"):
        st.success("✅ Profile saved")
    else:
        st.info("Your profile isn't saved yet. Fill it in and press **Save profile**.")
    st.caption(f"Signed in as {email}" if email else f"Profile ID: {uid}")

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

    # Education decides which interests are offered below
    saved_edu = p.get("education", "")
    edu_options = ["(select your education)"] + EDUCATION_OPTIONS
    if saved_edu and saved_edu not in edu_options:
        edu_options.append(saved_edu)  # keep an older free-text value visible
    education_pick = st.selectbox(
        "Education", edu_options,
        index=edu_options.index(saved_edu) if saved_edu in edu_options else 0, key="p_edu_sel",
    )
    education = "" if education_pick.startswith("(select") else education_pick

    options = interests_for(education)
    if "p_interests" not in st.session_state:
        st.session_state["p_interests"] = [i for i in p.get("interests", []) if i in options]
    else:  # drop interests that don't belong to the newly chosen education
        st.session_state["p_interests"] = [i for i in st.session_state["p_interests"] if i in options]
    interests = st.multiselect("Interests (these change with your education)", options, key="p_interests")

    goal_options = ["(not set)"] + list(ROLES)
    saved_goal = p.get("career_goal", "")
    career_goal = st.selectbox(
        "Career goal (the role you want)", goal_options,
        index=goal_options.index(saved_goal) if saved_goal in goal_options else 0, key="p_goal",
    )

    saved_level = p.get("experience_level", EXPERIENCE_LEVELS[0])
    experience_level = st.selectbox(
        "Experience level", EXPERIENCE_LEVELS,
        index=EXPERIENCE_LEVELS.index(saved_level) if saved_level in EXPERIENCE_LEVELS else 0,
        key="p_exp_level",
    )
    experience = st.text_area(
        "Experience, internships or projects (optional, one per line)", p.get("experience", ""),
        height=100, key="p_exp",
        placeholder="Built a Python API with SQL during my internship at XYZ",
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
            "education": education,
            "interests": interests,
            "career_goal": "" if career_goal == "(not set)" else career_goal,
            "experience_level": experience_level,
            "experience": experience.strip(),
            "skills": skills,
            "extra_skills": extra_list,
            "levels": levels,
        }
        st.session_state["profile"] = new_profile
        ok = api.save_profile(uid, new_profile, st.session_state.get("targets", {}))
        st.session_state["flash"] = "ok" if ok else "fail"
        st.rerun()

# ---------- Top bar: brand | menu | profile | log out ----------
brand_col, nav_col, profile_col, logout_col = st.columns([1.6, 8.2, 1.2, 1.2])
with brand_col:
    st.markdown('<div class="cg-brand">🎯 CareerGuide AI</div>', unsafe_allow_html=True)
with nav_col:
    page = st.radio("Navigate", PAGES, horizontal=True, label_visibility="collapsed")
with profile_col:
    if st.button("👤 Profile", key="profile_btn"):
        profile_dialog()
with logout_col:
    if st.button("🚪 Log out", key="logout_btn"):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()

flash = st.session_state.pop("flash", None)
if flash == "ok":
    st.toast("Profile saved ✅", icon="✅")
elif flash == "fail":
    st.toast("Saved on this page only. The backend isn't reachable.", icon="⚠️")
elif flash == "login":
    has_profile = bool(st.session_state["profile"].get("name"))
    st.toast("Welcome back! Your profile is loaded ✅" if has_profile
            else "Logged in. Create your profile with the 👤 button.", icon="👋")

profile = st.session_state["profile"]
profile["user_id"] = uid  # so the Apply / tick buttons know who the user is

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