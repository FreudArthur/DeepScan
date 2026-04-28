import streamlit as st

from utils.layout import metrics_row, presentation


def render(settings: dict):
	presentation()
	metrics_row(settings.get("score_min", 0.65))

	
	st.markdown("### Demarrage rapide")
	st.markdown(
			"1. Ajoute des visages dans l'onglet Ajout visage.\n"
			"2. Lance une verification avec camera ou image.\n"
			"3. Affiche les correspondances et le score de confiance."
		)
		
	col1, col2 = st.columns(2)
	with col1:
			if st.button("➕ Ajouter visage", use_container_width=True):
				st.switch_page("pages/add_user.py")
	with col2:
			if st.button("🔍 Verifier", use_container_width=True):
				st.switch_page("pages/verif.py")

	
	st.markdown('<div class="soft-card">', unsafe_allow_html=True)
	st.markdown("#### Apercu visuel")
	st.image("photos\\test_bill_Gates.png", use_container_width=True)
	st.markdown("</div>", unsafe_allow_html=True)
