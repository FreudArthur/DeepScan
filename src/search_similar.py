import torch
import numpy as np
import matplotlib.pyplot as plt
import torch
from pathlib import Path
import streamlit as st
from img_preprocessing import load_image , img_to_embedding
from save_image import load_mapping_strictly 
from search_similar_pre import calc_distance_with_faiss ,find_path


# Version avec le fichier déjà eregistrer en base
st.cache_data
def recognize_face(
    image_path: str,
    embeddings_path: str = "\\data\\embeddings.npy",
    mapping_path: str = "\\data\\mapping.json",
    k: int = 5,
    temperature: float = 0.3,
    show_best_match: bool = True,
):
    """
    Pipeline complet de reconnaissance:
    1) charge l'image requete
    2) calcule son embedding
    3) cherche les k plus proches dans FAISS
    4) retourne les resultats ordonnes avec probabilites
    5) affiche le meilleur match si show_best_match=True
    """
    if k <= 0:
        raise ValueError("k doit etre >= 1")

    # Verifications minimales des fichiers de base
    db_path = Path(embeddings_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Base introuvable: {embeddings_path}")

    mapping_data = load_mapping_strictly(mapping_path)
    if not isinstance(mapping_data, dict):
        raise TypeError("Le mapping doit etre un dictionnaire.")

    database = np.load(embeddings_path).astype("float32")
    if database.ndim != 2 or database.shape[1] != 512:
        raise ValueError(f"Base invalide, attendu (N, 512), recu {database.shape}")

    if database.shape[0] == 0:
        raise ValueError("La base embeddings est vide.")

    if len(mapping_data) != database.shape[0]:
        raise RuntimeError(
            f"Desynchronisation detectee: mapping={len(mapping_data)} embeddings={database.shape[0]}"
        )

    # Image requete + embedding
    query_img = load_image(image_path)
    query_vec = img_to_embedding(query_img).astype("float32")

    # Recherche FAISS + conversion en matches ordonnes
    k_search = min(int(k), database.shape[0])
    faiss_results = calc_distance_with_faiss(database=database, vector=query_vec, dimension=512)

    ordered_matches = find_path(
        mapping=mapping_path,
        results=faiss_results,
        top_k=k_search,
        temperature=temperature,
    )

    if not ordered_matches:
        return {"query_image": image_path, "best_match": None, "top_k": {}}

    best_match = ordered_matches[0]

    # Affichage du meilleur match
    if show_best_match:
        best_img_path = best_match.get("image_path", "")

        fig, axes = plt.subplots(1, 2, figsize=(10, 5))

        axes[0].imshow(query_img)
        axes[0].set_title("Image requete")
        axes[0].axis("off")

        if best_img_path and Path(best_img_path).exists():
            best_img = load_image(best_img_path)
            axes[1].imshow(best_img)
            axes[1].set_title(
                f"Best match: {best_match['name']}\nP={best_match['probability']:.2%}"
            )
            axes[1].axis("off")
        else:
            axes[1].text(
                0.5,
                0.5,
                f"Best match: {best_match['name']}\nImage introuvable",
                ha="center",
                va="center",
            )
            axes[1].axis("off")

        plt.tight_layout()
        plt.show()

    return {
        "query_image": str(image_path),
        "best_match": best_match,
        "top_k": ordered_matches,
    }


# Version Streamlit simplifiee: charge la base et mapping directement depuis les fichiers. Le fichier qui rentre est un ndarray
st.cache_data
def recognize_face_from_numpy(
    image_array,
    embeddings_path: str = "../data/embeddings.npy",
    mapping_path: str = "../data/mapping.json",
    k: int = 5,
    temperature: float = 0.3,
):
    """
    Pipeline de reconnaissance compatible Streamlit.
    Charge la base et le mapping directement depuis les fichiers.
    image_array est le seul paramètre en mémoire (numpy array ou torch tensor).
    """
    # Conversion de image_array si nécessaire
    if isinstance(image_array, torch.Tensor):
        image_array = image_array.detach().cpu().numpy()

    image_array = np.asarray(image_array)

    if image_array.ndim != 3:
        raise ValueError("Format d'image invalide: attendu [H, W, C].")

    # Charger la base depuis le fichier
    db_path = Path(embeddings_path)
    if not db_path.exists():
        raise FileNotFoundError(f"Base introuvable: {embeddings_path}")

    database = np.load(embeddings_path).astype("float32")
    database = np.ascontiguousarray(database)

    if database.ndim != 2 or database.shape[0] == 0:
        raise ValueError("La base d'embeddings doit avoir la forme (N, d) avec N > 0.")

    # Charger le mapping depuis le fichier
    mapping = load_mapping_strictly(mapping_path)

    if not isinstance(mapping, dict):
        raise TypeError("mapping doit etre un dictionnaire.")

    if len(mapping) != database.shape[0]:
        raise RuntimeError(
            f"Desynchronisation detectee: mapping={len(mapping)} embeddings={database.shape[0]}"
        )

    # Calcul de l'embedding de l'image
    query_vec = img_to_embedding(image_array).astype("float32")
    query_vec = np.ascontiguousarray(query_vec)

    # Recherche FAISS
    k_search = min(int(k), database.shape[0])
    faiss_results = calc_distance_with_faiss(
        database=database,
        vector=query_vec,
        dimension=database.shape[1],
    )

    # Récupération des matches ordonnés
    ordered_matches = find_path(
        mapping=mapping_path,
        results=faiss_results,
        top_k=k_search,
        temperature=temperature,
    )

    if not ordered_matches:
        return {"best_match": None, "top_k": {}}

    return {
        "best_match": ordered_matches[0],
        "top_k": ordered_matches,
    }



if __name__ == "__main__":
    # Exemple d'appel
    result = recognize_face(
        image_path="data\\test\\test.png",
        embeddings_path="data\\embeddings.npy",
        mapping_path="data\\mapping.json",
        k=5,
        temperature=0.3,
        show_best_match=True,
    )

    print(result)