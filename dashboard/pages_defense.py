"""Defense Showcase page for AdversarialShield Dashboard."""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import load_csv, DEMO_DATA, CHART_LAYOUT, get_figure_path


def render():
    st.markdown('<div class="page-title">🛡️ Defense Mechanisms Showcase</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Explore how defenses protect against adversarial attacks</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Load real data ---
    df_bench = load_csv("complete_defense_benchmark.csv")
    if df_bench is not None:
        defense_names = df_bench['Defense'].tolist()
        defenses = {}
        for _, row in df_bench.iterrows():
            d = row['Defense']
            defenses[d] = {
                'clean': row['Clean'] * 100 if pd.notna(row['Clean']) else 0,
                'fgsm': row['FGSM'] * 100 if pd.notna(row['FGSM']) else 0,
                'pgd': row['PGD'] * 100 if pd.notna(row['PGD']) else 0,
                'cw': row['C&W'] * 100 if pd.notna(row.get('C&W', 0)) else 0,
            }
    else:
        defenses = DEMO_DATA['defenses']
        defense_names = list(defenses.keys())

    # --- Defense Performance Table ---
    st.markdown('<div class="section-header">📋 Defense Performance Matrix</div>', unsafe_allow_html=True)
    df_display = pd.DataFrame({
        'Defense': defense_names,
        'Clean (%)': [defenses[d]['clean'] for d in defense_names],
        'FGSM (%)': [defenses[d]['fgsm'] for d in defense_names],
        'PGD (%)': [defenses[d]['pgd'] for d in defense_names],
        'C&W (%)': [defenses[d]['cw'] for d in defense_names],
    })
    st.dataframe(
        df_display.style
        .background_gradient(subset=['FGSM (%)', 'PGD (%)', 'C&W (%)'], cmap='RdYlGn', vmin=50, vmax=100)
        .format({'Clean (%)': '{:.2f}', 'FGSM (%)': '{:.2f}', 'PGD (%)': '{:.2f}', 'C&W (%)': '{:.2f}'}),
        use_container_width=True, hide_index=True,
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Visualizations ---
    c1, c2 = st.columns(2)
    attack_keys = ['fgsm', 'pgd', 'cw']
    attack_labels = ['FGSM', 'PGD', 'C&W']
    attack_colors = ['#f59e0b', '#3b82f6', '#ef4444']

    with c1:
        fig1 = go.Figure()
        for ak, al, ac in zip(attack_keys, attack_labels, attack_colors):
            fig1.add_trace(go.Bar(
                name=al, x=defense_names,
                y=[defenses[d][ak] for d in defense_names],
                marker_color=ac, opacity=0.85,
            ))
        fig1.update_layout(**CHART_LAYOUT, barmode='group', height=420,
            title=dict(text='Accuracy Under Different Attacks', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Accuracy (%)', range=[50, 105], gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)', tickangle=-20),
            legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'))
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        # Recovery over no-defense baseline
        base_key = defense_names[0]
        no_def = defenses[base_key]
        other_defenses = [d for d in defense_names if d != base_key]
        fig2 = go.Figure()
        for ak, al, ac in zip(attack_keys, attack_labels, attack_colors):
            recovery = [defenses[d][ak] - no_def[ak] for d in other_defenses]
            fig2.add_trace(go.Bar(
                name=al, x=other_defenses, y=recovery,
                marker_color=ac, opacity=0.85,
            ))
        fig2.update_layout(**CHART_LAYOUT, barmode='group', height=420,
            title=dict(text='Recovery Rate (pp improvement)', font=dict(size=14, color='#e2e8f0')),
            yaxis=dict(title='Recovery (pp)', gridcolor='rgba(148,163,184,0.1)'),
            xaxis=dict(gridcolor='rgba(148,163,184,0.1)', tickangle=-20),
            legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Embed benchmark figure ---
    fig_path = get_figure_path("complete_defense_benchmark.png")
    if fig_path:
        st.markdown('<div class="section-header">📸 Complete Defense Benchmark</div>', unsafe_allow_html=True)
        st.image(fig_path, use_column_width=True)
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    fig_path2 = get_figure_path("adversarial_training_effectiveness.png")
    if fig_path2:
        st.markdown('<div class="section-header">📸 Adversarial Training Effectiveness</div>', unsafe_allow_html=True)
        st.image(fig_path2, use_column_width=True)
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Defense Details Tabs ---
    st.markdown('<div class="section-header">🔬 Defense Details</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["Adversarial Training", "Feature Squeezing", "Ensemble Defense", "Combined Defense"])

    with tab1:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="color:#60a5fa;margin-top:0;">Adversarial Training</h4>'
            '<p><strong>How it works:</strong></p>'
            '<ul style="color:#cbd5e1;">'
            '<li>Generate adversarial examples during training using FGSM/PGD</li>'
            '<li>Augment training data with adversarial samples (50/50 clean/adversarial ratio)</li>'
            '<li>Retrain the model on the augmented dataset</li>'
            '<li>Model learns to recognize and correctly classify perturbed inputs</li>'
            '</ul>'
            '<p><strong>Results:</strong> Near-complete recovery — 99.97% on FGSM, 99.29% on PGD</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="success-box">'
            '<strong>Key Benefit:</strong> Most effective single defense, achieving near-baseline accuracy on all attacks. '
            'The model genuinely learns robust features rather than relying on brittle patterns.'
            '</div>',
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="color:#60a5fa;margin-top:0;">Feature Squeezing</h4>'
            '<p><strong>Method:</strong> Reduces the precision of input features to eliminate small adversarial perturbations. '
            'Uses bit-depth reduction and spatial smoothing to "squeeze" out adversarial noise.</p>'
            '<p><strong>Results:</strong> 85.53% on FGSM, 60.3% on PGD, 60.3% on C&W</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="warning-box">'
            '<strong>Trade-off:</strong> Fast inference with no retraining needed, but moderate effectiveness. '
            'Best used as a complementary defense layer rather than standalone.'
            '</div>',
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="color:#60a5fa;margin-top:0;">Ensemble Defense</h4>'
            '<p><strong>Strategy:</strong> Combines predictions from multiple diverse models (XGBoost, Random Forest, Neural Network) '
            'using majority voting. Diversity makes it harder for an adversary to fool all models simultaneously.</p>'
            '<p><strong>Results:</strong> 97.15% on FGSM, 96.35% on PGD, 83.2% on C&W</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="success-box">'
            '<strong>Key Benefit:</strong> Model diversity provides natural robustness. Even if one model is fooled, '
            'the ensemble vote corrects the prediction.'
            '</div>',
            unsafe_allow_html=True,
        )

    with tab4:
        st.markdown(
            '<div class="info-box">'
            '<h4 style="color:#60a5fa;margin-top:0;">Combined Defense (Defense-in-Depth)</h4>'
            '<p><strong>Approach:</strong> Layers multiple defenses — feature squeezing as preprocessing, '
            'adversarial training for the base model, and ensemble voting for final prediction.</p>'
            '<p><strong>Results:</strong> 97.40% on FGSM, 96.19% on PGD, 83.25% on C&W</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="warning-box">'
            '<strong>Note:</strong> While strong against FGSM/PGD, C&W performance drops due to optimization-based attacks '
            'adapting to the combined pipeline. This highlights the need for adaptive attack evaluation.'
            '</div>',
            unsafe_allow_html=True,
        )
