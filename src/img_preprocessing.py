import torch
import numpy as np
import matplotlib.pyplot as plt
import cv2
from src.pretrained import MTCNN_MODEL , EMBED_MODEL

import streamlit as st

# Charger une image et retourner un ndarray RGB

def load_image(path: str) -> np.ndarray:
    """
    Charger une image et retourner un ndarray RGB
    
    Args: 
        path (str) : chemin de l'image
        
    Returns:
            np.ndarray 
    """
    
    image_bgr = cv2.imread(str(path))  # type: ignore[attr-defined]

    if image_bgr is None:
        raise ValueError(f"Impossible de lire l'image: {path}")

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    print("Image chargée")

    return image_rgb








def show_image(image_original)-> None:
    
    """
    Afficher une image a partir d'un ndarray    
    Args: 
         image_original (ndarray | Tensor) : chemin de l'image
        
    Returns:
            None 
    """
    if isinstance(image_original, torch.Tensor):
        image_original = image_original.detach().cpu().numpy()

    if image_original.ndim != 3:
        raise ValueError("Format d'image invalide: attendu [H, W, C].")

    # Créer une figure avec 1 ligne et 2 colonnes
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Image originale
    axes[0].imshow(image_original.astype(np.uint8))
    axes[0].set_title('Originale')
    axes[0].axis('off')

    # Visage détecté
    face_detect = MTCNN_MODEL(image_original)
    axes[1].set_title('Visage')
    axes[1].axis('off')

    if face_detect is not None:
        axes[1].imshow(face_detect.permute(1, 2, 0).detach().cpu().numpy())
    else:
        axes[1].text(0.5, 0.5, 'Aucun visage détecté', ha='center', va='center')

    plt.show()
    
    
    
    
    
    
    
    
    

# Transformer une image en embedding
st.cache_data
def img_to_embedding(image_original) -> np.ndarray:
    """
    Transforme l'image originale en vecteur d'embedding.
    """
    if isinstance(image_original, torch.Tensor):
        image_original = image_original.detach().cpu().numpy()

    face_detect = MTCNN_MODEL(image_original)

    if face_detect is None:
        raise ValueError("Aucun visage détecté sur la photo.Veuillez réessayez")

    face_detect = face_detect.unsqueeze(0)

    with torch.no_grad():
        embedding = EMBED_MODEL(face_detect).detach().cpu().numpy().astype("float32")

    return embedding






    
if __name__ == "__main__":
    print("Preproccessing OK ...")
    show_image(load_image("photos/test_bill_Gates.png"))