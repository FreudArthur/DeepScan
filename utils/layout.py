import streamlit as st
from streamlit_option_menu import option_menu

def setup_page():
        
    st.set_page_config(
        page_title="Deep Scan | Face Recognition",
        page_icon="📷",
        layout="wide",
    )


    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Syne:wght@600;700;800&display=swap');

        :root {
            --bg-1: #f6efe5;
            --bg-2: #ffe3c2;
            --bg-3: #d7f0f0;
            --ink: #1f1b17;
            --muted: #5f5951;
            --brand: #ef7a2d;
            --brand-dark: #d5621a;
            --glass: rgba(255, 255, 255, 0.58);
            --border: rgba(31, 27, 23, 0.12);
        }

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Space Grotesk', sans-serif;
            color: var(--ink);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(65rem 40rem at -5% 0%, var(--bg-2), transparent 70%),
                radial-gradient(55rem 35rem at 120% 10%, #ffd79f, transparent 72%),
                linear-gradient(140deg, var(--bg-1) 0%, var(--bg-3) 100%);
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .hero {
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 2rem;
            background: var(--glass);
            backdrop-filter: blur(8px);
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.08);
        }

        .eyebrow {
            font-size: 0.82rem;
            color: var(--muted);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
        }

        .hero h1 {
            margin: 0.2rem 0 0.6rem 0;
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            line-height: 1;
            font-size: clamp(2rem, 5vw, 3.7rem);
        }

        .hero p {
            margin: 0;
            color: var(--muted);
            max-width: 52rem;
            font-size: 1.02rem;
        }

        .soft-card {
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1rem 0.6rem 1rem;
        }

        .stButton button {
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);
            color: white;
            font-weight: 700;
            padding: 0.55rem 1rem;
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.5rem;
        }

        @media (max-width: 768px) {
            .hero {
                padding: 1.2rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar():
    with st.sidebar:
        st.markdown("### Deep Scan")
        st.caption("Interface de démonstration")

        menu = option_menu(
            menu_title="Navigation",
            options=["Accueil", "Ajout visage", "Verification", "Stats", "Aide"],
            icons=["house", "person-plus", "shield-check", "bar-chart", "question-circle"],
            menu_icon="camera",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#ffead9ff"},
                "icon": {"color": "orange", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#ceb1867f"},

            }
        )

        st.divider()
        with st.expander("🛠️ Paramètres Avancés"):
            score_min = st.slider("Seuil de confiance", 0.10, 1.00, 0.65, 0.01)
            mode_temps_reel = st.toggle("Mode temps réel", value=True)
            st.color_picker("Couleur du thème")

    return menu, {
        "score_min": score_min,
        "mode_temps_reel": mode_temps_reel,
    }

def header():
    st.title("🚀 Deep Scan")
    st.write("---")

def presentation(): 
    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Reconnaissance faciale intelligente</div>
            <h1>Deep Scan Studio</h1>
            <p>
                Base d'interface moderne pour une application de reconnaissance faciale.
                Emerveillé par la reconnaissance faciale ?? Ceci est pour toi. Tu peux t'amuser seul ou avec tes potes pour trouver des similarités ou des ressemblances. Mieux tu peux utiliser l'API totalement gratuitement si tu veux construire une app perso 😏
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write("")


def metrics_row(score_min: float):
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Visages enroles", "128", "+4 aujourd'hui")
    col_b.metric("Precision estimee", "97.3%", "+0.8%")
    col_c.metric("Seuil actif", f"{score_min:.2f}", "personnalise")
