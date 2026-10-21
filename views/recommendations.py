import streamlit as st
from utils import api
from utils.local_matcher import match_roles
from utils.theme import chips, metric_card


def _applied(uid):
    """Return (set of applied job ids, total applications)."""
    if not uid:
        return set(), 0
    try:
        data = api.get_applications(uid)
        return {i["job"]["id"] for i in data.get("items", [])}, data.get("total", 0)
    except Exception:
        return set(), 0


def _salary(job) -> str:
    lo, hi = job.get("salary_min"), job.get("salary_max")
    if lo and hi:
        return f"Salary: {int(lo):,} – {int(hi):,} per year"
    if lo or hi:
        return f"Salary: about {int(lo or hi):,} per year"
    return ""


def render(profile: dict) -> None:
    st.title("💼 Recommendations")
    msg = st.session_state.pop("apply_flash", None)
    if msg:
        st.toast(msg)

    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    uid = profile.get("user_id")
    if not skills:
        st.info("Add your skills in **👤 Profile** (top right) to get recommendations.")
        return

    # ---- Roles that fit your skills ----
    st.markdown("#### 🎯 Roles that fit your skills")
    cols = st.columns(3)
    for col, r in zip(cols, match_roles(skills)[:3]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{r['role']}**")
                st.markdown(f"{r['score']}% match")
                st.markdown(chips(r["matched"], "have"), unsafe_allow_html=True)

    # ---- Job search ----
    st.markdown("#### 🔎 Jobs you can apply to")
    with st.form("job_search"):
        c1, c2, c3 = st.columns([2, 2, 1.4])
        pick = c1.selectbox("Search for", ["All my skills"] + skills)
        q = c2.text_input("Extra keyword (optional)", placeholder="e.g. fresher, intern, analyst")
        loc = c3.text_input("Location", "India")
        st.form_submit_button("🔎 Find jobs", type="primary")

    search_skills = skills[:8] if pick == "All my skills" else [pick]
    params = (tuple(search_skills), q.strip(), (loc.strip() or "India"))
    cache = st.session_state.get("jobs_result")
    if cache is None or cache["params"] != params:
        with st.spinner("Finding jobs..."):
            try:
                data = api.get_jobs(list(params[0]), params[1], params[2])
            except Exception as exc:
                st.error(f"Could not load jobs. Is the backend running? ({exc})")
                return
        cache = {"params": params, "data": data}
        st.session_state["jobs_result"] = cache
    data = cache["data"]
    jobs = sorted(data["jobs"], key=lambda j: -len(j.get("skills_matched", [])))[:30]

    applied, total = _applied(uid)
    a, b = st.columns(2)
    with a:
        metric_card("Jobs you applied to", str(total))
    with b:
        metric_card("Jobs shown", str(len(jobs)))
    if data.get("note"):
        st.info(data["note"])
    if data["source"] == "adzuna":
        st.caption("Click **Apply ↗** to open the job's apply page in a new tab. After you apply there, "
                   "come back and press **I applied ✅** so it counts on your Home graph.")
    else:
        st.caption("These open job-site searches. Apply on the site, then come back and press "
                "**I applied ✅** so it counts on your Home graph.")
    if not uid:
        st.warning("Save your profile first so your applications can be recorded.")

    # ---- Job cards ----
    for job in jobs:
        jid = job["id"]
        is_search = job.get("kind") == "search"
        done = jid in applied and not is_search
        with st.container(border=True):
            left, mid, right = st.columns([5, 1.6, 1.8])
            with left:
                st.markdown(f"**{job['title']}**")
                meta = " · ".join(x for x in [job.get("company"), job.get("location"), job.get("posted")] if x)
                if meta:
                    st.caption(meta)
                sal = _salary(job)
                if sal:
                    st.caption(sal)
                if job.get("skills_matched"):
                    st.markdown(chips(job["skills_matched"], "have"), unsafe_allow_html=True)
            with mid:
                label = f"Open {job['source']} ↗" if is_search else "Apply ↗"
                st.link_button(label, job["url"], use_container_width=True)
            with right:
                if done:
                    st.success("Applied ✅")
                elif uid and st.button("I applied ✅", key=f"ap_{jid}", use_container_width=True):
                    try:
                        api.mark_applied(uid, job, job.get("skills_matched") or search_skills[:1] or ["Other"])
                        st.session_state["apply_flash"] = "Saved. It now counts on your Home graph ✅"
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not save: {exc}")