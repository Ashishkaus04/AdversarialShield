"""Explainability (SHAP) page for AdversarialShield Dashboard."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import load_csv, CHART_LAYOUT, get_figure_path


def render():
    st.markdown('<div class="page-title">🧠 Explainability — SHAP Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Understanding model decisions and adversarial vulnerability through SHAP values</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    df_feat = load_csv("global_feature_importance.csv", subdir="explanations")
    if df_feat is None:
        st.error("Could not load SHAP feature importance data.")
        return

    # Clean column names
    df_feat.columns = [c.strip() for c in df_feat.columns]
    if 'feature' in df_feat.columns:
        df_feat['feature'] = df_feat['feature'].str.strip()

    # --- Top 15 Feature Importance Bar ---
    st.markdown('<div class="section-header">📊 Top 20 Most Important Features (SHAP)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">SHAP (SHapley Additive exPlanations) values show how much each feature contributes to the model\'s prediction. Higher values indicate greater influence on classification decisions.</div>', unsafe_allow_html=True)

    top20 = df_feat.head(20).sort_values('mean_abs_shap', ascending=True)
    colors = [f'rgba(59,130,246,{0.4 + 0.6*(i/19)})' for i in range(20)]
    fig = go.Figure(go.Bar(
        y=top20['feature'], x=top20['mean_abs_shap'],
        orientation='h', marker_color=colors,
        text=[f"{v:.3f}" for v in top20['mean_abs_shap']], textposition='outside',
        textfont=dict(size=11, color='#e2e8f0'),
    ))
    layout_kwargs = {**CHART_LAYOUT, 'margin': dict(l=200, r=80, t=50, b=40)}
    fig.update_layout(**layout_kwargs, height=600,
        title=dict(text='Mean |SHAP| Value — Feature Importance', font=dict(size=14, color='#e2e8f0')),
        xaxis=dict(title='Mean |SHAP Value|', gridcolor='rgba(148,163,184,0.1)'),
        yaxis=dict(gridcolor='rgba(148,163,184,0.1)'))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Top 5 Feature Insight Cards ---
    st.markdown('<div class="section-header">🔍 Top 5 Most Influential Features</div>', unsafe_allow_html=True)
    top5 = df_feat.head(5)
    cols = st.columns(5)
    icons = ['🔌', '📦', '🪟', '📐', '🪟']
    for i, (_, row) in enumerate(top5.iterrows()):
        with cols[i]:
            st.markdown(
                f'<div class="stat-mini" style="min-height:120px;">'
                f'<div style="font-size:1.4rem;">{icons[i]}</div>'
                f'<div class="stat-val text-blue" style="font-size:1.1rem;">{row["mean_abs_shap"]:.3f}</div>'
                f'<div class="stat-lbl" style="font-size:0.7rem;">{row["feature"]}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Vulnerability Insight ---
    st.markdown('<div class="section-header">⚠️ Adversarial Vulnerability Insights</div>', unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        st.markdown(
            '<div class="warning-box">'
            '<h4 style="color:#f59e0b;margin-top:0;">🎯 Targeted Features</h4>'
            '<p>Adversarial attacks disproportionately perturb <strong>Destination Port</strong>, '
            '<strong>Bwd Packet Length Max</strong>, and <strong>Init_Win_bytes_backward</strong> — '
            'the top-3 features by SHAP importance. This confirms that attackers exploit the model\'s '
            'most relied-upon features.</p></div>',
            unsafe_allow_html=True,
        )
    with v2:
        st.markdown(
            '<div class="success-box">'
            '<h4 style="color:#10b981;margin-top:0;">🛡️ Robust Features</h4>'
            '<p>Lower-ranked features like <strong>Active Std</strong>, <strong>Idle Std</strong>, and '
            '<strong>Fwd PSH Flags</strong> are rarely perturbed and show stable SHAP contributions '
            'across clean and adversarial samples — making them reliable signals.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- SHAP Figures ---
    st.markdown('<div class="section-header">📸 SHAP Analysis Figures</div>', unsafe_allow_html=True)

    shap_figures = [
        ("shap_summary_global.png", "Global SHAP Summary — Beeswarm plot showing feature impact on predictions"),
        ("shap_comparison_clean_vs_adversarial.png", "SHAP: Clean vs Adversarial — How adversarial perturbation shifts explanations"),
        ("shap_waterfall_clean_attack.png", "SHAP Waterfall — Clean attack sample decision breakdown"),
        ("shap_waterfall_fgsm_attack.png", "SHAP Waterfall — FGSM adversarial sample decision breakdown"),
    ]

    for fname, caption in shap_figures:
        fig_path = get_figure_path(fname)
        if fig_path:
            st.markdown(f'<div class="figure-frame">', unsafe_allow_html=True)
            st.image(fig_path, use_column_width=True)
            st.markdown(f'<div class="figure-caption">{caption}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("", unsafe_allow_html=True)

    # --- Full feature table ---
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    with st.expander("📋 Complete Feature Importance Table (41 features)"):
        df_show = df_feat.copy()
        df_show.index = range(1, len(df_show)+1)
        df_show.index.name = 'Rank'
        st.dataframe(df_show.style.background_gradient(subset=['mean_abs_shap'], cmap='Blues')
            .format({'mean_abs_shap': '{:.6f}'}), use_container_width=True)
