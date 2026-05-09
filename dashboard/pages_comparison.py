"""Attack Comparison page for AdversarialShield Dashboard."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import load_csv, CHART_LAYOUT, get_figure_path


def render():
    st.markdown('<div class="page-title">📈 Attack Comparison Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Comprehensive comparison of all implemented adversarial attacks</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Load real data ---
    df_cw = load_csv("attack_comparison_with_cw.csv")
    df_detail = load_csv("attack_comparison.csv")

    if df_cw is not None:
        attacks = ['Baseline'] + df_cw['Attack'].tolist()
        accs = [99.98] + (df_cw['Accuracy'] * 100).tolist()
        drops = [0] + (df_cw['Accuracy Drop'] * 100).tolist()
        l2s_raw = df_cw['Avg L2 Perturbation'].tolist()
    else:
        attacks = ['Baseline', 'FGSM', 'PGD', 'C&W']
        accs = [99.98, 62.97, 63.64, 60.32]
        drops = [0, 37.01, 36.34, 39.66]
        l2s_raw = [1.778, 0.737, 3.745]

    # --- Comparison Table ---
    st.markdown('<div class="section-header">📋 Attack Performance Summary</div>', unsafe_allow_html=True)
    table_df = pd.DataFrame({
        'Attack': attacks,
        'Accuracy (%)': accs,
        'Drop (pp)': drops,
        'L2 Norm': [0] + l2s_raw,
    })
    st.dataframe(
        table_df.style
        .background_gradient(subset=['Accuracy (%)'], cmap='RdYlGn')
        .background_gradient(subset=['Drop (pp)'], cmap='OrRd')
        .background_gradient(subset=['L2 Norm'], cmap='YlOrRd')
        .format({'Accuracy (%)': '{:.2f}', 'Drop (pp)': '{:.2f}', 'L2 Norm': '{:.3f}'}),
        use_container_width=True, hide_index=True,
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Bar Charts ---
    c1, c2 = st.columns(2)
    colors_acc = ['#10b981'] + ['#f59e0b' if a > 62 else '#ef4444' for a in accs[1:]]

    with c1:
        fig1 = go.Figure(go.Bar(
            x=attacks, y=accs, marker_color=colors_acc,
            text=[f"{a:.2f}%" for a in accs], textposition='outside',
            textfont=dict(size=12, color='#e2e8f0'),
        ))
        fig1.update_layout(**CHART_LAYOUT, height=380,
            title=dict(text='Accuracy Comparison', font=dict(size=15, color='#e2e8f0')),
            yaxis=dict(title='Accuracy (%)', range=[0, 115], gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)'))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        atk_names = attacks[1:]
        colors_l2 = ['#f59e0b', '#10b981', '#ef4444']
        fig2 = go.Figure(go.Bar(
            x=atk_names, y=l2s_raw, marker_color=colors_l2,
            text=[f"{v:.3f}" for v in l2s_raw], textposition='outside',
            textfont=dict(size=12, color='#e2e8f0'),
        ))
        fig2.update_layout(**CHART_LAYOUT, height=380,
            title=dict(text='L2 Norm Comparison (Stealth)', font=dict(size=15, color='#e2e8f0')),
            yaxis=dict(title='L2 Norm', gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)'))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Scatter: Effectiveness vs Stealth ---
    st.markdown('<div class="section-header">🎯 Effectiveness vs Stealth Trade-off</div>', unsafe_allow_html=True)
    scatter_attacks = attacks[1:]
    scatter_acc = accs[1:]
    scatter_colors = ['#f59e0b', '#3b82f6', '#ef4444']

    fig3 = go.Figure()
    for i, atk in enumerate(scatter_attacks):
        fig3.add_trace(go.Scatter(
            x=[l2s_raw[i]], y=[scatter_acc[i]], mode='markers+text',
            marker=dict(size=45, color=scatter_colors[i], line=dict(width=2, color='#e2e8f0')),
            text=[atk], textposition='top center', textfont=dict(size=14, color='#e2e8f0'),
            name=atk, showlegend=True,
        ))
    fig3.add_annotation(x=2.0, y=58, text="← Lower accuracy + Lower L2 = Best attack →",
                        showarrow=False, font=dict(size=12, color='#64748b'))
    fig3.update_layout(**CHART_LAYOUT, height=420,
        title=dict(text='Attack Effectiveness vs Stealth', font=dict(size=15, color='#e2e8f0')),
        xaxis=dict(title='L2 Norm (Perturbation Size)', gridcolor='rgba(148,163,184,0.1)'),
        yaxis=dict(title='Accuracy (%) — Lower = More Effective', gridcolor='rgba(148,163,184,0.1)'))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Confusion matrix detail (if available) ---
    if df_detail is not None and len(df_detail) > 1:
        st.markdown('<div class="section-header">🔢 Confusion Matrix Breakdown</div>', unsafe_allow_html=True)
        cols_detail = st.columns(len(df_detail))
        for i, (_, row) in enumerate(df_detail.iterrows()):
            with cols_detail[i]:
                atk_name = row.get('Attack Type', row.get('Attack', 'Unknown'))
                tn = int(row.get('True Negatives', 0))
                fp = int(row.get('False Positives', 0))
                fn = int(row.get('False Negatives', 0))
                tp = int(row.get('True Positives', 0))
                st.markdown(
                    f'<div class="stat-mini" style="min-height:160px;">'
                    f'<div class="stat-lbl" style="font-size:0.9rem;color:#e2e8f0;margin-bottom:8px;">{atk_name}</div>'
                    f'<table style="width:100%;font-size:0.8rem;color:#94a3b8;text-align:center;">'
                    f'<tr><td style="color:#10b981;">TN: {tn:,}</td><td style="color:#ef4444;">FP: {fp:,}</td></tr>'
                    f'<tr><td style="color:#f59e0b;">FN: {fn:,}</td><td style="color:#3b82f6;">TP: {tp:,}</td></tr>'
                    f'</table></div>',
                    unsafe_allow_html=True,
                )
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Embed figure ---
    fig_path = get_figure_path("attack_comparison_confusion_matrices.png")
    if fig_path:
        st.markdown('<div class="section-header">📸 Confusion Matrix Visualization</div>', unsafe_allow_html=True)
        st.image(fig_path, use_column_width=True)
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Key Insights ---
    st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown('<div class="insight-card"><h4>🎯 Most Effective</h4><div class="insight-value text-red">C&W</div><div class="insight-detail">60.32% accuracy (−39.66 pp)</div></div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div class="insight-card"><h4>🥷 Most Stealthy</h4><div class="insight-value text-blue">PGD</div><div class="insight-detail">L2 Norm: 0.737</div></div>', unsafe_allow_html=True)
    with i3:
        st.markdown('<div class="insight-card"><h4>⚡ Fastest</h4><div class="insight-value text-orange">FGSM</div><div class="insight-detail">0.05 s per sample</div></div>', unsafe_allow_html=True)
