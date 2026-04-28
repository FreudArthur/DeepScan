import streamlit as st


def render(settings: dict):
	st.markdown("### Aide")
	st.markdown(
		"- Accueil: presentation rapide du produit.\n"
		"- Ajout visage: formulaire d'ajout d'un profil.\n"
		"- Verification: test d'une image contre la base.\n"
		"- Stats: suivi des indicateurs de base."
	)

	st.info("L'architecture est prete pour brancher la logique IA progressivement.")
