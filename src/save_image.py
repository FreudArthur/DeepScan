import numpy as np
from pathlib import Path
import json
import os

from src.img_preprocessing import load_image , show_image , img_to_embedding





# Verifier les doublons
def is_already_encoded(new_embedding, db, threshold=0.3):
    # Calcul de la distance euclidienne entre le nouveau et toute la base
    distances = np.linalg.norm(db - new_embedding, axis=1)
    
    # Si la distance minimale est inférieure au seuil, c'est un doublon
    if np.min(distances) < threshold:
        return True
    return False





# Sauvegarde atomique JSON + NPY avec verification de synchronisation

def save_mapping_and_embedding_safely(
    mapping: dict,
    embeddings: np.ndarray,
    final_path_embed: str,
    final_path_mapping: str,
):
    """
    Sauvegarde atomique de mapping.json et embeddings.npy.
    Verifie la synchronisation avant ecriture definitive.
    """
    # On crée des objets pour les fichiers embeddings et mapping
    embed_path = Path(final_path_embed)
    map_path = Path(final_path_mapping)

    embed_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.parent.mkdir(parents=True, exist_ok=True)

    # On refait les vérifications de bases
    if not isinstance(mapping, dict):
        raise TypeError("mapping doit etre un dictionnaire.")

    if embeddings.ndim != 2 or embeddings.shape[1] != 512:
        raise ValueError(
            f"embeddings doit avoir la forme (N, 512), recu {embeddings.shape}."
        )

    if len(mapping) != embeddings.shape[0]:
        raise ValueError(
            f"Desynchronisation detectee: mapping={len(mapping)} embeddings={embeddings.shape[0]}"
        )

    # On crée les fichiers temporaires pour l'ecriture et le backup
    map_tmp = map_path.with_suffix(".json.tmp")
    embed_tmp = embed_path.with_suffix(".npy.tmp")

    map_bak = map_path.with_suffix(".json.bak")
    embed_bak = embed_path.with_suffix(".npy.bak")

    try:
        # 1) Ecriture temporaire
        with open(map_tmp, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

        # Ecriture binaire explicite pour eviter que numpy ajoute automatiquement .npy
        with open(embed_tmp, "wb") as f:
            np.save(f, embeddings.astype("float32"))

        # 2) Validation des temporaires
        with open(map_tmp, "r", encoding="utf-8") as f:
            mapping_check = json.load(f)

        with open(embed_tmp, "rb") as f:
            embeddings_check = np.load(f)

        if len(mapping_check) != embeddings_check.shape[0]:
            raise RuntimeError(
                "Validation des temporaires echouee: JSON et NPY ne sont pas synchronises."
            )

        # 3) Backup puis remplacement atomique
        if map_path.exists():
            os.replace(map_path, map_bak)
        if embed_path.exists():
            os.replace(embed_path, embed_bak)

        os.replace(map_tmp, map_path)
        os.replace(embed_tmp, embed_path)

        print(f"Base synchronisee avec succes ({len(mapping)} visages).")

    except Exception as e:
        # Si n'importe quel erreur intervient on efface les fichiers temporaires
        for tmp in [map_tmp, embed_tmp]:
            if tmp.exists():
                tmp.unlink()
        raise RuntimeError(f"Echec de sauvegarde atomique: {e}") from e
    


# Charger les fichiers de mappage pour eviter toute erreur
def load_mapping_strictly(file_path :str):
    """
    Pour éviter de corrompre les fichiers de mapping
    Soit l'image est enregistréer ou elle n'est pas enregistrée
    """
    
    path = Path(file_path)
    
    # Cas 1 : Le fichier n'existe pas encore (Premier lancement)
    if not path.exists():
        print("Initialisation du projet : Création d'un mapping vide.")
        return {}

    # Cas 2 : Tentative de lecture
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Vérifier que c'est bien un dictionnaire
            if not isinstance(data, dict):
                raise ValueError("Le format du JSON n'est pas un dictionnaire.")
            return data

    except (json.JSONDecodeError, ValueError) as e:
        # Cas 3 : Erreur de lecture -> On cherche un fichier temporaire (.tmp) comme une sorte de sauvegarde
        temp_path = path.with_suffix(".json.tmp")
        
        if temp_path.exists():
            print(f"⚠️ Erreur de lecture sur {path}. Tentative de récupération via le fichier temporaire ...")
            try:
                with open(temp_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                print("Fichier de backup est corrompu")
                pass # Si le backup foire aussi, on passe à l'exception finale
        
        # Cas 4 : Échec total -> On lève l'exception
        raise RuntimeError(
            f"IMPOSSIBLE DE CHARGER LE MAPPING : {e}\n"
            "Le fichier est corrompu et aucun backup valide n'a été trouvé. "
            "Veuillez vérifier manuellement le fichier avant de relancer."
        )

# Enregistrer un embedding avec verification stricte de la synchronisation

def save_embedding(
    embed: np.ndarray,
    person_name: str = None,
    image_path: str = None,
    embeddings_path: str = "../data/embeddings.npy",
    mapping_path: str = "../data/mapping.json",
    threshold: float = 0.3,
):
    """ Enregistrer un embedding avec verification stricte de la synchronisation
    """
    if embed.shape != (1, 512):
        raise ValueError(
            f"La taille de l'embedding doit etre (1, 512), recu {embed.shape}."
        )

    embeddings_file = Path(embeddings_path)

    # Chargement de NPY
    if embeddings_file.exists():
        db = np.load(embeddings_file).astype("float32")
        if db.ndim == 1:
            db = db.reshape(1, -1)
    else:
        db = np.empty((0, 512), dtype="float32")

    mapping = load_mapping_strictly(mapping_path)

    # Controle de synchronisation AVANT toute modification
    if len(mapping) != db.shape[0]:
        raise RuntimeError(
            f"Desynchronisation detectee avant sauvegarde: mapping={len(mapping)} embeddings={db.shape[0]}"
        )

    if db.shape[0] > 0 and is_already_encoded(embed, db, threshold=threshold):
        raise ValueError("Cette photo semble deja enregistree (doublon detecte).")

    updated_db = np.concatenate((db, embed.astype("float32")), axis=0)
    new_index = int(updated_db.shape[0] - 1)

    label = person_name if person_name else f"person_{new_index}"
    mapping[str(new_index)] = {
        "name": label,
        "image_path": image_path if image_path else "",
    }

    save_mapping_and_embedding_safely(
        mapping=mapping,
        embeddings=updated_db,
        final_path_embed=embeddings_path,
        final_path_mapping=mapping_path,
    )

    print(f"Done\nTaille actuelle {updated_db.shape}")
    return new_index



# Pipeline complet

def pipeline_save_image(
    image_path: str,
    person_name: str = None,
    embeddings_path: str = "../data/embeddings.npy",
    mapping_path: str = "../data/mapping.json",
    threshold: float = 0.3,
    preview: bool = True,
):
    """
    Enregistre une image dans la base de vecteurs via une sauvegarde atomique.

    Etapes:
    1) charge l'image
    2) affiche l'image + visage detecte (optionnel)
    3) extrait l'embedding
    4) verifie les doublons
    5) verifie la synchronisation mapping/embeddings
    6) sauvegarde atomique JSON + NPY
    """

    image_array = load_image(image_path)

    if preview:
        show_image(image_array)

    new_embedding = img_to_embedding(image_array).astype("float32")

    if new_embedding.shape != (1, 512):
        raise ValueError(
            f"Embedding invalide: attendu (1, 512), obtenu {new_embedding.shape}"
        )

    # Chemin unique de sauvegarde: save_embedding gere
    # - verification de synchro
    # - detection de doublon
    # - sauvegarde atomique mapping + embeddings
    new_index = save_embedding(
        embed=new_embedding,
        person_name=person_name,
        image_path=image_path,
        embeddings_path=embeddings_path,
        mapping_path=mapping_path,
        threshold=threshold,
    )

    updated_db = np.load(embeddings_path).astype("float32")
    mapping = load_mapping_strictly(mapping_path)

    if len(mapping) != updated_db.shape[0]:
        raise RuntimeError(
            f"Desynchronisation apres sauvegarde: mapping={len(mapping)} embeddings={updated_db.shape[0]}"
        )

    label = mapping[str(new_index)]["name"]

    print(f"Image enregistree avec succes. Index: {new_index}")
    print(f"Nouvelle taille de la base: {updated_db.shape}")

    return {
        "index": new_index,
        "name": label,
        "image_path": str(image_path),
        "embedding_shape": tuple(new_embedding.shape),
        "db_shape": tuple(updated_db.shape),
    }