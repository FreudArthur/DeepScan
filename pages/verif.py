import streamlit as st


def render(settings: dict):
	st.markdown("### Verifier une identite")
	check_col_1, check_col_2 = st.columns(2)

	with check_col_1:
		image_test = st.file_uploader(
			"Charger une image a verifier",
			type=["jpg", "jpeg", "png", "webp"],
			key="verify_uploader",
		)
		is_realtime = settings.get("mode_temps_reel", True)
		st.caption(f"Mode temps reel: {'active' if is_realtime else 'desactive'}")

		if st.button("Lancer la verification"):
			if image_test:
				st.success("Analyse lancee. Branche ici ta logique de prediction.")
			else:
				st.error("Ajoute une image avant de lancer la verification.")

	with check_col_2:
		st.markdown('<div class="soft-card">', unsafe_allow_html=True)
		st.markdown("#### Resultat")
		st.write("Nom predit: --")
		st.write("Score: --")
		st.progress(0)
		st.markdown("</div>", unsafe_allow_html=True)
