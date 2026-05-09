"""Advanced Analysis page — Adaptive attacks, Certified robustness, Continual defense, Backdoor."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from config import load_csv, CHART_LAYOUT, get_figure_path


def render():
    st.markdown('<div class="page-title">🔬 Advanced Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Adaptive attacks, certified robustness, continual defense & backdoor evaluation</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Adaptive Attacks", "📜 Certified Robustness", "🔄 Continual Defense", "🚪 Backdoor Attacks"])

    # ══════════════════════════════════════════════════════════
    # TAB 1 — Adaptive Attacks
    # ══════════════════════════════════════════════════════════
    with tab1:
        df_adap = load_csv("adaptive_attack_comparison.csv")
        if df_adap is None:
            st.error("Could not load adaptive attack data.")
        else:
            st.markdown('<div class="section-header">🎯 Standard vs Adaptive Attack Accuracy</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">Adaptive attacks are specifically crafted to bypass a known defense. They represent the <strong>gold standard</strong> for evaluating defense robustness.</div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Standard Attack', x=df_adap['Defense'], y=df_adap['Standard Attack']*100, marker_color='#3b82f6', opacity=0.88))
                fig.add_trace(go.Bar(name='Adaptive Attack', x=df_adap['Defense'], y=df_adap['Adaptive Attack']*100, marker_color='#ef4444', opacity=0.88))
                fig.update_layout(**CHART_LAYOUT, barmode='group', height=420,
                    title=dict(text='Standard vs Adaptive Attack', font=dict(size=14, color='#e2e8f0')),
                    yaxis=dict(title='Accuracy (%)', range=[0,110]), xaxis=dict(tickangle=-15),
                    legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'))
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                fig2 = go.Figure(go.Bar(
                    x=df_adap['Defense'], y=df_adap['Degradation']*100,
                    marker_color=['#10b981' if d < 0.05 else '#f59e0b' if d < 0.1 else '#ef4444' for d in df_adap['Degradation']],
                    text=[f"{d*100:.1f}pp" for d in df_adap['Degradation']], textposition='outside',
                    textfont=dict(size=12, color='#e2e8f0'), opacity=0.88))
                fig2.update_layout(**CHART_LAYOUT, height=420,
                    title=dict(text='Defense Degradation Under Adaptive Attack', font=dict(size=14, color='#e2e8f0')),
                    yaxis=dict(title='Degradation (pp)'), xaxis=dict(tickangle=-15))
                st.plotly_chart(fig2, use_container_width=True)

            # Data table
            show = df_adap.copy()
            show['Standard Attack'] = show['Standard Attack'] * 100
            show['Adaptive Attack'] = show['Adaptive Attack'] * 100
            show['Degradation'] = show['Degradation'] * 100
            st.dataframe(show.style.format({'Standard Attack':'{:.2f}%','Adaptive Attack':'{:.2f}%','Degradation':'{:.2f}pp'}), use_container_width=True, hide_index=True)

            st.markdown('<div class="warning-box"><h4 style="color:#f59e0b;margin-top:0;">⚠️ Key Finding</h4><p>Ensemble defense shows the highest degradation (12.6pp) under adaptive attacks, while Feature Squeezing is most resilient (1.1pp degradation).</p></div>', unsafe_allow_html=True)

            fig_path = get_figure_path("adaptive_attacks_evaluation.png")
            if fig_path:
                st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
                st.image(fig_path, use_column_width=True)

    # ══════════════════════════════════════════════════════════
    # TAB 2 — Certified Robustness
    # ══════════════════════════════════════════════════════════
    with tab2:
        df_cert = load_csv("certification_results.csv", subdir="certification")
        if df_cert is None:
            st.error("Could not load certification data.")
        else:
            st.markdown('<div class="section-header">📜 Randomized Smoothing Certification</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">Certified robustness provides <strong>mathematical guarantees</strong> that predictions won\'t change within a given perturbation radius.</div>', unsafe_allow_html=True)

            total = len(df_cert)
            correct = df_cert['correct'].sum()
            certified = df_cert['certified'].sum()
            finite_radii = df_cert[df_cert['certified_radius'] != np.inf]
            avg_radius = finite_radii['certified_radius'].mean() if len(finite_radii) > 0 else 0

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'<div class="stat-mini"><div class="stat-val text-blue">{total}</div><div class="stat-lbl">Total Samples</div></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="stat-mini"><div class="stat-val text-green">{correct/total*100:.1f}%</div><div class="stat-lbl">Correct</div></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="stat-mini"><div class="stat-val text-purple">{certified/total*100:.1f}%</div><div class="stat-lbl">Certified</div></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="stat-mini"><div class="stat-val text-cyan">{avg_radius:.4f}</div><div class="stat-lbl">Avg Certified Radius</div></div>', unsafe_allow_html=True)

            st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                # Radius distribution histogram
                radii = finite_radii['certified_radius'].values
                fig_hist = go.Figure(go.Histogram(x=radii, nbinsx=25, marker_color='#8b5cf6', opacity=0.8))
                fig_hist.update_layout(**CHART_LAYOUT, height=380,
                    title=dict(text='Certified Radius Distribution', font=dict(size=14, color='#e2e8f0')),
                    xaxis=dict(title='Certified Radius'), yaxis=dict(title='Count'))
                st.plotly_chart(fig_hist, use_container_width=True)

            with col2:
                # Probability lower bound vs radius scatter
                fig_sc = go.Figure(go.Scatter(
                    x=finite_radii['certified_radius'], y=finite_radii['probability_lower_bound'],
                    mode='markers',
                    marker=dict(size=8, color=finite_radii['correct'].astype(int), colorscale=['#ef4444','#10b981'], showscale=False),
                ))
                fig_sc.update_layout(**CHART_LAYOUT, height=380,
                    title=dict(text='Probability Bound vs Radius', font=dict(size=14, color='#e2e8f0')),
                    xaxis=dict(title='Certified Radius'), yaxis=dict(title='Probability Lower Bound'))
                st.plotly_chart(fig_sc, use_container_width=True)

            for fp in ["certified_robustness_analysis.png", "certified_robustness_finite_radii.png"]:
                fig_path = get_figure_path(fp)
                if fig_path:
                    st.image(fig_path, use_column_width=True)

    # ══════════════════════════════════════════════════════════
    # TAB 3 — Continual Defense
    # ══════════════════════════════════════════════════════════
    with tab3:
        df_cont = load_csv("continual_defense_history.csv")
        if df_cont is None:
            st.error("Could not load continual defense data.")
        else:
            st.markdown('<div class="section-header">🔄 Continual Learning Defense Evolution</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">The model is periodically retrained with newly discovered adversarial samples to maintain robustness over time.</div>', unsafe_allow_html=True)

            # Line chart
            fig_line = go.Figure()
            metrics_map = {'clean_acc': ('Clean', '#10b981'), 'fgsm_acc': ('FGSM', '#f59e0b'), 'pgd_acc': ('PGD', '#3b82f6'), 'cw_acc': ('C&W', '#ef4444')}
            for col, (label, color) in metrics_map.items():
                fig_line.add_trace(go.Scatter(
                    x=df_cont['week'], y=df_cont[col]*100, mode='lines+markers', name=label,
                    line=dict(color=color, width=3), marker=dict(size=10)))
            fig_line.update_layout(**CHART_LAYOUT, height=420,
                title=dict(text='Accuracy Evolution Over Weeks', font=dict(size=14, color='#e2e8f0')),
                xaxis=dict(title='Week', dtick=1), yaxis=dict(title='Accuracy (%)', range=[95,100.5]),
                legend=dict(orientation='h', y=1.12, x=0.5, xanchor='center'))
            st.plotly_chart(fig_line, use_container_width=True)

            # Training sample table
            st.dataframe(df_cont.style.format({
                'clean_acc':'{:.4f}','fgsm_acc':'{:.4f}','pgd_acc':'{:.4f}','cw_acc':'{:.4f}',
                'training_samples':'{:,.0f}','adversarial_samples':'{:,.0f}'}),
                use_container_width=True, hide_index=True)

            fig_path = get_figure_path("continual_defense_evolution.png")
            if fig_path:
                st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
                st.image(fig_path, use_column_width=True)

    # ══════════════════════════════════════════════════════════
    # TAB 4 — Backdoor Attacks
    # ══════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<div class="section-header">🚪 Backdoor / Trojan Attack Evaluation</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Backdoor attacks inject hidden triggers into the training data so that the model misclassifies specific inputs while maintaining normal performance otherwise.</div>', unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown('<div class="stat-mini"><div class="stat-val text-green">99.98%</div><div class="stat-lbl">Clean Accuracy</div></div>', unsafe_allow_html=True)
        with b2:
            st.markdown('<div class="stat-mini"><div class="stat-val text-red">94.2%</div><div class="stat-lbl">Attack Success Rate</div></div>', unsafe_allow_html=True)
        with b3:
            st.markdown('<div class="stat-mini"><div class="stat-val text-orange">0.5%</div><div class="stat-lbl">Poison Rate</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="danger-box"><h4 style="color:#ef4444;margin-top:0;">🚨 Critical Finding</h4><p>With only <strong>0.5% poisoning rate</strong>, backdoor attacks achieve 94.2% success while maintaining clean accuracy — making them extremely stealthy and difficult to detect.</p></div>', unsafe_allow_html=True)

        fig_path = get_figure_path("backdoor_attack_evaluation.png")
        if fig_path:
            st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
            st.image(fig_path, use_column_width=True)
