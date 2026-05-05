import streamlit as st
from pathlib import Path
import sys
import time

# Add src folder to path so we can import pipeline_save_image
ROOT = Path()
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from src.save_image import pipeline_save_image
from src.csv_logger import log_requete


def render(settings: dict):    
    
    st.markdown("### Ajouter un nouveau profil") 
    embeddings_path = settings.get("embeddings_path", str(ROOT / "data" / "embeddings.npy"))
    mapping_path = settings.get("mapping_path", str(ROOT / "data" / "mapping.json"))
    uploads_dir = Path(settings.get("uploads_dir", str(ROOT / "data" / "uploads")))
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    if "mode_ajout" not in st.session_state:
        st.session_state.mode_ajout = None
    
    c1, c2 = st.columns([1, 1])   
    
    with c1:        
        
        col1_1 , col1_2 = st.columns(2)
        
        with col1_1 :
             if st.button("📂 Upload Image"):
                st.session_state.mode_ajout = "upload"
        
        with col1_2:
            if st.button("📷 Prendre une photo"):
                st.session_state.mode_ajout = "camera"
        
        nom = st.text_input(
            "Nom de la personne", placeholder="Ex: Jean Dupont"
            )    
            
        identifiant = st.text_input("Identifiant" , placeholder="ID-001") 
        
        # A ce niveau je mets l'option de soit uploader ou soit camera
        
        image_ajout = None
        
        if st.session_state.mode_ajout == "upload":    
            image_ajout = st.file_uploader("Importer une image du visage", type="image/*") 
             
        elif  st.session_state.mode_ajout == "camera" :
            image_ajout = st.camera_input(
				"Prendre une photo",
				key="verify_camera_input",
			)
            
  
          
        if st.button("Enregistrer le profil"):            
            if not (nom and identifiant and image_ajout):                
                st.warning("Remplis tous les champs avant validation.")            
            else:                
                suffix = Path(image_ajout.name).suffix
                timestamp = int(time.time())                
                out_name = f"{nom}{identifiant}_{timestamp}{suffix}"                
                out_path = uploads_dir / out_name     
                
        
                with open(out_path, "wb") as f:                    
                    f.write(image_ajout.getbuffer())    
                    try:                    
                        result = pipeline_save_image(
                            image_path=str(out_path),
                            person_name=nom,
                            embeddings_path=embeddings_path,
                            mapping_path=mapping_path,
                            preview=False,
                        )                    
                        st.success(f"Profil enregistré: index {result['index']} — {result['name']}")                    
                        st.write("Ready for the next 🔥🔥")         
                        st.balloons()
                        log_requete(
                            session_id=settings.get("session_name", "main"),
                            mode="Enrollment",
                            status="enrollment",
                            personne=nom,
                        )                       
                        
                    except Exception as e:                    
                        st.error(f"Erreur lors de l'enregistrement: {e}")
                        log_requete(
                            session_id=settings.get("session_name", "main"),
                            mode="Enrollment",
                            status="error",
                            personne=nom,
                        )    
    with c2:        
        st.markdown('<div class="soft-card">',  unsafe_allow_html=True)        
        st.markdown("#### Previsualisation")        
        if image_ajout:            
            st.image(image_ajout, width="stretch")        
        else:            
            st.info("Ajoute une image pour voir l'apercu.")        
        st.markdown("</div>", unsafe_allow_html=True)