"""Model Comparison page — shows baseline model benchmarking results."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from config import load_csv, CHART_LAYOUT, MODEL_COLORS, get_figure_path


def render():
    st.markdown('<div class="page-title">📊 Model Comparison</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Benchmarking ML classifiers to justify XGBoost selection for the IDS</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Load real data ---
    df = load_csv("baseline_model_comparison.csv", subdir="results")
    if df is None:
        st.error("Could not load baseline_model_comparison.csv")
        return

    df = df.sort_values("Rank").reset_index(drop=True)

    # --- Hero metric cards ---
    best = df.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Best Model</div>'
            f'<div class="metric-value text-blue">{best["Model"]}</div>'
            f'<div class="metric-delta text-green">Rank #1</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Accuracy</div>'
            f'<div class="metric-value text-green">{best["Accuracy"]*100:.2f}%</div>'
            f'<div class="metric-delta text-green">● Near-perfect</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">F1-Score</div>'
            f'<div class="metric-value text-purple">{best["F1-Score"]*100:.2f}%</div>'
            f'<div class="metric-delta text-green">Balanced precision/recall</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Inference Time</div>'
            f'<div class="metric-value text-cyan">{best["Inference Time (s)"]:.2f}s</div>'
            f'<div class="metric-delta text-green">⚡ Fast</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Full comparison table ---
    st.markdown('<div class="section-header">📋 Complete Benchmark Table</div>', unsafe_allow_html=True)
    display_df = df[['Rank', 'Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC',
                      'Train Time (s)', 'Inference Time (s)']].copy()
    for col in ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']:
        display_df[col] = display_df[col] * 100

    st.dataframe(
        display_df.style
        .background_gradient(subset=['Accuracy'], cmap='RdYlGn', vmin=90, vmax=100)
        .background_gradient(subset=['F1-Score'], cmap='RdYlGn', vmin=90, vmax=100)
        .background_gradient(subset=['Inference Time (s)'], cmap='RdYlGn_r')
        .format({
            'Accuracy': '{:.4f}%', 'Precision': '{:.4f}%', 'Recall': '{:.4f}%',
            'F1-Score': '{:.4f}%', 'ROC-AUC': '{:.6f}%',
            'Train Time (s)': '{:.2f}', 'Inference Time (s)': '{:.3f}',
        }),
        use_container_width=True, hide_index=True,
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Charts ---
    col1, col2 = st.columns(2)

    with col1:
        # Grouped bar: Accuracy, Precision, Recall, F1
        fig1 = go.Figure()
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        bar_colors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b']
        for i, m in enumerate(metrics):
            fig1.add_trace(go.Bar(
                name=m, x=df['Model'], y=df[m] * 100,
                marker_color=bar_colors[i], opacity=0.88,
            ))
        fig1.update_layout(
            **CHART_LAYOUT, barmode='group',
            title=dict(text='Classification Metrics by Model', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Score (%)', range=[95, 100.5], gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)', tickangle=-20),
            legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'),
            height=440,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Radar chart for top 3 models
        top3 = df.head(3)
        categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        fig2 = go.Figure()
        radar_colors = ['#3b82f6', '#10b981', '#8b5cf6']
        for idx, row in top3.iterrows():
            vals = [row[c] * 100 for c in categories] + [row[categories[0]] * 100]
            fig2.add_trace(go.Scatterpolar(
                r=vals, theta=categories + [categories[0]],
                fill='toself', name=row['Model'],
                line=dict(color=radar_colors[idx], width=2),
                fillcolor=f'rgba({",".join(str(int(radar_colors[idx][i:i+2], 16)) for i in (1,3,5))},0.1)',
            ))
        fig2.update_layout(
            **CHART_LAYOUT,
            polar=dict(
                radialaxis=dict(visible=True, range=[99, 100.1], gridcolor='rgba(148,163,184,0.15)'),
                bgcolor='rgba(0,0,0,0)',
            ),
            title=dict(text='Top-3 Models — Radar Comparison', font=dict(size=14, color='#e2e8f0')),
            legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'),
            height=440,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Timing comparison ---
    col3, col4 = st.columns(2)
    with col3:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name='Train Time', x=df['Model'], y=df['Train Time (s)'],
            marker_color='#f59e0b', opacity=0.85,
        ))
        fig3.update_layout(
            **CHART_LAYOUT,
            title=dict(text='Training Time', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Time (s)', gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(tickangle=-20, gridcolor='rgba(148,163,184,0.1)'),
            height=380,
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name='Inference Time', x=df['Model'], y=df['Inference Time (s)'],
            marker_color='#06b6d4', opacity=0.85,
            text=[f"{v:.3f}s" for v in df['Inference Time (s)']], textposition='outside',
            textfont=dict(size=11, color='#e2e8f0'),
        ))
        fig4.update_layout(
            **CHART_LAYOUT,
            title=dict(text='Inference Time (lower = better)', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Time (s)', gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(tickangle=-20, gridcolor='rgba(148,163,184,0.1)'),
            height=380,
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Justification ---
    st.markdown('<div class="section-header">🏆 Why XGBoost?</div>', unsafe_allow_html=True)
    j1, j2, j3 = st.columns(3)
    with j1:
        st.markdown(
            '<div class="success-box">'
            '<h4 style="color:#10b981;margin-top:0;">✅ Highest Accuracy</h4>'
            '<p>XGBoost achieves <strong>99.98%</strong> accuracy — the highest among all evaluated models, '
            'with near-perfect precision and recall.</p></div>',
            unsafe_allow_html=True,
        )
    with j2:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="color:#60a5fa;margin-top:0;">⚡ Fast Inference</h4>'
            '<p>At <strong>0.37s</strong> for the full test set, XGBoost is fast enough for '
            'real-time IDS deployment, unlike Gradient Boosting (1.15s).</p></div>',
            unsafe_allow_html=True,
        )
    with j3:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="color:#60a5fa;margin-top:0;">🎯 Best Trade-off</h4>'
            '<p>XGBoost balances accuracy, speed, and robustness better than any alternative. '
            'It trains in <strong>16s</strong> vs 1305s for Gradient Boosting.</p></div>',
            unsafe_allow_html=True,
        )

    # --- Embed figure if available ---
    fig_path = get_figure_path("baseline_model_comparison.png")
    if fig_path:
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📸 Generated Comparison Figure</div>', unsafe_allow_html=True)
        st.image(fig_path, use_column_width=True)
