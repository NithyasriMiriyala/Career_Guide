import re

import streamlit as st

from utils import api
from utils.ats import build_resume_text, score_resume
from utils.local_matcher import ROLES, match_roles
from utils.theme import chips, metric_card

COUNTRY_CODES = [
    "🇮🇳 +91 India", "🇺🇸 +1 USA", "🇬🇧 +44 UK", "🇨🇦 +1 Canada", "🇦🇺 +61 Australia",
    "🇦🇪 +971 UAE", "🇸🇬 +65 Singapore", "🇩🇪 +49 Germany", "🇫🇷 +33 France", "🇳🇱 +31 Netherlands",
    "🇸🇦 +966 Saudi Arabia", "🇶🇦 +974 Qatar", "🇰🇼 +965 Kuwait", "🇴🇲 +968 Oman", "🇧🇭 +973 Bahrain",
    "🇲🇾 +60 Malaysia", "🇮🇩 +62 Indonesia", "🇵🇭 +63 Philippines", "🇹🇭 +66 Thailand", "🇻🇳 +84 Vietnam",
    "🇯🇵 +81 Japan", "🇰🇷 +82 South Korea", "🇨🇳 +86 China", "🇭🇰 +852 Hong Kong", "🇳🇿 +64 New Zealand",
    "🇿🇦 +27 South Africa", "🇳🇬 +234 Nigeria", "🇰🇪 +254 Kenya", "🇪🇬 +20 Egypt", "🇹🇷 +90 Turkey",
    "🇧🇩 +880 Bangladesh", "🇳🇵 +977 Nepal", "🇱🇰 +94 Sri Lanka", "🇵🇰 +92 Pakistan", "🇧🇷 +55 Brazil",
    "🇲🇽 +52 Mexico", "🇮🇹 +39 Italy", "🇪🇸 +34 Spain", "🇸🇪 +46 Sweden", "🇨🇭 +41 Switzerland",
]


def _file_stem(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_") or "resume"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _missing_fields(name, email, digits, skills, education, experience, projects) -> list:
    miss = []
    if not name.strip():
        miss.append("Full name")
    if not EMAIL_RE.match(email.strip()):
        miss.append("a valid Email")
    if not digits:
        miss.append("Phone number")
    if not [s for s in skills.split(",") if s.strip()]:
        miss.append("Skills")
    if not education.strip():
        miss.append("Education")
    if not (experience.strip() or projects.strip()):
        miss.append("Experience or Projects (at least one)")
    return miss

def render(profile: dict) -> None:
    st.title("📄 Resume Builder")
    st.caption("Fill in your details. One item per line in the big boxes. "
            "Start each line with an action verb and include numbers, for example: "
            "*Built a sales dashboard in Power BI used by 40 managers*.")

    d = st.session_state.setdefault("resume", {})
    profile_skills = profile.get("skills", []) + profile.get("extra_skills", [])
    roles = list(ROLES.keys())

    with st.form("resume_form"):
        a, b = st.columns(2)
        name = a.text_input("Full name", d.get("name", profile.get("name", "")))
        role = b.selectbox("Target role", roles, index=roles.index(d.get("role", roles[0])))
        c, e, f = st.columns([1, 1.5, 1])
        email = c.text_input("Email", d.get("email", ""))
        with e:
            cc_col, num_col = st.columns([2, 3])
            code_label = cc_col.selectbox(
                "Country code", COUNTRY_CODES,
                index=COUNTRY_CODES.index(d.get("phone_code", COUNTRY_CODES[0])),
            )
            number = num_col.text_input(
                "Phone (max 10 digits)", d.get("phone_number", ""), max_chars=10, placeholder="9876543210"
            )
        location = f.text_input("City / location", d.get("location", ""), key="r_location")
        linkedin = st.text_input("LinkedIn / GitHub link", d.get("linkedin", ""))
        skills = st.text_input("Skills (comma separated)", d.get("skills_text", ", ".join(profile_skills)))
        summary = st.text_area("Summary (optional, we write one if empty)", d.get("summary", ""), height=80)
        education = st.text_area("Education", d.get("education", ""), height=100,
                                placeholder="B.Tech in Computer Science, ABC University, 2026, CGPA 8.4")
        experience = st.text_area("Experience / internships", d.get("experience", ""), height=130,
                                placeholder="Data Analyst Intern at XYZ: Reduced report time by 30% by automating Excel tasks")
        projects = st.text_area("Projects", d.get("projects", ""), height=130,
                                placeholder="Built a job recommender in Python using scikit-learn with 85% accuracy")
        certificates = st.text_area("Certificates", d.get("certificates", ""), height=90)
        volunteer = st.text_area("Volunteer work", d.get("volunteer", ""), height=90)
        hobbies = st.text_area("Hobbies, languages & other (optional)", d.get("hobbies", ""), height=80)
        go = st.form_submit_button("Generate resume & ATS score", type="primary")

    if go:
        code = code_label.split()[1]
        digits = number.strip()
        missing = _missing_fields(name, email, digits, skills, education, experience, projects)
        problem = None
        if digits:
            if not digits.isdigit():
                problem = "Phone number must contain digits only."
            elif code == "+91" and (len(digits) != 10 or digits[0] not in "6789"):
                problem = "Indian numbers must be exactly 10 digits and start with 6, 7, 8 or 9."
            elif code != "+91" and not 6 <= len(digits) <= 10:
                problem = "Enter 6 to 10 digits for the phone number."

        if missing:
            st.session_state["resume_valid"] = False
            st.error("Please fill in: " + ", ".join(missing) + " before generating your resume.")
            return
        if problem:
            st.session_state["resume_valid"] = False
            st.error(problem)
            return

        st.session_state["resume"] = {
            "name": name, "role": role, "email": email.strip(),
            "phone": f"{code} {digits}",
            "phone_code": code_label, "phone_number": digits,
            "location": location, "linkedin": linkedin, "skills_text": skills,
            "skills": [s.strip() for s in skills.split(",") if s.strip()],
            "summary": summary, "education": education, "experience": experience,
            "projects": projects, "certificates": certificates, "volunteer": volunteer,
            "hobbies": hobbies,
        }
        st.session_state["resume_valid"] = True
        d = st.session_state["resume"]
        # Save to the database (Atlas) only when the resume is valid
        uid = profile.get("user_id")
        if uid:
            try:
                api.save_resume(uid, d)
                st.toast("Resume saved ✅")
            except Exception as exc:
                st.warning(f"Resume generated, but it could not be saved to the database: {exc}")

    if not st.session_state.get("resume_valid"):
        st.info("Fill in the form above and click **Generate resume & ATS score** to see your score.")
        return

    role = d["role"]
    result = score_resume(d, role)
    total = result["total"]
    text = build_resume_text(d, role)

    st.divider()
    x, y = st.columns([1, 2])
    with x:
        metric_card("ATS score", f"{total} / 100")
        st.progress(total / 100)
        if total >= 80:
            st.success("Excellent: ready to apply.")
        elif total >= 60:
            st.warning("Good: a few fixes will help.")
        else:
            st.error("Needs work: follow the tips.")
    with y:
        st.markdown("#### Score breakdown")
        for p in result["parts"]:
            st.markdown(f"**{p['label']}**: {p['got']:g} / {p['max']}  ·  _{p['tip']}_")

    st.markdown("#### 🎯 Jobs that fit your resume")
    for r in match_roles(d["skills"])[:3]:
        st.markdown(f"**{r['role']}** - {r['score']}% match")
        st.markdown(chips(r["matched"], "have"), unsafe_allow_html=True)

    st.markdown("#### Your ATS-friendly resume")
    st.caption("One column, standard headings, plain text and no tables or images, "
            "which is what applicant tracking systems read best.")
    st.code(text, language=None)

    st.markdown("#### ⬇️ Download")
    stem = _file_stem(d["name"]) + "_Resume"
    c1, c2, c3 = st.columns(3)
    try:
        from utils.resume_files import make_docx, make_pdf
        c1.download_button("⬇️ Download PDF", make_pdf(d, role), file_name=f"{stem}.pdf",
                        mime="application/pdf", type="primary", key="dl_pdf")
        c2.download_button("⬇️ Download Word (.docx)", make_docx(d, role), file_name=f"{stem}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="dl_docx")
    except ImportError:
        st.error("PDF/Word export needs two packages. In your terminal run: "
                "`pip install reportlab python-docx` and restart Streamlit.")
    c3.download_button("⬇️ Download text (.txt)", text, file_name=f"{stem}.txt", key="dl_txt")