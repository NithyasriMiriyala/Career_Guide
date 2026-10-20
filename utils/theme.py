import streamlit as st
import streamlit.components.v1 as components

THEME = {
    "primary": "#2A5C8F",
    "accent": "#4A90D9",
    "bg": "#E6F0FA",
    "card": "#FFFFFF",
    "text": "#1F3347",
    "muted": "#62788C",
}


def inject_css() -> None:
    t = THEME
    st.markdown(
        f"""
        <style>
        .stApp {{ background: linear-gradient(160deg, #E3EEFA 0%, #F3F8FD 100%); color: {t['text']}; }}
        section[data-testid="stSidebar"] {{ background: {t['primary']}; }}
        section[data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}
        .cg-card {{ background: {t['card']}; border-radius: 14px; padding: 18px 20px;
                    box-shadow: 0 1px 6px rgba(20,40,70,.08); margin-bottom: 14px; }}
        .cg-metric-label {{ color: {t['muted']}; font-size: .82rem; text-transform: uppercase; }}
        .cg-metric-value {{ font-size: 1.9rem; font-weight: 700; color: {t['primary']}; }}
        .cg-chip {{ display:inline-block; padding:3px 10px; margin:2px 4px 2px 0; border-radius:999px;
                    font-size:.8rem; background:#E6F0FA; color:{t['primary']}; }}
        .cg-chip.miss {{ background:#FDF2D0; color:#7A5A00; }}
        .cg-chip.have {{ background:#DDF3E8; color:#126B47; }}
        .cg-title {{ font-weight:700; font-size:1.05rem; color:{t['text']}; }}
        .cg-sub {{ color:{t['muted']}; font-size:.9rem; }}

        [data-testid="stSidebar"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{ display: none; }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        .cg-brand {{ font-weight: 800; font-size: 1.3rem; color: {t['primary']}; padding-top: 6px; }}
        div[role="radiogroup"] {{ gap: .5rem; flex-wrap: wrap; }}
        div[role="radiogroup"] label {{ background: #FFFFFF; border-radius: 999px;
                                        padding: 6px 14px; box-shadow: 0 1px 4px rgba(20,40,70,.10); }}
        div[role="radiogroup"] label:has(input:checked) {{ background: {t['primary']}; }}
        div[role="radiogroup"] label:has(input:checked) * {{ color: #FFFFFF !important; }}

        .cg-topbar {{ position: sticky; top: 0; z-index: 999; background: {t['bg']}; padding: 8px 0; }}
        body.cg-scrolled .cg-topbar {{ position: fixed; top: 0; left: 0; bottom: 0; width: 230px;
                                    flex-direction: column; flex-wrap: nowrap; gap: 1rem;
                                    background: {t['primary']}; padding: 24px 14px; overflow-y: auto; }}
        body.cg-scrolled .cg-topbar > div {{ width: 100% !important; flex: none !important; min-width: 0 !important; }}
        body.cg-scrolled .cg-topbar .cg-brand {{ color: #FFFFFF; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] {{ flex-direction: column; align-items: stretch; }}
        body.cg-scrolled [data-testid="stMainBlockContainer"],
        body.cg-scrolled .block-container {{ margin-left: 230px; }}

        .st-key-chatpop {{ position: fixed; bottom: 24px; right: 24px; z-index: 1000; width: auto !important; }}
        .st-key-chatpop button {{ background: {t['primary']}; border: none; border-radius: 999px;
                                padding: 10px 20px; box-shadow: 0 4px 14px rgba(20,40,70,.35); }}
        .st-key-chatpop button * {{ color: #FFFFFF !important; }}
        div[data-testid="stPopoverBody"] {{ min-width: 360px; max-width: 92vw; }}

        div[role="radiogroup"] label {{ border-radius: 14px; padding: 18px 28px; min-width: 170px;
                                        justify-content: center; text-align: center;
                                        box-shadow: 0 2px 8px rgba(20,40,70,.12); }}
        div[role="radiogroup"] label > div:first-child {{ display: none; }}
        div[role="radiogroup"] label p {{ font-size: 1.05rem; font-weight: 600; margin: 0; }}

        body.cg-scrolled .cg-topbar {{ width: 150px !important; padding: 16px 8px !important; gap: .6rem !important; }}
        body.cg-scrolled .cg-topbar .cg-brand {{ font-size: .95rem; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] {{ gap: .35rem; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label {{ min-width: 0 !important; width: 100%;
                                                                    padding: 8px 10px !important; border-radius: 10px; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label p {{ font-size: .8rem !important; }}
        body.cg-scrolled .cg-topbar button {{ font-size: .8rem; padding: 4px 8px; }}
        body.cg-scrolled [data-testid="stMainBlockContainer"],
        body.cg-scrolled .block-container {{ margin-left: 0 !important; padding-left: 170px !important; }}

        body.cg-scrolled .cg-topbar {{ width: 76px !important; padding: 14px 6px !important; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label p[data-icon],
        body.cg-scrolled .cg-topbar button p[data-icon],
        body.cg-scrolled .cg-topbar .cg-brand[data-icon] {{ font-size: 0 !important; text-align: center; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label p[data-icon]::before,
        body.cg-scrolled .cg-topbar button p[data-icon]::before,
        body.cg-scrolled .cg-topbar .cg-brand[data-icon]::before {{ content: attr(data-icon); font-size: 1.5rem; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label {{ justify-content: center; padding: 8px 0 !important; }}
        body.cg-scrolled .cg-topbar button svg {{ display: none; }}
        body.cg-scrolled [data-testid="stMainBlockContainer"],
        body.cg-scrolled .block-container {{ padding-left: 96px !important; }}

        body.cg-scrolled .cg-topbar div[role="radiogroup"] label,
        body.cg-scrolled .cg-topbar button {{ background: transparent !important; box-shadow: none !important;
                                border: none !important; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label > div:first-child {{ display: none !important; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label:hover,
        body.cg-scrolled .cg-topbar button:hover {{ background: rgba(255,255,255,.15) !important; border-radius: 12px; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label:has(input:checked) {{
            background: rgba(255,255,255,.28) !important; border-radius: 12px; }}


        .cg-topbar div[role="radiogroup"] label div:not(:has(p)),
        .cg-topbar div[role="radiogroup"] label span:not(:has(p)),
        .cg-topbar div[role="radiogroup"] label input,
        .cg-topbar div[role="radiogroup"] label svg,
        .cg-topbar div[role="radiogroup"] label::before,
        .cg-topbar div[role="radiogroup"] label::after {{
            display: none !important; width: 0 !important; height: 0 !important;
            margin: 0 !important; padding: 0 !important; border: 0 !important; }}
        .cg-topbar div[role="radiogroup"] label {{ gap: 0 !important; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label {{
            justify-content: center !important; text-align: center; }}
        body.cg-scrolled .cg-topbar {{ width: 40px !important; padding: 12px 0 !important; }}
        body.cg-scrolled .cg-topbar > div {{ display: flex; justify-content: center; }}
        body.cg-scrolled .cg-topbar .cg-brand {{ text-align: center; padding: 0; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] {{
            align-items: center !important; width: 100%; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label {{
            width: 44px !important; min-width: 0 !important; margin: 0 auto !important;
            padding: 8px 0 !important; justify-content: center !important; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label > div {{
            width: 100% !important; margin: 0 !important; }}
        body.cg-scrolled .cg-topbar div[role="radiogroup"] label p {{
            text-align: center !important; width: 100%; }}
        body.cg-scrolled .cg-topbar button {{
            width: 30px !important; min-width: 0 !important; margin: 0 auto;
            padding: 8px 0 !important; justify-content: center !important; }}
        body.cg-scrolled [data-testid="stMainBlockContainer"],
        body.cg-scrolled .block-container {{ padding-left: 76px !important; }}
        div[data-baseweb="input"], div[data-baseweb="textarea"], div[data-baseweb="select"] > div {{
            background: #FFFFFF !important; border: 1.5px solid #B9D0E8 !important; border-radius: 10px !important; }}
        div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] input {{
            background: transparent !important; color: {t['text']} !important; }}
        div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {{
            border-color: {t['accent']} !important; box-shadow: 0 0 0 3px rgba(74,144,217,.20) !important; }}
        input::placeholder, textarea::placeholder {{ color: #8CA2B8 !important; }}
        [data-testid="stForm"] {{ background: rgba(255,255,255,.55); border: 1.5px solid #C9DCEE;
                                border-radius: 16px; padding: 18px; }}
        [data-testid="stWidgetLabel"] p {{ font-weight: 600; color: {t['text']}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="cg-card"><div class="cg-metric-label">{label}</div>'
        f'<div class="cg-metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def chips(items, kind: str = "") -> str:
    from html import escape
    return "".join(
        f'<span class="cg-chip {kind}">{escape(str(i))}</span>' for i in items
    ) or "<span class='cg-sub'>None</span>"


def nav_scroll_behavior() -> None:
    """Top bar becomes a slim emoji-only left bar after scrolling down."""
    components.html(
        """
        <script>
        const P = window.parent;
        const doc = P.document;
        if (P.__cgNavTimer) P.clearInterval(P.__cgNavTimer);
        const tag = (el, icon) => {
        if (!el || el.dataset.icon) return;
        const t = el.textContent.trim();
        el.dataset.icon = icon || t.split(' ')[0];
        (el.closest('label') || el).title = t;
        };
        P.__cgNavTimer = P.setInterval(() => {
        const rg = doc.querySelector('div[role="radiogroup"]');
        if (!rg) return;
        const bar = rg.closest('[data-testid="stHorizontalBlock"]');
        if (bar && !bar.classList.contains('cg-topbar')) bar.classList.add('cg-topbar');
        if (bar) {
            bar.querySelectorAll('div[role="radiogroup"] label p').forEach(p => tag(p));
            bar.querySelectorAll('button p').forEach(p => tag(p));
            tag(bar.querySelector('.cg-brand'), '🎯');
        }
        const main = doc.querySelector('[data-testid="stMain"]') || doc.querySelector('section.main');
        if (!main) return;
        const y = main.scrollTop;
        const on = doc.body.classList.contains('cg-scrolled');
        if (!on && y > 150) doc.body.classList.add('cg-scrolled');
        else if (on && y < 40) doc.body.classList.remove('cg-scrolled');
        }, 200);
        </script>
        """,
        height=0,
    )