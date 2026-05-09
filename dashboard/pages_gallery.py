"""Results Gallery page — Browse all 28 generated figures."""
import streamlit as st
import os
from config import FIGURE_CATALOG, get_figure_path


def render():
    st.markdown('<div class="page-title">🖼️ Results Gallery</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Browse all research figures organized by category</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Category filter ---
    categories = list(FIGURE_CATALOG.keys())
    selected = st.selectbox("Filter by Category", ["All Categories"] + categories)

    # Count available figures
    total = sum(1 for cat in FIGURE_CATALOG.values() for fn, _, _ in cat if get_figure_path(fn))
    total_all = sum(len(cat) for cat in FIGURE_CATALOG.values())
    st.markdown(f'<div class="info-box">Showing <strong>{total}</strong> of {total_all} figures. '
                f'Generated from 16 research notebooks across the full AdversarialShield pipeline.</div>',
                unsafe_allow_html=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # --- Render figures ---
    cats_to_show = FIGURE_CATALOG if selected == "All Categories" else {selected: FIGURE_CATALOG[selected]}

    for cat_name, figures in cats_to_show.items():
        st.markdown(f'<div class="section-header">{cat_name}</div>', unsafe_allow_html=True)

        # 2-column grid
        available = [(fn, title, nb) for fn, title, nb in figures if get_figure_path(fn)]
        if not available:
            st.markdown('<div class="warning-box">No figures found in this category.</div>', unsafe_allow_html=True)
            continue

        for i in range(0, len(available), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(available):
                    fn, title, notebook = available[idx]
                    fig_path = get_figure_path(fn)
                    with col:
                        st.markdown(f'<div class="gallery-card">', unsafe_allow_html=True)
                        st.image(fig_path, use_column_width=True)
                        st.markdown(
                            f'<div class="gallery-caption">'
                            f'<strong>{title}</strong><br>'
                            f'<span style="color:#64748b;font-size:0.75rem;">Source: {notebook}.ipynb</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
