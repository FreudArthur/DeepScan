import streamlit as st
from pathlib import Path
import sys
import time
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer

from src.video_prepreocessing import VideoProcessor
from src.search_similar import recognize_face , recognize_face_from_numpy


# Add src to path for imports
ROOT = Path()
SRC_DIR = ROOT / "src"



# Ensure src is importable
ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"

def recognice_face(image_array):
    return recognize_face_from_numpy(
						image_array=image_array,
						embeddings_path=str(ROOT / "data" / "embeddings.npy"),
						mapping_path=str(ROOT / "data" / "mapping.json"),
						k=5,
						temperature=0.3,
					)
    

    
def render(settings: dict):
	st.markdown("### Verifier une identite")
	check_col_1, check_col_2 = st.columns(2)
	
	if "mode" not in st.session_state:
		st.session_state.mode = "Upload"

	mode = st.selectbox("Mode", ["Upload" , "Photo", "Vidéo"])

	with check_col_1:
     
    # Mode pour upload une image 
		if mode == "Upload":
			image_test = st.file_uploader(
				"Charger une image a verifier",
				type="image/*",
				key="verify_uploader",
			)
			is_realtime = settings.get("mode_temps_reel", True)
			st.caption(f"Mode temps reel: {'active' if is_realtime else 'desactive'}")

			if image_test:
				st.image(image=image_test)
    
			if st.button("Lancer la verification"):
				if not image_test:
					st.error("Ajoute une image avant de lancer la verification.")
			
				else:
					#st.image(image=image_test)
					file_bytes = np.asarray(bytearray(image_test.read()), dtype=np.uint8)
					image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
					image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
     

					try:
						res = recognice_face(
							image_array=image)

						best = res.get("best_match") if res else None
						if not best:
							st.warning("Aucun match trouve.")
							st.session_state['verify_result'] = None
						else:
							st.success("Analyse terminee.")
							st.session_state['verify_result'] = best

					except Exception as e:
						st.error(f"Erreur lors de la recherche: {e}")
		
  # Mode pour prendre une photo en direct
		elif mode == "Photo":
      
			camera_image = st.camera_input(
				"Prendre une photo à analyser",
				key="verify_camera_input",
			)

			if camera_image:
				st.image(camera_image, caption="Photo capturée", use_container_width=True)

			if st.button("Analyser la photo", key="verify_camera_button"):
				if not camera_image:
					st.error("Prends une photo avant de lancer l'analyse.")
				else: 
					file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
					image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
					image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)	
    				
			
					

					try:
						res = recognice_face(
							image_array=image)

						best = res.get("best_match") if res else None
						if not best:
							st.warning("Aucun match trouve.")
							st.session_state['verify_result'] = None
						else:
							st.success("Analyse terminee.")
							st.session_state['verify_result'] = best

					except Exception as e:
						st.error(f"Erreur lors de la recherche: {e}")
     
     
    
		if mode =="Vidéo":
      
			ctx = webrtc_streamer( key="vidéo",   video_processor_factory=lambda: VideoProcessor(recognice_face=recognice_face , interval=0.8))
   
			

			result_placeholder = st.empty()

			while ctx.state.playing:
				if ctx.video_processor:
					results = getattr(ctx.video_processor, "results", None)

					if results:
						best = results.get("best_match")

						if best:
							st.session_state['verify_result'] = best
							result_placeholder.success(f"👤 {best['name']} ({best['probability']:.2f})")
						else:
							result_placeholder.warning("Aucun match")
							st.session_state['verify_result'] = None
				
				time.sleep(0.5)  # 🔥 important pour éviter freeze CPU
			
			


	with check_col_2:
		st.markdown('<div class="soft-card">', unsafe_allow_html=True)
		st.markdown("#### Resultat")
		result = st.session_state.get('verify_result') if 'verify_result' in st.session_state else None
  
		if result:
			name = result.get("name")
			score = result.get("probability")

			if score > 0.75:
				st.success(f"Prédiction : {name}")
				st.snow()
			elif score > 0.5:
				st.warning(f"Prédiction : {name}")
				st.toast("Reconnaissance partielle ")
			else:
				st.error(f"Prédiction : {name}")
				st.toast("Reconnaissance faible")
			
			
			st.metric(label="Score de confiance", value=f"{score:.4f}")
			
			if result.get('image_path'):
				img_path = result.get('image_path')
				if Path(img_path).exists():
					st.image(str(img_path), width="stretch")
     
			vider = st.button("Vider réponse")
			if vider:
				st.session_state['verify_result'] = None
		else:
			st.write("Nom predit: --")
			st.write("Score: --")
			st.progress(0)
		st.markdown("</div>", unsafe_allow_html=True)
