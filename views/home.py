from datetime import date, datetime

import altair as alt
import pandas as pd
import streamlit as st

from utils import api
from utils.theme import metric_card
from views.chat_widget import render_chat_popup


def _last_months(n: int = 6) -> list:
    """['2026-05', ..., '2026-10'] ending with the current month."""
    today = date.today()
    keys = []
    for i in range(n - 1, -1, -1):
        m, y = today.month - i, today.year
        while m <= 0:
            m += 12
            y -= 1
        keys.append(f"{y}-{m:02d}")
    return keys


def _safe(fn, uid):
    try:
        return fn(uid)
    except Exception:
        return None


def render(profile: dict) -> None:
    uid = st.session_state.get("uid")
    name = profile.get("name", "")
    st.title(f"Welcome back, {name} 👋" if name else "🎯 CareerGuide AI")
    st.caption("Your real progress: jobs you applied to and skills you completed.")

    apps = _safe(api.get_applications, uid) if uid else None
    prog = _safe(api.get_skill_progress, uid) if uid else None
    if apps is None:
        st.warning("Could not load your applications. Is the backend running?")
    apps, prog = apps or {}, prog or {}

    n_skills = len(profile.get("skills", [])) + len(profile.get("extra_skills", []))
    done = len(prog.get("completed", []))

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Jobs applied (total)", str(apps.get("total", 0)))
    with c2:
        metric_card("Applied this month", str(apps.get("this_month", 0)))
    with c3:
        metric_card("Skills completed", f"{done} / {n_skills}")

    # ---- Chart: last 6 months, real data only ----
    keys = _last_months(6)
    labels = [datetime.strptime(k, "%Y-%m").strftime("%b") for k in keys]
    jobs_m, skills_m = apps.get("by_month", {}), prog.get("by_month", {})
    df = pd.DataFrame({
        "Month": labels,
        "Jobs applied": [jobs_m.get(k, 0) for k in keys],
        "Skills completed": [skills_m.get(k, 0) for k in keys],
    })

    st.subheader("Jobs applied vs. skills completed")
    top = max(4, int(df[["Jobs applied", "Skills completed"]].max().max()) + 1)
    long = df.melt("Month", var_name="Series", value_name="Count")
    chart = (
        alt.Chart(long)
        .mark_bar(size=16, cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Month:N", sort=labels, title=None, axis=alt.Axis(labelAngle=0)),
            xOffset="Series:N",
            y=alt.Y("Count:Q", title="Count", scale=alt.Scale(domain=[0, top]),
                    axis=alt.Axis(tickMinStep=1)),
            color=alt.Color(
                "Series:N",
                scale=alt.Scale(domain=["Jobs applied", "Skills completed"],
                                range=["#2E86DE", "#1E9E6A"]),
                legend=alt.Legend(orient="top", title=None),
            ),
            tooltip=["Month", "Series", "Count"],
        )
        .properties(width="container", height=340)
    )
    st.altair_chart(chart)

    if apps.get("total", 0) == 0 and done == 0:
        st.info("Nothing to show yet. Press **I applied ✅** on a job in **💼 Recommendations**, "
                "and tick finished skills on **🧩 Skill Gap**. This chart updates automatically.")
    else:
        st.caption("Jobs applied counts the jobs you marked as applied. "
                "Skills completed counts the skills you ticked as done.")

    by_skill = apps.get("by_skill", {})
    if by_skill:
        with st.expander("📌 Applications by skill"):
            for skill, n in sorted(by_skill.items(), key=lambda x: -x[1]):
                st.markdown(f"- **{skill}**: {n}")

    items = apps.get("items", [])
    if items:
        with st.expander("🕘 Recent applications"):
            for it in sorted(items, key=lambda i: i["applied_at"], reverse=True)[:8]:
                job = it["job"]
                who = f" at {job['company']}" if job.get("company") else ""
                st.markdown(f"- {job['title']}{who} · {it['applied_at'][:10]}")

    render_chat_popup()