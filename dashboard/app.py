"""
AdversarialShield — Comprehensive Dashboard
============================================
Run with:  streamlit run app.py
"""
import streamlit as st
import sys, os

# Ensure dashboard directory is on the path so page modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

from config import CUSTOM_CSS

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AdversarialShield — ML Security Research",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ───────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:16px 0 8px 0;">'
        '<span style="font-size:2.2rem;">🛡️</span><br>'
        '<span style="font-size:1.3rem;font-weight:700;'
        'background:linear-gradient(135deg,#3b82f6,#8b5cf6);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
        'AdversarialShield</span><br>'
        '<span style="color:#64748b;font-size:0.85rem;">ML Security Research</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Home", "⚔️ Live Attack Demo", "📊 Attack Comparison", "🛡️ Defense Showcase"],
        label_visibility="collapsed",
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # Quick info
    st.markdown(
        '<div class="info-box" style="font-size:0.85rem;">'
        '<strong>About</strong><br>'
        'AdversarialShield evaluates the robustness of ML-based Intrusion Detection Systems '
        'against adversarial attacks and develops effective defenses.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Quick metrics
    st.markdown(
        '<div class="tech-card" style="padding:16px;min-height:auto;font-size:0.85rem;">'
        '<h4 style="color:#60a5fa;margin:0 0 8px 0;font-size:0.9rem;">📦 Quick Stats</h4>'
        '<table style="width:100%;color:#94a3b8;font-size:0.85rem;">'
        '<tr><td>Dataset</td><td style="text-align:right;color:#e2e8f0;">CICIDS2017</td></tr>'
        '<tr><td>Samples</td><td style="text-align:right;color:#e2e8f0;">692,703</td></tr>'
        '<tr><td>Features</td><td style="text-align:right;color:#e2e8f0;">41</td></tr>'
        '<tr><td>Model</td><td style="text-align:right;color:#e2e8f0;">XGBoost</td></tr>'
        '</table></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="text-align:center;padding:24px 0 8px 0;color:#475569;font-size:0.75rem;">'
        'BTech Minor Project<br>© 2024-2025'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Page Routing ─────────────────────────────────────────────────────────
if page == "🏠 Home":
    import pages_home
    pages_home.render()
elif page == "⚔️ Live Attack Demo":
    import pages_attack_demo
    pages_attack_demo.render()
elif page == "📊 Attack Comparison":
    import pages_comparison
    pages_comparison.render()
elif page == "🛡️ Defense Showcase":
    import pages_defense
    pages_defense.render()
