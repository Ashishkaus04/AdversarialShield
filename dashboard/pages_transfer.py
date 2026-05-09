"""Cross-Model Transfer Attack Analysis page."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import load_csv, CHART_LAYOUT, get_figure_path


def render():
    st.markdown('<div class="page-title">🔀 Transfer Attack Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">How well do adversarial examples transfer across different ML models?</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    df_transfer = load_csv("cross_model_transfer.csv")
    df_matrix = load_csv("transfer_success_matrix.csv")
    if df_transfer is None or df_matrix is None:
        st.error("Could not load transfer attack data.")
        return

    # --- Key Insight Cards ---
    avg_by_attack = df_transfer.groupby('Attack')['Transfer Success Rate'].mean()
    most_transferable = avg_by_attack.idxmax()
    avg_by_model = df_transfer.groupby('Model')['Accuracy Drop'].mean()
    most_vulnerable = avg_by_model.idxmax()
    least_vulnerable = avg_by_model.idxmin()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="insight-card"><h4>🎯 Most Transferable</h4><div class="insight-value text-red">{most_transferable}</div><div class="insight-detail">{avg_by_attack.max()*100:.1f}% avg transfer rate</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="insight-card"><h4>⚠️ Most Vulnerable</h4><div class="insight-value text-orange">{most_vulnerable}</div><div class="insight-detail">{avg_by_model.max()*100:.1f}% avg accuracy drop</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="insight-card"><h4>🛡️ Most Resistant</h4><div class="insight-value text-green">{least_vulnerable}</div><div class="insight-detail">{avg_by_model.min()*100:.1f}% avg accuracy drop</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Transfer Success Heatmap ---
    st.markdown('<div class="section-header">🗺️ Transfer Success Rate Heatmap</div>', unsafe_allow_html=True)
    models = df_matrix['Model'].tolist()
    attacks = [c for c in df_matrix.columns if c != 'Model']
    z_vals = df_matrix[attacks].values * 100
    fig_heat = go.Figure(go.Heatmap(
        z=z_vals, x=attacks, y=models,
        colorscale=[[0,'#0f172a'],[0.3,'#3b82f6'],[0.6,'#f59e0b'],[1.0,'#dc2626']],
        text=[[f"{v:.1f}%" for v in row] for row in z_vals],
        texttemplate="%{text}", textfont=dict(size=13, color='#e2e8f0'),
        colorbar=dict(title='Success %', tickfont=dict(color='#94a3b8')),
    ))
    fig_heat.update_layout(**CHART_LAYOUT, height=380,
        title=dict(text='Transfer Success Rate (%)', font=dict(size=14, color='#e2e8f0')),
        xaxis=dict(title='Attack Type'), yaxis=dict(title='Target Model'))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Grouped bars ---
    col1, col2 = st.columns(2)
    attack_colors = {'FGSM': '#f59e0b', 'PGD': '#3b82f6', 'C&W': '#ef4444'}
    with col1:
        fig_bar = go.Figure()
        for atk in df_transfer['Attack'].unique():
            sub = df_transfer[df_transfer['Attack'] == atk]
            fig_bar.add_trace(go.Bar(name=atk, x=sub['Model'], y=sub['Accuracy Drop']*100, marker_color=attack_colors.get(atk,'#94a3b8'), opacity=0.88))
        fig_bar.update_layout(**CHART_LAYOUT, barmode='group', height=420,
            title=dict(text='Accuracy Drop Under Transfer Attacks', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Accuracy Drop (pp)'), xaxis=dict(tickangle=-15),
            legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'))
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        fig_rem = go.Figure()
        for atk in df_transfer['Attack'].unique():
            sub = df_transfer[df_transfer['Attack'] == atk]
            fig_rem.add_trace(go.Bar(name=atk, x=sub['Model'], y=sub['Adversarial Accuracy']*100, marker_color=attack_colors.get(atk,'#94a3b8'), opacity=0.88))
        fig_rem.update_layout(**CHART_LAYOUT, barmode='group', height=420,
            title=dict(text='Remaining Accuracy After Attack', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Accuracy (%)', range=[0,110]), xaxis=dict(tickangle=-15),
            legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'))
        st.plotly_chart(fig_rem, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Full Data Table ---
    st.markdown('<div class="section-header">📋 Complete Transfer Data</div>', unsafe_allow_html=True)
    show_df = df_transfer.copy()
    for col in ['Baseline Accuracy','Adversarial Accuracy','Accuracy Drop','Transfer Success Rate']:
        show_df[col] = show_df[col] * 100
    st.dataframe(show_df.style
        .background_gradient(subset=['Transfer Success Rate'], cmap='OrRd')
        .format({'Baseline Accuracy':'{:.2f}%','Adversarial Accuracy':'{:.2f}%','Accuracy Drop':'{:.2f}%','Transfer Success Rate':'{:.2f}%'}),
        use_container_width=True, hide_index=True)

    # --- Key Findings ---
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown('<div class="warning-box"><h4 style="color:#f59e0b;margin-top:0;">⚠️ FGSM: Highly Transferable</h4><p>FGSM transfers well to Neural Networks (78.7%) and Logistic Regression (81.9%).</p></div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="success-box"><h4 style="color:#10b981;margin-top:0;">✅ C&W: Low NN Transfer</h4><p>C&W has only 9.7% transfer to Neural Networks — optimization-based attacks are model-specific.</p></div>', unsafe_allow_html=True)

    fig_path = get_figure_path("cross_model_transfer_analysis.png")
    if fig_path:
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        st.image(fig_path, use_column_width=True)
