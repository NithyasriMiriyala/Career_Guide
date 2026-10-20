import altair as alt
import pandas as pd
import streamlit as st

from utils.theme import metric_card
from views.chat_widget import render_chat_popup

MONTHS = ["May", "Jun", "Jul", "Aug", "Sep", "Oct"]


def _sample_progress() -> pd.DataFrame:
    return pd.DataFrame({
        "Month": MONTHS,
        "Jobs applied": [2, 5, 8, 6, 11, 14],
        "Skills": [2, 3, 5, 6, 8, 9],
    })


def render(profile: dict) -> None:
    name = profile.get("name", "")
    st.title(f"Welcome back, {name} 👋" if name else "🎯 CareerGuide AI")
    st.caption("Track your job applications and how many skills you have.")

    stored = st.session_state.setdefault("progress", _sample_progress())
    df = stored.copy()

    # Skills = number of skills saved in the Profile; the latest month follows it
    n_skills = len(profile.get("skills", [])) + len(profile.get("extra_skills", []))
    if n_skills > 0:
        df.loc[df.index[-1], "Skills"] = n_skills

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Jobs applied (total)", str(int(df["Jobs applied"].sum())))
    with c2:
        metric_card("Applied this month", str(int(df["Jobs applied"].iloc[-1])))
    with c3:
        metric_card("Skills in profile", str(n_skills))

    st.subheader("Jobs applied vs. skills")
    long = df.melt("Month", var_name="Series", value_name="Count")
    chart = (
        alt.Chart(long)
        .mark_bar(size=16, cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Month:N", sort=MONTHS, title=None, axis=alt.Axis(labelAngle=0)),
            xOffset="Series:N",
            y=alt.Y("Count:Q", title="Count"),
            color=alt.Color(
                "Series:N",
                scale=alt.Scale(domain=["Jobs applied", "Skills"], range=["#2E86DE", "#1E9E6A"]),
                legend=alt.Legend(orient="top", title=None),
            ),
            tooltip=["Month", "Series", "Count"],
        )
        .properties(width="container", height=340)
    )
    st.altair_chart(chart)
    st.caption("Earlier months are sample data. The latest month's Skills bar follows your Profile.")

    with st.expander("➕ Update this month's jobs applied"):
        apps = st.number_input(
            "Jobs applied this month", 0, 500, int(stored["Jobs applied"].iloc[-1])
        )
        if st.button("Update chart"):
            stored.loc[stored.index[-1], "Jobs applied"] = apps
            st.session_state["progress"] = stored
            st.rerun()

    render_chat_popup()