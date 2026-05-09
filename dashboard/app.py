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
        [
            "🏠 Home",
            "📊 Model Comparison",
            # "⚔️ Live Attack Demo",  # Hidden — kept for future use
            "📈 Attack Comparison",
            "🔀 Transfer Attacks",
            "🛡️ Defense Showcase",
            "🔬 Advanced Analysis",
            "🧠 Explainability",
            "🖼️ Results Gallery",
        ],
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
        '<tr><td>Samples</td><td style="text-align:right;color:#e2e8f0;">1,039,866</td></tr>'
        '<tr><td>Features</td><td style="text-align:right;color:#e2e8f0;">41</td></tr>'
        '<tr><td>Model</td><td style="text-align:right;color:#e2e8f0;">XGBoost</td></tr>'
        '<tr><td>Notebooks</td><td style="text-align:right;color:#e2e8f0;">16</td></tr>'
        '<tr><td>Figures</td><td style="text-align:right;color:#e2e8f0;">28</td></tr>'
        '</table></div>',
        unsafe_allow_html=True,
    )

    # Notebooks list
    with st.expander("📓 Research Notebooks"):
        notebooks = [
            "01 Data Exploration", "02 Data Preprocessing",
            "03 Baseline Classifier", "03a Model Comparison",
            "04 FGSM Attack", "05 PGD Attack", "06 C&W Attack",
            "07 Cross-Model Transfer", "08 Adversarial Training",
            "09 Additional Defenses", "10 Adaptive Attacks",
            "11 Threat Map Viz", "12 Backdoor Attack",
            "13 SHAP Explainability", "14 Certified Robustness",
            "15 Continual Defense",
        ]
        for nb in notebooks:
            st.markdown(f"<span style='color:#94a3b8;font-size:0.8rem;'>▸ {nb}</span>", unsafe_allow_html=True)

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
elif page == "📊 Model Comparison":
    import pages_model_comparison
    pages_model_comparison.render()
# Hidden — kept for future use
# elif page == "⚔️ Live Attack Demo":
#     import pages_attack_demo
#     pages_attack_demo.render()
elif page == "📈 Attack Comparison":
    import pages_comparison
    pages_comparison.render()
elif page == "🔀 Transfer Attacks":
    import pages_transfer
    pages_transfer.render()
elif page == "🛡️ Defense Showcase":
    import pages_defense
    pages_defense.render()
elif page == "🔬 Advanced Analysis":
    import pages_advanced
    pages_advanced.render()
elif page == "🧠 Explainability":
    import pages_explainability
    pages_explainability.render()
elif page == "🖼️ Results Gallery":
    import pages_gallery
    pages_gallery.render()
