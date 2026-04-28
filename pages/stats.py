import streamlit as st


def render(settings: dict):
	st.markdown("### Stats")
	st.caption("Vue analytique simple en attendant le branchement des vraies metriques.")

	c1, c2, c3 = st.columns(3)
	c1.metric("Requetes aujourd'hui", "42", "+7")
	c2.metric("Taux de match", "89%", "+2%")
	c3.metric("Seuil courant", f"{settings.get('score_min', 0.65):.2f}", "sidebar")

	st.markdown("#### Historique")
	st.line_chart({"matches": [3, 5, 4, 6, 8, 7, 9], "erreurs": [1, 1, 2, 1, 1, 0, 1]})
