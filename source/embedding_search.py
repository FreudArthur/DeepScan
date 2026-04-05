from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np


def find_most_similar_indices(
    query_embedding: Iterable[float] | np.ndarray,
    embeddings_path: str | Path = "../data/embeddings.npy",
    top_k: int = 5,
    metric: str = "cosine",
) -> list[int]:
    """Retourne les indices des embeddings les plus similaires au vecteur de requete.

    Args:
        query_embedding: Embedding de requete de taille (d,).
        embeddings_path: Chemin vers le fichier .npy contenant la base de vecteurs (N, d).
        top_k: Nombre de voisins a retourner.
        metric: "cosine" ou "l2".

    Returns:
        Liste d'indices de la base tries du plus proche au moins proche.
    """
    db = np.load(Path(embeddings_path))
    if db.ndim != 2:
        raise ValueError("Le fichier d'embeddings doit avoir la forme (N, d).")

    query = np.asarray(query_embedding, dtype=np.float32)
    if query.ndim != 1:
        query = query.reshape(-1)

    if query.shape[0] != db.shape[1]:
        raise ValueError(
            f"Dimension incompatible: query={query.shape[0]}, embeddings={db.shape[1]}"
        )

    top_k = int(top_k)
    if top_k <= 0:
        raise ValueError("top_k doit etre > 0.")

    top_k = min(top_k, db.shape[0])

    db = np.ascontiguousarray(db.astype(np.float32, copy=False))
    query = np.ascontiguousarray(query.astype(np.float32, copy=False))

    metric_key = metric.strip().lower()
    if metric_key == "cosine":
        # Evite division par zero au cas ou un vecteur a une norme nulle.
        eps = 1e-12
        db_norm = db / np.maximum(np.linalg.norm(db, axis=1, keepdims=True), eps)
        query_norm = query / max(np.linalg.norm(query), eps)
        similarity = db_norm @ query_norm
        best_idx = np.argsort(-similarity)[:top_k]
    elif metric_key == "l2":
        distances = np.sum((db - query) ** 2, axis=1)
        best_idx = np.argsort(distances)[:top_k]
    else:
        raise ValueError("metric doit etre 'cosine' ou 'l2'.")

    return best_idx.astype(int).tolist()
