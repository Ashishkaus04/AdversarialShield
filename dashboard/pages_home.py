"""Home / Overview page for AdversarialShield Dashboard."""
import streamlit as st
import plotly.graph_objects as go
from config import DEMO_DATA, CHART_LAYOUT


def render():
    # --- Header ---
    st.markdown('<div class="page-title">🛡️ AdversarialShield</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Comprehensive Adversarial Robustness Evaluation Framework for Network Intrusion Detection Systems</div>', unsafe_allow_html=True)
    st.markdown(
        '<span class="badge badge-blue">BTech Minor Project</span>'
        '<span class="badge badge-purple">Adversarial ML</span>'
        '<span class="badge badge-green">CICIDS2017</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Key Metrics ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">Baseline Accuracy</div>'
            '<div class="metric-value text-blue">99.98%</div>'
            '<div class="metric-delta text-green">● Best-in-class</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">Under C&W Attack</div>'
            '<div class="metric-value text-red">60.32%</div>'
            '<div class="metric-delta text-red">↓ 39.66 pp</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">Defense Recovery</div>'
            '<div class="metric-value text-green">99.97%</div>'
            '<div class="metric-delta text-green">↑ 37 pp recovery</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            '<div class="metric-card"><div class="metric-label">Test Samples</div>'
            '<div class="metric-value text-purple">138,541</div>'
            '<div class="metric-delta" style="color:#64748b">CICIDS2017</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Project Overview ---
    st.markdown("### 📋 Project Overview")
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(
            '<div class="info-box">'
            '<strong>AdversarialShield</strong> demonstrates that while ML-based IDS achieve near-perfect '
            'accuracy (99.98%), they exhibit critical vulnerabilities to adversarial attacks, dropping to '
            'as low as 60% accuracy. The project implements comprehensive defenses that recover accuracy to 99.97%.'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Key Contributions:**")
        st.markdown(
            "- 🔬 **Comprehensive Attack Suite** — FGSM, PGD, C&W, Backdoors\n"
            "- 🛡️ **Rigorous Defense Evaluation** — Adversarial training, ensemble methods\n"
            "- ✅ **Gold-Standard Testing** — Adaptive attacks, certified robustness\n"
            "- 🔍 **Explainability** — SHAP analysis for vulnerability detection\n"
            "- 🚀 **Practical Deployment** — Continual learning framework"
        )

    with right:
        attacks = ['Baseline', 'FGSM', 'PGD', 'C&W']
        accs = [99.98, 62.97, 63.64, 60.32]
        colors = ['#10b981', '#f59e0b', '#f59e0b', '#ef4444']
        fig = go.Figure(go.Bar(x=attacks, y=accs, marker_color=colors, text=[f"{a}%" for a in accs], textposition='outside', textfont=dict(size=13, color='#e2e8f0')))
        fig.update_layout(**CHART_LAYOUT, title=dict(text='Attack Effectiveness', font=dict(size=16, color='#e2e8f0')), yaxis=dict(title='Accuracy (%)', range=[0, 115], gridcolor='rgba(148,163,184,0.1)'), xaxis=dict(gridcolor='rgba(148,163,184,0.1)'), height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Technical Stack ---
    st.markdown("### 🔧 Technical Stack")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown(
            '<div class="tech-card"><h3>🤖 Machine Learning</h3><ul>'
            '<li>XGBoost (Primary Model)</li><li>Random Forest</li>'
            '<li>Neural Networks (PyTorch)</li><li>Ensemble Methods</li></ul></div>',
            unsafe_allow_html=True,
        )
    with t2:
        st.markdown(
            '<div class="tech-card"><h3>⚔️ Attack Techniques</h3><ul>'
            '<li>FGSM (Fast Gradient Sign)</li><li>PGD (Projected Gradient Descent)</li>'
            '<li>C&W (Carlini & Wagner)</li><li>Backdoor / Trojan Attacks</li></ul></div>',
            unsafe_allow_html=True,
        )
    with t3:
        st.markdown(
            '<div class="tech-card"><h3>🛡️ Defense Mechanisms</h3><ul>'
            '<li>Adversarial Training</li><li>Feature Squeezing</li>'
            '<li>Ensemble Defense</li><li>Certified Robustness</li></ul></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Dataset Info ---
    st.markdown("### 📦 Dataset Information")
    dl, dr = st.columns([1.2, 1])
    with dl:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="margin-top:0;color:#60a5fa;">CICIDS2017 Dataset</h4>'
            '<table style="width:100%;color:#cbd5e1;">'
            '<tr><td><strong>Total Flows</strong></td><td>692,703</td></tr>'
            '<tr><td><strong>Features</strong></td><td>41 (after preprocessing)</td></tr>'
            '<tr><td><strong>Classes</strong></td><td>BENIGN vs ATTACK</td></tr>'
            '<tr><td><strong>Attack Types</strong></td><td>DoS, Heartbleed, Web attacks, Brute Force, Infiltration</td></tr>'
            '</table></div>',
            unsafe_allow_html=True,
        )
    with dr:
        fig2 = go.Figure(go.Pie(
            labels=['BENIGN', 'ATTACK'], values=[63.5, 36.5],
            marker=dict(colors=['#3b82f6', '#ef4444'], line=dict(color='#1e293b', width=3)),
            textinfo='label+percent', textfont=dict(size=14, color='#e2e8f0'),
            hole=0.45,
        ))
        fig2.update_layout(**CHART_LAYOUT, title=dict(text='Class Distribution', font=dict(size=14, color='#e2e8f0')), height=300, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
