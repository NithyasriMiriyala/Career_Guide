import streamlit as st

from utils import api
from utils.theme import metric_card

LEVELS = ["Beginner", "Intermediate", "Advanced"]
ICONS = {"Beginner": "🌱", "Intermediate": "🌿", "Advanced": "🌳"}


def _completed(uid) -> set:
    """Skills the user has ticked as completed (loaded once from the backend)."""
    if "completed_skills" not in st.session_state and uid:
        try:
            st.session_state["completed_skills"] = set(api.get_skill_progress(uid).get("completed", []))
        except Exception:
            return set()  # backend unreachable: don't cache the failure
    return st.session_state.get("completed_skills", set())


def _toggle(uid: str, skill: str) -> None:
    """Runs when a tick box is clicked: save to the backend."""
    done = st.session_state[f"done_{skill}"]
    try:
        res = api.set_skill_done(uid, skill, done)
        st.session_state["completed_skills"] = set(res.get("completed", []))
        st.session_state["tick_flash"] = (
            f"{skill} marked as completed ✅" if done else f"{skill} unmarked")
    except Exception:
        st.session_state["tick_flash"] = "Could not save: the backend isn't reachable."


def render(profile: dict) -> None:
    st.title("🧩 Skill Gap")
    msg = st.session_state.pop("tick_flash", None)
    if msg:
        st.toast(msg)

    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    if not skills:
        st.info("Add your skills and levels in **👤 Profile** (top right) first.")
        return

    uid = st.session_state.get("uid")
    levels = profile.get("levels", {})
    targets = st.session_state.setdefault("targets", {})
    completed = _completed(uid)

    st.caption("Choose the level you want to reach for each skill. Tick **Completed** when you "
            "have finished learning it. Completed skills count on your Home graph.")
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
                    pct = round(100 * (ci + 1) / (ti + 1))
                    st.progress((ci + 1) / (ti + 1), text=f"{pct}% of the way to {target}")
                    st.caption(" → ".join(
                        f"**{ICONS[l]} {l}**" if l == current else f"{ICONS[l]} {l}"
                        for l in LEVELS[: ti + 1]))
                    st.warning(f"📈 {ti - ci} level(s) to go: {current} → {target}")
                else:
                    st.progress(1.0)
                    st.success("✅ Target reached")

                st.checkbox(
                    "✅ I've completed this skill",
                    value=skill in completed,
                    key=f"done_{skill}",
                    on_change=_toggle,
                    args=(uid, skill),
                    disabled=not uid,
                )

    done_count = len([s for s in skills if s in _completed(uid)])
    with summary:
        a, b, c, d = st.columns(4)
        with a:
            metric_card("Skills I know", str(len(skills)))
        with b:
            metric_card("Skills to improve", str(to_improve))
        with c:
            metric_card("Targets reached", str(len(skills) - to_improve))
        with d:
            metric_card("Skills completed", f"{done_count} / {len(skills)}")