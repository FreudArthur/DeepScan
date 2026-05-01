import streamlit as st

from utils.layout import metrics_row, presentation


def render(settings: dict):
	presentation()
	metrics_row(settings.get("score_min", 0.65))

	

	
	st.divider()

    # 🚀 SECTION DEMARRAGE
	st.markdown("## 🚀 Démarrage rapide")

	col1, col2, col3 = st.columns(3)

	with col1:
		st.markdown("### ➕ Ajouter")
		st.markdown("Ajoute de nouveaux visages à ta base de données.")

	with col2:
		st.markdown("### 🎥 Scanner")
		st.markdown("Utilise la caméra ou une image pour analyser.")

	with col3:
		st.markdown("### 🧠 Résultat")
		st.markdown("Obtiens le nom et le score de confiance.")
        
        
	col1, col2 = st.columns(2)
	with col1:
			if st.button("➕ Ajouter visage", width="stretch"):
				st.switch_page("pages/add_user.py")
	with col2:
			if st.button("🔍 Verifier", width="stretch"):
				st.switch_page("pages/verif.py")

	
	st.markdown('<div class="soft-card">', unsafe_allow_html=True)
	st.markdown("#### Apercu visuel")
	st.image("photos\\test_bill_Gates.png", width="stretch")
 
	col1 , col2 = st.columns(2)
 
 
	
	with col1:
		
		st.markdown("""
        ### 🔎 Exemple de détection

        - 👤 Nom reconnu : **Bill Gates**
        - 📊 Score : **0.958**
        - ⚡ Traitement rapide

         Le modèle analyse le visage et le compare à la base de donnée.
        """)
 
	with col2:
		st.info("💡 Astuce : Plus tu ajoutes de visages, plus le système devient précis.")

      	
	st.markdown("</div>", unsafe_allow_html=True)
	
