from html import escape

import streamlit as st

from utils.local_matcher import match_roles
from utils.theme import chips


def render(profile: dict) -> None:
    st.title("💼 Role Recommendations")
    skills = profile.get("skills", []) + profile.get("extra_skills", [])
    if not skills:
        st.info("Add your skills in **👤 Profile** (top right) to see the roles that match you best.")
        return

    st.caption(f"Based on your {len(skills)} skills")
    cols = st.columns(2)
    for i, r in enumerate(match_roles(skills)):
        badge = '<span class="cg-chip have">⭐ Best match</span>' if i == 0 else ""
        card = f"""
        <div class="cg-card" style="min-height: 290px;">
        <div class="cg-title" style="font-size:1.25rem;">{escape(r['role'])} {badge}</div>
        <div class="cg-sub" style="margin-bottom:12px;">{escape(r['description'])}</div>
        <div style="font-size:2rem;font-weight:700;color:#1F4E79;">{r['score']}%
            <span class="cg-sub" style="font-size:.9rem;font-weight:400;">match</span></div>
        <div style="background:#E6EEF7;border-radius:999px;height:10px;margin:8px 0 14px;">
            <div style="width:{r['score']}%;background:#2E86DE;height:10px;border-radius:999px;"></div>
        </div>
        <div class="cg-sub">You have</div>{chips(r['matched'], 'have')}
        <div class="cg-sub" style="margin-top:8px;">To learn</div>{chips(r['missing'], 'miss')}
        </div>
        """
        with cols[i % 2]:
            st.markdown(card, unsafe_allow_html=True)