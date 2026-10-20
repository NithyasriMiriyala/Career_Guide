import html

import streamlit as st

from utils.roadmap import topics_for
from utils.theme import THEME, metric_card

LEVELS = ["Beginner", "Intermediate", "Advanced"]
STAGE_COLOR = {"Intermediate": THEME["accent"], "Advanced": THEME["primary"]}

CSS = f"""
<style>
.cg-tl {{position:relative; margin:6px 0 10px 22px; padding-left:34px;
        border-left:4px solid #BBD3EC;}}
.cg-node {{position:relative; margin:22px 0 10px 0;}}
.cg-dot {{position:absolute; left:-54px; top:-4px; width:36px; height:36px;
        border-radius:50%; background:#fff; border:3px solid {THEME["accent"]};
        display:flex; align-items:center; justify-content:center; font-size:18px;}}
.cg-stage {{font-weight:700; font-size:1.15rem; color:{THEME["primary"]};}}
.cg-sub {{color:{THEME["muted"]}; font-size:.9rem; margin-top:2px;}}
.cg-topic {{background:{THEME["card"]}; border:1px solid #CFE0F2; border-radius:12px;
        padding:12px 16px; margin:10px 0; box-shadow:0 1px 3px rgba(42,92,143,.08);}}
.cg-topic h5 {{margin:0 0 6px 0; font-size:1rem; color:{THEME["text"]};}}
.cg-num {{display:inline-block; min-width:24px; height:24px; line-height:24px;
        text-align:center; border-radius:50%; color:#fff; font-size:.8rem;
        margin-right:8px;}}
.cg-topic ul {{margin:0; padding-left:22px; color:{THEME["text"]};}}
.cg-topic li {{margin:2px 0;}}
.cg-start .cg-dot {{border-color:#2E9E6B;}}
.cg-end .cg-dot {{border-color:#E0A526;}}
</style>
"""


def _e(x) -> str:
    return html.escape(str(x))


def _timeline(skill: str, cur: str, tgt: str) -> str:
    """Build one top-to-bottom roadmap: you are here -> stages -> goal."""
    out = ['<div class="cg-tl">']
    out.append(f'<div class="cg-node cg-start"><span class="cg-dot">📍</span>'
            f'<div class="cg-stage">You are here · {_e(cur)}</div></div>')

    step = 0
    for lv in LEVELS[LEVELS.index(cur) + 1: LEVELS.index(tgt) + 1]:
        prev = LEVELS[LEVELS.index(lv) - 1]
        topics = topics_for(skill, lv)
        color = STAGE_COLOR.get(lv, THEME["accent"])
        out.append(f'<div class="cg-node"><span class="cg-dot" style="border-color:{color}">'
                f'{LEVELS.index(lv)}</span>'
                f'<div class="cg-stage">{_e(prev)} → {_e(lv)}</div>'
                f'<div class="cg-sub">{len(topics)} topics to cover</div></div>')
        for topic, subs in topics.items():
            step += 1
            items = "".join(f"<li>{_e(s)}</li>" for s in subs)
            out.append(f'<div class="cg-topic"><h5><span class="cg-num" '
                    f'style="background:{color}">{step}</span>{_e(topic)}</h5>'
                    f'<ul>{items}</ul></div>')

    out.append(f'<div class="cg-node cg-end"><span class="cg-dot">🎯</span>'
            f'<div class="cg-stage">Goal reached · {_e(tgt)}</div></div>')
    out.append("</div>")
    return "".join(out)  # one line: no blank lines, so markdown never breaks the HTML


def render(profile: dict) -> None:
    st.title("🗺️ Learning Roadmap")
    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    if not skills:
        st.info("Add your skills and levels in **👤 Profile** (top right) first.")
        return

    levels = profile.get("levels", {})
    targets = st.session_state.get("targets", {})

    plan = []
    for s in skills:
        cur = levels.get(s, "Beginner")
        tgt = targets.get(s, "Advanced")
        if LEVELS.index(tgt) > LEVELS.index(cur):
            plan.append((s, cur, tgt))

    if not plan:
        st.success("🎉 You've reached your target level in every skill. "
                   "Raise a target on the **🧩 Skill Gap** page to get a new roadmap.")
        return

    a, b = st.columns(2)
    with a:
        metric_card("Skills to improve", str(len(plan)))
    with b:
        total = sum(len(topics_for(s, lv)) for s, c, t in plan
                    for lv in LEVELS[LEVELS.index(c) + 1: LEVELS.index(t) + 1])
        metric_card("Topics to learn", str(total))

    st.caption("Follow each path from top to bottom. Targets come from the "
        "**🧩 Skill Gap** page, and only the levels you still need are shown.")

    pick = st.selectbox("Show roadmap for", ["All skills"] + [p[0] for p in plan])
    st.markdown(CSS, unsafe_allow_html=True)

    for skill, cur, tgt in plan:
        if pick != "All skills" and pick != skill:
            continue
        with st.container(border=True):
            st.markdown(f"## {skill}  ·  {cur} → {tgt}")
            st.markdown(_timeline(skill, cur, tgt), unsafe_allow_html=True)