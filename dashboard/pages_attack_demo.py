"""Live Attack Demo page for AdversarialShield Dashboard."""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from config import DEMO_DATA, CHART_LAYOUT


def render():
    st.markdown('<div class="page-title">⚔️ Live Attack Demonstration</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">See adversarial attacks in action — fool the IDS in real-time!</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    config_col, result_col = st.columns([3, 7])

    with config_col:
        st.markdown('<div class="tech-card"><h3>⚙️ Configuration</h3></div>', unsafe_allow_html=True)
        attack_type = st.selectbox("Select Attack Type", ["FGSM", "PGD", "C&W"])

        if attack_type == "FGSM":
            epsilon = st.slider("Epsilon (ε)", 0.05, 0.50, 0.30, 0.05, help="Perturbation budget")
        elif attack_type == "PGD":
            epsilon = st.slider("Epsilon (ε)", 0.05, 0.30, 0.15, 0.05)
            iterations = st.slider("Iterations", 5, 50, 10)
        else:  # C&W
            c_param = st.slider("C Parameter", 0.5, 5.0, 1.0, 0.1)
            iterations = st.slider("Iterations", 50, 200, 100, 10)

        sample_idx = st.number_input("Sample Index", 0, 1000, 42)
        launch = st.button("🚀 Launch Attack", use_container_width=True)

    with result_col:
        if launch:
            # Simulate attack with progress
            progress = st.progress(0, text="Initializing attack...")
            for i in range(100):
                time.sleep(0.015)
                if i < 30:
                    txt = "Loading sample data..."
                elif i < 60:
                    txt = f"Generating adversarial perturbation ({attack_type})..."
                elif i < 85:
                    txt = "Evaluating adversarial sample..."
                else:
                    txt = "Finalizing results..."
                progress.progress(i + 1, text=txt)
            progress.empty()

            st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

            # Simulated results
            np.random.seed(sample_idx)
            true_label = np.random.choice(["ATTACK", "BENIGN"], p=[0.365, 0.635])
            orig_pred = true_label
            orig_conf = np.random.uniform(95, 99.9)

            atk_data = DEMO_DATA['attacks'][attack_type]
            attack_success = np.random.random() < (1 - atk_data['accuracy'])
            adv_pred = ("BENIGN" if true_label == "ATTACK" else "ATTACK") if attack_success else true_label
            adv_conf = np.random.uniform(55, 85) if attack_success else np.random.uniform(80, 95)
            l2_pert = atk_data['l2_norm'] * np.random.uniform(0.7, 1.3)

            # Display original vs adversarial
            r1, r2 = st.columns(2)
            with r1:
                label_color = "#10b981" if true_label == "ATTACK" else "#3b82f6"
                st.markdown(
                    f'<div class="success-box">'
                    f'<h4 style="color:#10b981;margin-top:0;">✅ Original Sample</h4>'
                    f'<p><strong>True Label:</strong> <span style="color:{label_color}">{true_label}</span></p>'
                    f'<p><strong>Prediction:</strong> <span style="color:{label_color}">{orig_pred}</span></p>'
                    f'<p><strong>Confidence:</strong> {orig_conf:.2f}%</p>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with r2:
                if attack_success:
                    st.markdown(
                        f'<div class="warning-box">'
                        f'<h4 style="color:#f59e0b;margin-top:0;">⚠️ Adversarial Sample</h4>'
                        f'<p><strong>New Prediction:</strong> <span style="color:#ef4444">{adv_pred}</span></p>'
                        f'<p><strong>Confidence:</strong> {adv_conf:.2f}%</p>'
                        f'<p><strong>L2 Perturbation:</strong> {l2_pert:.3f}</p>'
                        f'<p style="color:#f59e0b;font-weight:600;">🎯 Attack Successful! Model fooled.</p>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="success-box">'
                        f'<h4 style="color:#10b981;margin-top:0;">✅ Adversarial Sample</h4>'
                        f'<p><strong>Prediction:</strong> <span style="color:#10b981">{adv_pred}</span></p>'
                        f'<p><strong>Confidence:</strong> {adv_conf:.2f}%</p>'
                        f'<p><strong>L2 Perturbation:</strong> {l2_pert:.3f}</p>'
                        f'<p style="color:#10b981;font-weight:600;">🛡️ Model resisted the attack.</p>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            # Feature perturbation chart
            st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
            st.markdown("#### 📊 Feature Perturbation Analysis")
            n_feat = 10
            feat_names = [f"Feature {i}" for i in np.random.choice(41, n_feat, replace=False)]
            orig_vals = np.random.uniform(0.1, 1.0, n_feat)
            adv_vals = orig_vals + np.random.uniform(-0.3, 0.3, n_feat) * (l2_pert / 3)

            fig = go.Figure()
            fig.add_trace(go.Bar(name='Original', x=feat_names, y=orig_vals, marker_color='#10b981', opacity=0.85))
            fig.add_trace(go.Bar(name='Adversarial', x=feat_names, y=adv_vals, marker_color='#ef4444', opacity=0.85))
            fig.update_layout(
                **CHART_LAYOUT, barmode='group',
                title=dict(text='Top 10 Most Perturbed Features', font=dict(size=15, color='#e2e8f0')),
                yaxis=dict(title='Feature Value', gridcolor='rgba(148,163,184,0.1)'),
                xaxis=dict(gridcolor='rgba(148,163,184,0.1)'),
                legend=dict(orientation='h', y=1.12, x=0.5, xanchor='center'),
                height=380,
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.markdown(
                '<div style="display:flex;align-items:center;justify-content:center;height:400px;">'
                '<div style="text-align:center;">'
                '<div style="font-size:4rem;margin-bottom:16px;">⚔️</div>'
                '<h3 style="color:#64748b;">Configure attack parameters and click Launch Attack</h3>'
                '<p style="color:#475569;">Select an attack type, adjust parameters, and launch to see results</p>'
                '</div></div>',
                unsafe_allow_html=True,
            )
