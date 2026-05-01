
""" import sys
import time
from pathlib import Path

import cv2
import numpy as np
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
	sys.path.insert(0, str(SRC_DIR))

from src.search_similar import recognize_face, recognize_face_from_numpy

DATA_DIR = ROOT / "data"
EMBEDDINGS_PATH = DATA_DIR / "embeddings.npy"
MAPPING_PATH = DATA_DIR / "mapping.json"
UPLOADS_DIR = DATA_DIR / "uploads"


def _save_upload(file_like, prefix: str) -> Path:
	UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
	suffix = Path(file_like.name).suffix if getattr(file_like, "name", "") else ".jpg"
	out_name = f"{prefix}_{int(time.time())}{suffix}"
	out_path = UPLOADS_DIR / out_name
	out_path.write_bytes(file_like.getbuffer())
	return out_path


def _decode_uploaded_image(file_like) -> np.ndarray:
	file_bytes = np.frombuffer(file_like.getbuffer(), dtype=np.uint8)
	image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

	if image_bgr is None:
		raise ValueError("Impossible de lire l'image fournie.")

	return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def _run_image_analysis(image_array: np.ndarray):
	return recognize_face_from_numpy(
		image_array=image_array,
		embeddings_path=str(EMBEDDINGS_PATH),
		mapping_path=str(MAPPING_PATH),
		k=5,
		temperature=0.3,
	)


def _run_video_analysis(video_path: Path, max_frames: int = 40, frame_step: int = 10):
	capture = cv2.VideoCapture(str(video_path))
	if not capture.isOpened():
		raise ValueError("Impossible d'ouvrir la vidéo.")

	frame_results = []
	frame_index = 0

	try:
		while True:
			success, frame = capture.read()
			if not success:
				break

			if frame_index % frame_step == 0:
				frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				try:
					result = _run_image_analysis(frame_rgb)
					best = result.get("best_match") if result else None
					if best:
						frame_results.append(
							{
								"frame": frame_index,
								"name": best.get("name"),
								"probability": best.get("probability", 0.0),
								"distance": best.get("distance", 0.0),
								"image_path": best.get("image_path", ""),
							}
						)
				except Exception:
					pass

				if len(frame_results) >= max_frames:
					break

			frame_index += 1
	finally:
		capture.release()

	if not frame_results:
		return {"best_match": None, "frames": []}

	best_match = max(frame_results, key=lambda item: item["probability"])
	return {"best_match": best_match, "frames": frame_results}


def render(settings: dict):
	st.markdown("### Verifier une identite")

	if "verify_result" not in st.session_state:
		st.session_state.verify_result = None
	if "verify_mode" not in st.session_state:
		st.session_state.verify_mode = "Upload"

	mode = st.selectbox("Mode", ["Upload", "Photo", "Vidéo"], key="verify_mode")
	st.caption(f"Mode temps reel: {'active' if settings.get('mode_temps_reel', True) else 'desactive'}")

	check_col_1, check_col_2 = st.columns(2)

	with check_col_1:
		if mode == "Upload":
			uploaded_image = st.file_uploader(
				"Charger une image à vérifier",
				type=["jpg", "jpeg", "png", "webp"],
				key="verify_uploader_image",
			)

			if uploaded_image:
				st.image(uploaded_image, caption="Image importée", use_container_width=True)

			if st.button("Lancer la vérification", key="verify_upload_button"):
				if not uploaded_image:
					st.error("Ajoute une image avant de lancer la vérification.")
				else:
					try:
						image_array = _decode_uploaded_image(uploaded_image)
						result = _run_image_analysis(image_array)
						best = result.get("best_match") if result else None
						st.session_state.verify_result = best

						if not best:
							st.warning("Aucun match trouvé.")
						else:
							st.success("Analyse terminée.")
					except Exception as e:
						st.error(f"Erreur lors de la recherche: {e}")

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
					try:
						image_array = _decode_uploaded_image(camera_image)
						result = _run_image_analysis(image_array)
						best = result.get("best_match") if result else None
						st.session_state.verify_result = best

						if not best:
							st.warning("Aucun match trouvé.")
						else:
							st.success("Photo analysée avec succès.")
					except Exception as e:
						st.error(f"Erreur lors de l'analyse de la photo: {e}")

		elif mode == "Vidéo":
			uploaded_video = st.file_uploader(
				"Charger une vidéo à analyser",
				type=["mp4", "mov", "avi", "mkv"],
				key="verify_video_uploader",
			)

			st.caption("La vidéo sera analysée par échantillonnage de frames.")

			if st.button("Lancer l'analyse vidéo", key="verify_video_button"):
				if not uploaded_video:
					st.error("Ajoute une vidéo avant de lancer l'analyse.")
				else:
					try:
						video_path = _save_upload(uploaded_video, "verify_video")
						result = _run_video_analysis(video_path)
						st.session_state.verify_result = result

						if not result.get("best_match"):
							st.warning("Aucun visage reconnu dans la vidéo.")
						else:
							st.success("Analyse vidéo terminée.")
					except Exception as e:
						st.error(f"Erreur lors de l'analyse vidéo: {e}")

	with check_col_2:
		st.markdown('<div class="soft-card">', unsafe_allow_html=True)
		st.markdown("#### Résultat")

		result = st.session_state.get("verify_result")

		if mode == "Vidéo" and isinstance(result, dict) and "frames" in result:
			best = result.get("best_match")
			frames = result.get("frames", [])

			if best:
				st.write(f"Nom prédit: {best.get('name')}")
				st.write(f"Score: {best.get('probability', 0.0):.4f}")
				st.write(f"Frame: {best.get('frame')}")
				if best.get("image_path") and Path(best["image_path"]).exists():
					st.image(str(best["image_path"]), use_container_width=True)
			else:
				st.write("Nom prédit: --")
				st.write("Score: --")

			if frames:
				st.markdown("##### Détails des frames")
				for item in frames[:10]:
					st.write(
						f"Frame {item['frame']} : {item['name']} ({item['probability']:.4f})"
					)
		else:
			if result:
				st.write(f"Nom prédit: {result.get('name')}")
				st.write(f"Score: {result.get('probability'):.4f}")
				if result.get("image_path") and Path(result["image_path"]).exists():
					st.image(str(result["image_path"]), use_container_width=True)
			else:
				st.write("Nom prédit: --")
				st.write("Score: --")
				st.progress(0)

		st.markdown("</div>", unsafe_allow_html=True) """
