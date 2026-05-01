"""Module de logging des requêtes et opérations en CSV."""

import pandas as pd
from pathlib import Path
from datetime import datetime


STATS_CSV = Path(__file__).parent.parent / "data" / "stats.csv"
COLUMNS = ["timestamp", "session_id", "mode", "status", "confiance", "personne"]


def _ensure_csv_exists():
    """Crée le fichier CSV s'il n'existe pas."""
    if not STATS_CSV.exists():
        STATS_CSV.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(STATS_CSV, index=False)


def log_requete(
    session_id: str,
    mode: str,
    status: str,
    confiance: float = None,
    personne: str = None,
):
    """
    Enregistre une requête dans le CSV.
    
    Args:
        session_id: ID de la session (main ou nom de session temporaire)
        mode: Type de requête (Upload, Photo, Vidéo)
        status: Résultat (valide, faible, rejet, error)
        confiance: Score de confiance (0-1)
        personne: Nom de la personne reconnue ou ajoutée
    """
    _ensure_csv_exists()
    
    new_row = pd.DataFrame(
        {
            "timestamp": [datetime.now().isoformat()],
            "session_id": [session_id],
            "mode": [mode],
            "status": [status],
            "confiance": [confiance if confiance is not None else ""],
            "personne": [personne or "--"],
        }
    )
    
    df = pd.read_csv(STATS_CSV)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(STATS_CSV, index=False)


def get_stats(session_id: str = None) -> pd.DataFrame:
    """
    Récupère les stats depuis le CSV.
    
    Args:
        session_id: Filtre optionnel par session
        
    Returns:
        DataFrame avec toutes les stats (ou filtrées)
    """
    _ensure_csv_exists()
    df = pd.read_csv(STATS_CSV)
    
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    if session_id:
        df = df[df["session_id"] == session_id]
    
    return df


def get_today_stats(session_id: str = None) -> pd.DataFrame:
    """Récupère les stats d'aujourd'hui."""
    df = get_stats(session_id)
    
    if df.empty:
        return df
    
    today = datetime.now().date()
    df = df[df["timestamp"].dt.date == today]
    
    return df


def get_summary_stats(session_id: str = None) -> dict:
    """
    Retourne un résumé des stats du jour.
    
    Returns:
        Dict avec total_requetes, taux_match, requetes_par_mode, etc.
    """
    df = get_today_stats(session_id)
    
    if df.empty:
        return {
            "total_requetes": 0,
            "taux_match": 0.0,
            "requetes_par_mode": {},
            "confiance_moyenne": 0.0,
        }
    
    total = len(df)
    valides = len(df[df["status"].isin(["valide"])])
    taux_match = (valides / total * 100) if total > 0 else 0
    
    # Extraire les modes
    requetes_par_mode = df["mode"].value_counts().to_dict()
    
    # Confiance moyenne (ignorer les vides)
    df_conf = df[df["confiance"] != ""]
    confiance_moyenne = 0.0
    if not df_conf.empty:
        df_conf["confiance"] = pd.to_numeric(df_conf["confiance"], errors="coerce")
        confiance_moyenne = df_conf["confiance"].mean()
    
    return {
        "total_requetes": total,
        "taux_match": taux_match,
        "requetes_par_mode": requetes_par_mode,
        "confiance_moyenne": confiance_moyenne,
    }


def get_recent_details(session_id: str = None, limit: int = 10) -> pd.DataFrame:
    """Retourne les N dernières requêtes formatées pour affichage."""
    df = get_stats(session_id)
    
    if df.empty:
        return df
    
    df = df.tail(limit).copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["Heure"] = df["timestamp"].dt.strftime("%H:%M:%S")
    df["Confiance"] = df["confiance"].apply(
        lambda x: f"{float(x):.2f}" if x != "" else "--"
    )
    df["Status"] = df["status"].apply(lambda x: _format_status(x))
    
    return df[["Heure", "mode", "personne", "Confiance", "Status"]].rename(
        columns={"mode": "Mode", "personne": "Personne"}
    )


def _format_status(status: str) -> str:
    """Formate le statut avec emoji."""
    status_map = {
        "valide": "✅ Valide",
        "faible": "⚠️ Faible",
        "rejet": "❌ Rejet",
        "error": "⚠️ Erreur",
        "enrollment": "📝 Ajouté",
    }
    return status_map.get(status, f"❓ {status}")
