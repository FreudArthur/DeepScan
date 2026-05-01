import numpy as np
import faiss
from pathlib import Path
from facenet_pytorch import MTCNN, InceptionResnetV1


from img_preprocessing import load_image , img_to_embedding
from save_image import load_mapping_strictly 


def calc_distance_with_faiss(database:np.ndarray , vector:np.ndarray , dimension = 512):
    


    # Créer + peupler l'index
    index = faiss.IndexFlatL2(dimension)
    index.add(database)

    # Recherche des 5 plus proches voisins
    
    D, I = index.search(vector, k=5)
    # D: distances (n_queries, k)  I: indices (n_queries, k)
    
    return {"distances" : D , "indices" : I}





# Probabilites softmax simples

def distances_to_probs(distances, T=0.1):
    """Convertit une liste de distances en probabilites.

    Plus la distance est petite, plus la probabilite est grande.
    T controle la douceur de la distribution.
    """
    distances = np.asarray(distances, dtype="float32").reshape(-1)

    if distances.size == 0:
        return np.array([], dtype="float32")

    if T <= 0:
        raise ValueError("T doit etre strictement positif.")

    # Softmax inverse: on favorise les petites distances
    
    # En reconnaissance faciale, une petite distance = une grande ressemblance. En mettant un signe moins, on transforme les distances (ex: 0.1, 0.5, 0.9) en scores (ex: -0.1, -0.5, -0.9). Ainsi, le plus grand nombre (le moins négatif) devient celui qui est le plus proche.

    scores = -distances / T
    
    # Mathématiquement, $e^{x}$ grandit extrêmement vite un x trop grand  peur provoquer Erreur d'Infini ou Overflow .L'astuce : En soustrayant le maximum de tous les scores, le plus grand score devient 0 ($e^0 = 1$) et tous les autres deviennent négatifs.Résultat : On travaille uniquement avec des nombres entre 0 et 1. Ça ne change pas les proportions finales, mais ça empêche le programme de crasher.
    
    scores = scores - np.max(scores)
    
    # np.exp : On passe à l'exponentielle pour s'assurer que tous nos résultats sont positifs (on ne peut pas avoir une probabilité de -5%).
    
    exp_scores = np.exp(scores)
    
    #total : On calcule la somme de toutes ces valeurs pour pouvoir diviser et obtenir un total de 100% (1.0).
    
    total = np.sum(exp_scores)

    # Si, pour une raison bizarre (distances infinies), le total est nul, on ne peut pas diviser.La solution : On renvoie une répartition équitable. Si tu as 3 candidats, on donne 33% à chacun ($1/3$). C'est une manière de dire : "Je ne sais pas, ils se ressemblent tous ou sont tous trop loin". C'est peu probable cela dit
    if total == 0:
        return np.full(distances.shape[0], 1.0 / distances.shape[0], dtype="float32")

    # On divise chaque score par le total.
    return (exp_scores / total).astype("float32")



# Fonction pour recuperer les correspondances les plus similaires
# et retourner un dictionnaire ordonne par similarite.
def find_path(mapping, results: dict, top_k: int | None = None, temperature: float = 0.3):
    """
    Retourne un dictionnaire ordonne des meilleurs matches FAISS.

    mapping peut etre:
    - un chemin vers mapping.json
    - un dictionnaire deja charge en memoire

    Format de sortie:
    {0: {"name": ..., "image_path": ..., "probability": ..., "distance": ...}, ...}
    """
    if not isinstance(results, dict):
        raise TypeError("results doit etre un dictionnaire retourne par FAISS.")

    if "indices" not in results or "distances" not in results:
        raise ValueError("results doit contenir les cles 'indices' et 'distances'.")

    indices = np.asarray(results["indices"])
    distances = np.asarray(results["distances"], dtype="float32")

    if indices.size == 0 or distances.size == 0:
        return {}

    if indices.ndim == 2:
        indices = indices[0]
    if distances.ndim == 2:
        distances = distances[0]

    if indices.shape[0] != distances.shape[0]:
        raise ValueError(
            f"Incoherence entre indices ({indices.shape[0]}) et distances ({distances.shape[0]})."
        )

    if isinstance(mapping, dict):
        mapping_data = mapping
    elif isinstance(mapping, str):
        mapping_data = load_mapping_strictly(mapping)
    else:
        raise TypeError("mapping doit etre un chemin (str) ou un dict deja charge.")

    if not isinstance(mapping_data, dict):
        raise TypeError("Le mapping doit contenir un dictionnaire JSON.")

    valid_items = []
    for idx, distance in zip(indices.tolist(), distances.tolist()):
        key = str(int(idx))
        if key not in mapping_data:
            continue

        entry = mapping_data[key]
        if not isinstance(entry, dict):
            continue

        valid_items.append(
            {
                "index": int(idx),
                "name": entry.get("name", "unknown"),
                "image_path": entry.get("image_path", ""),
                "distance": float(distance),
            }
        )

    if not valid_items:
        return {}

    if top_k is not None:
        top_k = max(1, min(int(top_k), len(valid_items)))
        valid_items = valid_items[:top_k]

    probabilities = distances_to_probs(
        [item["distance"] for item in valid_items],
        T=temperature,
    )

    ordered_matches = {}
    for rank, (item, probability) in enumerate(zip(valid_items, probabilities)):
        ordered_matches[rank] = {
            "name": item["name"],
            "image_path": item["image_path"],
            "probability": float(probability),
            "distance": item["distance"],
        }

    return ordered_matches











if __name__ =="__main__":
# Exemple d'utilisation (chemin)

    database = np.load("..\\data\\embeddings.npy")
    vector = img_to_embedding( load_image("..\\data\\images\\Laurent.jpg") )


    print(calc_distance_with_faiss(database=database , vector=vector))
    
    matches = find_path(
        "..\\data\\mapping.json",
        results=calc_distance_with_faiss(database=database, vector=vector),
        top_k=5,
        temperature=0.3,
    )
    
    print(matches)

