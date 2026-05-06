"""Attack Comparison page for AdversarialShield Dashboard."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import DEMO_DATA, CHART_LAYOUT


def render():
    st.markdown('<div class="page-title">📊 Attack Comparison Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Comprehensive comparison of all implemented adversarial attacks</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Comparison Table ---
    st.markdown("### 📋 Attack Performance Summary")
    df = pd.DataFrame({
        'Attack': ['Baseline', 'FGSM', 'PGD', 'C&W'],
        'Accuracy (%)': [99.98, 62.97, 63.64, 60.32],
        'Drop (pp)': [0, 37.01, 36.34, 39.66],
        'L2 Norm': [0, 1.778, 0.737, 3.745],
        'Time (s)': [0, 0.05, 0.5, 5.0],
    })
    st.dataframe(
        df.style.background_gradient(subset=['Accuracy (%)'], cmap='RdYlGn')
              .background_gradient(subset=['Drop (pp)'], cmap='OrRd')
              .background_gradient(subset=['L2 Norm'], cmap='YlOrRd')
              .format({'Accuracy (%)': '{:.2f}', 'Drop (pp)': '{:.2f}', 'L2 Norm': '{:.3f}', 'Time (s)': '{:.2f}'}),
        use_container_width=True, hide_index=True,
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Bar Charts ---
    c1, c2 = st.columns(2)
    attacks = ['Baseline', 'FGSM', 'PGD', 'C&W']
    accs = [99.98, 62.97, 63.64, 60.32]
    colors_acc = ['#10b981', '#f59e0b', '#f59e0b', '#ef4444']

    with c1:
        fig1 = go.Figure(go.Bar(
            x=attacks, y=accs, marker_color=colors_acc,
            text=[f"{a}%" for a in accs], textposition='outside',
            textfont=dict(size=12, color='#e2e8f0'),
        ))
        fig1.update_layout(
            **CHART_LAYOUT,
            title=dict(text='Accuracy Comparison', font=dict(size=15, color='#e2e8f0')),
            yaxis=dict(title='Accuracy (%)', range=[0, 115], gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)'), height=380,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        atk_names = ['FGSM', 'PGD', 'C&W']
        l2s = [1.778, 0.737, 3.745]
        colors_l2 = ['#f59e0b', '#10b981', '#ef4444']
        fig2 = go.Figure(go.Bar(
            x=atk_names, y=l2s, marker_color=colors_l2,
            text=[f"{v:.3f}" for v in l2s], textposition='outside',
            textfont=dict(size=12, color='#e2e8f0'),
        ))
        fig2.update_layout(
            **CHART_LAYOUT,
            title=dict(text='L2 Norm Comparison (Stealth)', font=dict(size=15, color='#e2e8f0')),
            yaxis=dict(title='L2 Norm', gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)'), height=380,
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Scatter: Effectiveness vs Stealth ---
    st.markdown("### 🎯 Effectiveness vs Stealth Trade-off")
    fig3 = go.Figure()
    scatter_attacks = ['FGSM', 'PGD', 'C&W']
    scatter_acc = [62.97, 63.64, 60.32]
    scatter_l2 = [1.778, 0.737, 3.745]
    scatter_colors = ['#f59e0b', '#3b82f6', '#ef4444']
    scatter_sizes = [40, 40, 50]

    for i, atk in enumerate(scatter_attacks):
        fig3.add_trace(go.Scatter(
            x=[scatter_l2[i]], y=[scatter_acc[i]], mode='markers+text',
            marker=dict(size=scatter_sizes[i], color=scatter_colors[i], line=dict(width=2, color='#e2e8f0')),
            text=[atk], textposition='top center', textfont=dict(size=14, color='#e2e8f0'),
            name=atk, showlegend=True,
        ))

    fig3.add_annotation(x=0.5, y=58, text="← Lower accuracy + Lower L2 = Best attack →",
                        showarrow=False, font=dict(size=12, color='#64748b'))
    fig3.update_layout(
        **CHART_LAYOUT,
        title=dict(text='Attack Effectiveness vs Stealth', font=dict(size=15, color='#e2e8f0')),
        xaxis=dict(title='L2 Norm (Perturbation Size)', gridcolor='rgba(148,163,184,0.1)'),
        yaxis=dict(title='Accuracy (%) — Lower = More Effective', gridcolor='rgba(148,163,184,0.1)'),
        height=420,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Key Insights ---
    st.markdown("### 💡 Key Insights")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(
            '<div class="insight-card">'
            '<h4>🎯 Most Effective</h4>'
            '<div class="insight-value text-red">C&W</div>'
            '<div class="insight-detail">60.32% accuracy (−39.66 pp)</div>'
            '</div>', unsafe_allow_html=True,
        )
    with i2:
        st.markdown(
            '<div class="insight-card">'
            '<h4>🥷 Most Stealthy</h4>'
            '<div class="insight-value text-blue">PGD</div>'
            '<div class="insight-detail">L2 Norm: 0.737</div>'
            '</div>', unsafe_allow_html=True,
        )
    with i3:
        st.markdown(
            '<div class="insight-card">'
            '<h4>⚡ Fastest</h4>'
            '<div class="insight-value text-orange">FGSM</div>'
            '<div class="insight-detail">0.05 s per sample</div>'
            '</div>', unsafe_allow_html=True,
        )
