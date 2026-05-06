"""Configuration and shared data for AdversarialShield Dashboard."""

# === PROJECT DATA ===
DEMO_DATA = {
    'baseline_accuracy': 0.9998,
    'attacks': {
        'FGSM': {'accuracy': 0.6297, 'l2_norm': 1.778, 'time': 0.05},
        'PGD': {'accuracy': 0.6364, 'l2_norm': 0.737, 'time': 0.5},
        'C&W': {'accuracy': 0.6032, 'l2_norm': 3.745, 'time': 5.0}
    },
    'defenses': {
        'No Defense':           {'clean': 99.98, 'fgsm': 62.97, 'pgd': 63.64, 'cw': 60.32},
        'Adversarial Training': {'clean': 99.98, 'fgsm': 99.97, 'pgd': 99.29, 'cw': 98.0},
        'Feature Squeezing':    {'clean': 99.98, 'fgsm': 85.53, 'pgd': 86.0,  'cw': 84.0},
        'Ensemble':             {'clean': 99.98, 'fgsm': 97.15, 'pgd': 97.0,  'cw': 95.0},
        'Combined':             {'clean': 99.98, 'fgsm': 97.40, 'pgd': 97.0,  'cw': 83.25},
    },
    'num_samples': 138541,
    'total_flows': 692703,
    'num_features': 41,
}

# === CSS STYLES ===
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global */
.stApp { font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1929 0%, #162544 100%);
    border-right: 1px solid rgba(59,130,246,0.15);
}
section[data-testid="stSidebar"] .stRadio label { color: #e2e8f0 !important; font-size: 1.05rem; }
section[data-testid="stSidebar"] .stRadio label:hover { color: #60a5fa !important; }

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 16px; padding: 24px; text-align: center;
    border: 1px solid rgba(59,130,246,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.metric-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(59,130,246,0.15); }
.metric-card .metric-value { font-size: 2.2rem; font-weight: 800; margin: 8px 0; }
.metric-card .metric-label { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
.metric-card .metric-delta { font-size: 0.9rem; font-weight: 600; margin-top: 4px; }

/* Color classes */
.text-blue { color: #3b82f6; }
.text-green { color: #10b981; }
.text-red { color: #ef4444; }
.text-orange { color: #f59e0b; }
.text-purple { color: #8b5cf6; }

/* Badges */
.badge {
    display: inline-block; padding: 6px 16px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600; margin: 4px;
    letter-spacing: 0.5px;
}
.badge-blue { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.badge-purple { background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
.badge-green { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }

/* Info boxes */
.info-box {
    background: rgba(59,130,246,0.08); border-left: 4px solid #3b82f6;
    border-radius: 0 12px 12px 0; padding: 20px; margin: 12px 0;
    color: #cbd5e1;
}
.success-box {
    background: rgba(16,185,129,0.08); border-left: 4px solid #10b981;
    border-radius: 0 12px 12px 0; padding: 20px; margin: 12px 0;
    color: #cbd5e1;
}
.warning-box {
    background: rgba(245,158,11,0.08); border-left: 4px solid #f59e0b;
    border-radius: 0 12px 12px 0; padding: 20px; margin: 12px 0;
    color: #cbd5e1;
}
.danger-box {
    background: rgba(239,68,68,0.08); border-left: 4px solid #ef4444;
    border-radius: 0 12px 12px 0; padding: 20px; margin: 12px 0;
    color: #cbd5e1;
}

/* Tech cards */
.tech-card {
    background: linear-gradient(135deg, #1e293b 0%, #293548 100%);
    border-radius: 14px; padding: 24px;
    border: 1px solid rgba(59,130,246,0.15);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
    min-height: 220px;
}
.tech-card:hover { transform: translateY(-3px); }
.tech-card h3 { color: #e2e8f0; margin-bottom: 12px; }
.tech-card ul { list-style: none; padding: 0; }
.tech-card ul li { padding: 6px 0; color: #94a3b8; font-size: 0.95rem; }
.tech-card ul li::before { content: "▸ "; color: #3b82f6; font-weight: bold; }

/* Insight cards */
.insight-card {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 14px; padding: 20px; text-align: center;
    border: 1px solid rgba(59,130,246,0.15);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.insight-card h4 { color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
.insight-card .insight-value { font-size: 1.5rem; font-weight: 700; margin: 8px 0; }
.insight-card .insight-detail { font-size: 0.9rem; color: #64748b; }

/* Page title */
.page-title {
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.page-subtitle { color: #94a3b8; font-size: 1.1rem; margin-bottom: 24px; }

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(30,41,59,0.8); border-radius: 8px 8px 0 0;
    border: 1px solid rgba(59,130,246,0.2); color: #94a3b8;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: rgba(59,130,246,0.15) !important;
    color: #60a5fa !important; border-bottom: 2px solid #3b82f6;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 12px 32px !important;
    font-weight: 600 !important; font-size: 1.05rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
}

/* Divider */
.gradient-divider {
    height: 2px; border: none; margin: 24px 0;
    background: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, transparent);
}
</style>
"""

# === CHART LAYOUT ===
CHART_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#94a3b8'),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor='#1e293b', font_size=13, font_family='Inter'),
)
