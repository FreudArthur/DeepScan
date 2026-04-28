import streamlit as st


def render(settings: dict):
	st.markdown("### Ajouter un nouveau profil")
	c1, c2 = st.columns([1, 1])

	with c1:
		nom = st.text_input("Nom de la personne", placeholder="Ex: Jean Dupont")
		identifiant = st.text_input("Identifiant", placeholder="ID-001")
		image_ajout = st.file_uploader(
			"Importer une image du visage",
			type=["jpg", "jpeg", "png"],
		)

		if st.button("Enregistrer le profil"):
			if nom and identifiant and image_ajout:
				st.success("Profil pret a etre indexe.")
			else:
				st.warning("Remplis tous les champs avant validation.")

	with c2:
		st.markdown('<div class="soft-card">', unsafe_allow_html=True)
		st.markdown("#### Previsualisation")
		if image_ajout:
			st.image(image_ajout, use_container_width=True)
		else:
			st.info("Ajoute une image pour voir l'apercu.")
		st.markdown("</div>", unsafe_allow_html=True)
