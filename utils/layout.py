from pathlib import Path
import re
import shutil

import streamlit as st
from streamlit_option_menu import option_menu


ROOT = Path()
MAIN_DATA_DIR = ROOT / "data"
CACHE_SESSIONS_DIR = ROOT / "cache" / "sessions"


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "session-temporaire"


def _build_session_paths(is_temp_session: bool, session_name: str) -> dict:
    if not is_temp_session:
        return {
            "is_temp_session": False,
            "session_name": "main",
            "data_dir": str(MAIN_DATA_DIR),
            "embeddings_path": str(MAIN_DATA_DIR / "embeddings.npy"),
            "mapping_path": str(MAIN_DATA_DIR / "mapping.json"),
            "uploads_dir": str(MAIN_DATA_DIR / "uploads"),
        }

    safe_name = _slugify(session_name)
    session_dir = CACHE_SESSIONS_DIR / safe_name
    return {
        "is_temp_session": True,
        "session_name": safe_name,
        "data_dir": str(session_dir),
        "embeddings_path": str(session_dir / "embeddings.npy"),
        "mapping_path": str(session_dir / "mapping.json"),
        "uploads_dir": str(session_dir / "uploads"),
    }


def _ensure_temp_session(session_name: str, source_mode: str) -> dict:
    session_paths = _build_session_paths(True, session_name)
    session_dir = Path(session_paths["data_dir"])
    uploads_dir = Path(session_paths["uploads_dir"])
    session_dir.mkdir(parents=True, exist_ok=True)
    uploads_dir.mkdir(parents=True, exist_ok=True)

    embeddings_path = Path(session_paths["embeddings_path"])
    mapping_path = Path(session_paths["mapping_path"])

    if source_mode == "Copier la base principale":
        if (MAIN_DATA_DIR / "embeddings.npy").exists() and not embeddings_path.exists():
            shutil.copy2(MAIN_DATA_DIR / "embeddings.npy", embeddings_path)
        if (MAIN_DATA_DIR / "mapping.json").exists() and not mapping_path.exists():
            shutil.copy2(MAIN_DATA_DIR / "mapping.json", mapping_path)
    else:
        if not embeddings_path.exists():
            import numpy as np

            np.save(embeddings_path, np.empty((0, 512), dtype="float32"))
        if not mapping_path.exists():
            mapping_path.write_text("{}", encoding="utf-8")

    return session_paths


def _delete_temp_session(session_name: str) -> None:
    safe_name = _slugify(session_name)
    session_dir = CACHE_SESSIONS_DIR / safe_name
    if session_dir.exists() and session_dir.is_dir():
        shutil.rmtree(session_dir)

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
            rate_time = st.slider("Rate Time(ms)" , 100 , 1000 , 200 , 50)
            mode_temps_reel = st.toggle("Mode temps réel", value=True)
            st.color_picker("Couleur du thème")

        st.divider()
        with st.expander("🧪 Session temporaire", expanded=False):
            temp_session_enabled = st.toggle(
                "Activer une session temporaire",
                value=st.session_state.get("temp_session_enabled", False),
                key="temp_session_enabled_widget",
            )
            temp_session_name = st.text_input("Nom de la session", value=st.session_state.get("temp_session_name", "test-cache"))
            auto_delete_on_disable = st.checkbox(
                "Supprimer automatiquement à la désactivation",
                value=True,
                key="temp_session_auto_delete",
            )
            source_mode = st.selectbox(
                "Point de départ",
                ["Copier la base principale", "Base vide"],
                index=0,
            )

            if st.button("Créer / réinitialiser la session"):
                session_name_value = temp_session_name or "test-cache"
                session_paths = _ensure_temp_session(session_name_value, source_mode)
                st.session_state["temp_session_name"] = session_paths["session_name"]
                st.session_state["temp_session_enabled"] = True
                st.session_state["session_paths"] = session_paths
                st.success(f"Session '{session_paths['session_name']}' prête dans le cache.")

            if st.button("Supprimer la session active"):
                session_name_to_delete = st.session_state.get("temp_session_name", temp_session_name)
                _delete_temp_session(session_name_to_delete)
                st.session_state["temp_session_enabled"] = False
                st.session_state["temp_session_enabled_widget"] = False
                st.session_state["session_paths"] = _build_session_paths(False, "main")
                st.success(f"Session '{_slugify(session_name_to_delete)}' supprimée.")

            previous_enabled = st.session_state.get("_temp_session_prev_enabled", False)
            if previous_enabled and not temp_session_enabled and auto_delete_on_disable:
                session_name_to_delete = st.session_state.get("temp_session_name", temp_session_name)
                _delete_temp_session(session_name_to_delete)
                st.info(f"Session '{_slugify(session_name_to_delete)}' supprimée automatiquement.")

            if temp_session_enabled:
                session_name = st.session_state.get("temp_session_name", temp_session_name)
                session_paths = _build_session_paths(True, session_name)
                st.session_state["temp_session_enabled"] = True
                st.session_state["session_paths"] = session_paths
                st.info(f"Session active: {session_paths['session_name']}")
            else:
                st.session_state["temp_session_enabled"] = False
                st.session_state["session_paths"] = _build_session_paths(False, "main")

            st.session_state["_temp_session_prev_enabled"] = temp_session_enabled

    session_paths = st.session_state.get("session_paths")
    if not session_paths:
        session_paths = _build_session_paths(False, "main")
        st.session_state["session_paths"] = session_paths

    return menu, {
        "score_min": score_min,
        "mode_temps_reel": mode_temps_reel,
        "rate_time" : rate_time,
        **session_paths,
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
