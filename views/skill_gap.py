import streamlit as st

from utils.theme import metric_card

LEVELS = ["Beginner", "Intermediate", "Advanced"]
ICONS = {"Beginner": "🌱", "Intermediate": "🌿", "Advanced": "🌳"}


def render(profile: dict) -> None:
    st.title("🧩 Skill Gap")
    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    if not skills:
        st.info("Add your skills and levels in **👤 Profile** (top right) first.")
        return

    levels = profile.get("levels", {})
    targets = st.session_state.setdefault("targets", {})

    st.caption("Choose the level you want to reach for each skill. "
               "The gap is the distance between where you are and where you want to be.")
    summary = st.container()  # filled after the boxes are drawn, but shown at the top

    to_improve = 0
    cols = st.columns(2)
    for i, skill in enumerate(skills):
        current = levels.get(skill, "Beginner")
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"### {skill}")
                st.markdown(f"You know: {ICONS[current]} **{current}**")
                target = st.selectbox(
                    "I want to reach", LEVELS,
                    index=LEVELS.index(targets.get(skill, "Advanced")),
                    key=f"tgt_{skill}",
                )
                targets[skill] = target  # remembered for the Roadmap page

                ci, ti = LEVELS.index(current), LEVELS.index(target)
                if ti > ci:
                    to_improve += 1
                    st.progress((ci + 1) / (ti + 1))
                    st.warning(f"📈 {ti - ci} level(s) to go: {current} → {target}")
                else:
                    st.progress(1.0)
                    st.success("✅ Target reached")

    with summary:
        a, b, c = st.columns(3)
        with a:
            metric_card("Skills I know", str(len(skills)))
        with b:
            metric_card("Skills to improve", str(to_improve))
        with c:
            metric_card("Targets reached", str(len(skills) - to_improve))