import streamlit as st
from pathlib import Path
import sys
import time
import cv2
import numpy as np

from src.search_similar import recognize_face , recognize_face_from_numpy


# Add src to path for imports
ROOT = Path()
SRC_DIR = ROOT / "src"



# Ensure src is importable
ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"


def render(settings: dict):
	st.markdown("### Verifier une identite")
	check_col_1, check_col_2 = st.columns(2)
	
	if "mode" not in st.session_state:
		st.session_state.mode = "upload"

	mode = st.selectbox("Mode", ["Upload" , "Photo", "Vidéo"])

	with check_col_1:
		image_test = st.file_uploader(
			"Charger une image a verifier",
			type="image/*",
			key="verify_uploader",
		)
		is_realtime = settings.get("mode_temps_reel", True)
		st.caption(f"Mode temps reel: {'active' if is_realtime else 'desactive'}")

		if st.button("Lancer la verification"):
			if not image_test:
				st.error("Ajoute une image avant de lancer la verification.")
		
			else:
				
				file_bytes = np.asarray(bytearray(image_test.read()), dtype=np.uint8)
				image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
				image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
				
				

				try:
					res = recognize_face_from_numpy(
						image_array=image,
						embeddings_path=str(ROOT / "data" / "embeddings.npy"),
						mapping_path=str(ROOT / "data" / "mapping.json"),
						k=5,
						temperature=0.3,
					)

					best = res.get("best_match") if res else None
					if not best:
						st.warning("Aucun match trouve.")
						st.session_state['verify_result'] = None
					else:
						st.success("Analyse terminee.")
						st.session_state['verify_result'] = best

				except Exception as e:
					st.error(f"Erreur lors de la recherche: {e}")

	with check_col_2:
		st.markdown('<div class="soft-card">', unsafe_allow_html=True)
		st.markdown("#### Resultat")
		result = st.session_state.get('verify_result') if 'verify_result' in st.session_state else None
		if result:
			st.write(f"Nom predit: {result.get('name')}")
			st.write(f"Score: {result.get('probability'):.4f}")
			if result.get('image_path'):
				img_path = result.get('image_path')
				if Path(img_path).exists():
					st.image(str(img_path), width="stretch")
		else:
			st.write("Nom predit: --")
			st.write("Score: --")
			st.progress(0)
		st.markdown("</div>", unsafe_allow_html=True)
