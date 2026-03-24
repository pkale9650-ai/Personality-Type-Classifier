import streamlit as st
import numpy as np
import pickle
import plotly.graph_objects as go

# ── Page config
st.set_page_config(
    page_title="Personality Predictor",
    page_icon="🧠",
    layout="centered"
)

# ── Load model
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── CSS
st.markdown("""
    <style>
        .stApp { background-color: #0a0a0f; }
        section[data-testid="stMain"] { background-color: #0a0a0f; }
        [data-testid="stMainBlockContainer"] { padding-top: 1.5rem; }
        #MainMenu, footer, header { visibility: hidden; }

        .hero-card {
            background: linear-gradient(135deg, #1a1035 0%, #0f0f2e 60%, #0a0a1a 100%);
            border: 1px solid #2d2060;
            border-radius: 20px;
            padding: 2.2rem 2rem 1.8rem 2rem;
            text-align: center;
            margin-bottom: 1.2rem;
        }
        .hero-badge {
            display: inline-block;
            background: linear-gradient(90deg, #7c3aed, #6d28d9);
            color: #fff;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            padding: 7px 22px;
            border-radius: 20px;
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 1.75rem;
            font-weight: 800;
            color: #f1f5f9;
            margin-bottom: 0.3rem;
            letter-spacing: -0.5px;
        }
        .hero-subtitle { font-size: 0.95rem; color: #6b7280; margin: 0; }

        .stats-row {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-bottom: 1.8rem;
        }
        .stat-card {
            background: #111118;
            border: 1px solid #1e1e2e;
            border-radius: 14px;
            padding: 0.9rem 1rem;
        }
        .stat-label { font-size: 0.72rem; color: #6b7280; margin-bottom: 5px; }
        .stat-value { font-size: 0.95rem; font-weight: 700; color: #f1f5f9; }

        .section-head {
            font-size: 1rem; font-weight: 700; color: #e2e8f0;
            margin: 0.5rem 0 1rem 0; padding-bottom: 0.5rem;
            border-bottom: 1px solid #1e293b;
        }
        .stSlider label p {
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
        }
        div[data-testid="stButton"] > button {
            background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
            color: white !important; border: none !important;
            border-radius: 12px !important; padding: 0.75rem 2rem !important;
            font-size: 1.05rem !important; font-weight: 700 !important;
            width: 100% !important; cursor: pointer !important;
            transition: opacity 0.2s !important; margin-top: 0.5rem !important;
        }
        div[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

        .result-card {
            background: linear-gradient(135deg, #13111e 0%, #0f172a 100%);
            border: 1px solid #4f46e5; border-radius: 20px;
            padding: 2rem; text-align: center; margin: 1.5rem 0 0.5rem 0;
        }
        .result-badge {
            display: inline-block; background: #1e1b4b; color: #a5b4fc;
            font-size: 0.68rem; font-weight: 700; letter-spacing: 3px;
            text-transform: uppercase; padding: 5px 16px;
            border-radius: 20px; margin-bottom: 0.8rem; border: 1px solid #4338ca;
        }
        .result-emoji { font-size: 3rem; display: block; margin-bottom: 0.4rem; }
        .result-type {
            font-size: 2.8rem; font-weight: 800; color: #f1f5f9;
            letter-spacing: -1px; margin-bottom: 0.8rem;
        }
        .result-desc {
            font-size: 0.92rem; color: #94a3b8; line-height: 1.8;
            max-width: 480px; margin: auto;
        }
        .mini-card {
            background: #111118;
            border: 1px solid #1e1e2e;
            border-radius: 12px;
            padding: 0.8rem 1rem;
            text-align: center;
        }
        .mini-label {
            font-size: 0.68rem; color: #6b7280;
            margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;
        }
        .mini-value { font-size: 1rem; font-weight: 700; }

        .footer {
            text-align: center; color: #374151; font-size: 0.75rem;
            margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid #111827;
        }
    </style>
""", unsafe_allow_html=True)

# ── Hero Card
st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">🧠 AI Powered</div>
        <div class="hero-title">Personality Predictor</div>
        <p class="hero-subtitle">Get instant personality insights powered by Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# ── Stats Row
st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-label">Model</div>
            <div class="stat-value">Logistic Regression</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Accuracy</div>
            <div class="stat-value">99.77%</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Types</div>
            <div class="stat-value">🌙 Introvert</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">&nbsp;</div>
            <div class="stat-value">⚡ Ambivert</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">&nbsp;</div>
            <div class="stat-value">☀️ Extrovert</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Data
descriptions = {
    "Introvert": "You recharge through solitude and deep reflection. You prefer meaningful one-on-one conversations over large social gatherings and think carefully before you speak.",
    "Extrovert": "You thrive in social settings and gain energy from being around people. You are expressive, outgoing, and love being at the center of the action.",
    "Ambivert":  "You are a perfect blend of both worlds — enjoying social situations while also valuing your alone time. You adapt naturally to any environment."
}
emojis     = {"Introvert": "🌙", "Extrovert": "☀️", "Ambivert": "⚡"}
type_color = {"Introvert": "#5eead4", "Extrovert": "#a78bfa", "Ambivert": "#fbbf24"}

# ── Features (dropped: planning, gadget_usage, work_style_collaborative, group_comfort, listening_skill)
features = {
    "social_energy":           "Social Energy",
    "alone_time_preference":   "Alone Time Preference",
    "talkativeness":           "Talkativeness",
    "deep_reflection":         "Deep Reflection",
    "party_liking":            "Party Liking",
    "empathy":                 "Empathy",
    "creativity":              "Creativity",
    "organization":            "Organization",
    "leadership":              "Leadership",
    "risk_taking":             "Risk Taking",
    "public_speaking_comfort": "Public Speaking Comfort",
    "curiosity":               "Curiosity",
    "routine_preference":      "Routine Preference",
    "excitement_seeking":      "Excitement Seeking",
    "friendliness":            "Friendliness",
    "emotional_stability":     "Emotional Stability",
    "spontaneity":             "Spontaneity",
    "adventurousness":         "Adventurousness",
    "reading_habit":           "Reading Habit",
    "sports_interest":         "Sports Interest",
    "online_social_usage":     "Online Social Usage",
    "travel_desire":           "Travel Desire",
    "decision_speed":          "Decision Speed",
    "stress_handling":         "Stress Handling",
}

# ── Sliders — 3 per row
st.markdown('<p class="section-head">⚙️ Your Traits</p>', unsafe_allow_html=True)

values = {}
items  = list(features.items())

for row_start in range(0, len(items), 3):
    row_items = items[row_start:row_start+3]
    cols = st.columns(3)
    for col, (key, label) in zip(cols, row_items):
        with col:
            values[key] = st.slider(label, 0.0, 10.0, 5.0, step=0.1, key=key)

# ── Predict Button
st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔍 Predict My Personality", use_container_width=True)

# ── Result
if predict_btn:
    input_data = np.array([[values[k] for k in features.keys()]])
    prediction = model.predict(input_data)[0]
    proba      = model.predict_proba(input_data)[0]
    classes    = list(model.classes_)

    pred_idx   = classes.index(prediction)
    confidence = round(proba[pred_idx] * 100, 1)
    color      = type_color[prediction]

    # Result card
    st.markdown(f"""
        <div class="result-card">
            <div class="result-badge">Personality Analysis</div>
            <span class="result-emoji">{emojis[prediction]}</span>
            <div class="result-type">{prediction}</div>
            <div class="result-desc">{descriptions[prediction]}</div>
        </div>
    """, unsafe_allow_html=True)

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        number={"suffix": "%", "font": {"size": 36, "color": "#f1f5f9"}},
        title={"text": f"Confidence — {prediction}", "font": {"size": 16, "color": "#94a3b8"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#374151", "tickfont": {"color": "#6b7280", "size": 11}},
            "bar":  {"color": color, "thickness": 0.25},
            "bgcolor": "#111118",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  40],  "color": "#1a1a2e"},
                {"range": [40, 70],  "color": "#16213e"},
                {"range": [70, 100], "color": "#0f3460"},
            ],
            "threshold": {
                "line":  {"color": color, "width": 3},
                "thickness": 0.75,
                "value": confidence
            }
        }
    ))
    fig.update_layout(
        height=280,
        margin=dict(t=40, b=10, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f1f5f9"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Mini cards — 3 columns
    c1, c2, c3 = st.columns(3)
    for col, (cls, prob) in zip([c1, c2, c3], zip(classes, proba)):
        pct = round(prob * 100, 1)
        c   = type_color.get(cls, "#f1f5f9")
        col.markdown(f"""
            <div class="mini-card">
                <div class="mini-label">{cls}</div>
                <div class="mini-value" style="color:{c};">{pct}%</div>
            </div>
        """, unsafe_allow_html=True)

# ── Footer
st.markdown(
    '<p class="footer">Built with Logistic Regression &nbsp;·&nbsp; personality_synthetic_dataset.csv &nbsp;·&nbsp; Pratik</p>',
    unsafe_allow_html=True
)