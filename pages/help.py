import streamlit as st


def render(settings: dict):
	st.markdown("""
	<style>
		.help-card {
			background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
			padding: 20px;
			border-radius: 10px;
			border-left: 4px solid #ef7a2d;
			margin: 15px 0;
			box-shadow: 0 2px 8px rgba(0,0,0,0.1);
		}
		.help-title {
			color: #ef7a2d;
			font-weight: bold;
			font-size: 18px;
			margin-bottom: 10px;
		}
		.help-section {
			margin: 30px 0;
		}
	</style>
	""", unsafe_allow_html=True)

	# En-tête
	st.markdown("# 📚 Guide d'utilisation")
	st.markdown("Découvrez toutes les fonctionnalités de Deep Scan et comment les utiliser efficacement.")
	st.divider()

	# Section : Vue d'ensemble
	st.markdown("## 🎯 Vue d'ensemble")
	col1, col2 = st.columns(2)
	
	with col1:
		st.markdown("""
		**Deep Scan** est une application de reconnaissance faciale utilisant l'IA.
		Elle vous permet de :
		- 📸 Enregistrer des profils avec photos
		- 🔍 Vérifier l'identité à partir d'une image
		- 📊 Suivre vos statistiques d'utilisation
		""")
	
	with col2:
		st.info("💡 **Astuce** : Vous pouvez basculer entre une session temporaire (par défaut) et la base de données principale en saisissant le mot de passe.")

	st.divider()

	# Section : Fonctionnalités
	st.markdown("## 🚀 Fonctionnalités")

	# Accueil
	st.markdown('<div class="help-card">', unsafe_allow_html=True)
	st.markdown('<div class="help-title">🏠 Accueil</div>', unsafe_allow_html=True)
	st.markdown("""
	Page d'introduction et de présentation rapide du produit.
	- Vue globale de l'application
	- Informations sur les sessions (temporaire ou principale)
	- Accès rapide aux fonctionnalités principales
	""")
	st.markdown('</div>', unsafe_allow_html=True)

	# Ajout visage
	st.markdown('<div class="help-card">', unsafe_allow_html=True)
	st.markdown('<div class="help-title">👤 Ajout de visage</div>', unsafe_allow_html=True)
	st.markdown("""
	Enregistrez un nouveau profil dans la base de données.
	
	**Comment faire :**
	1. Entrez le nom de la personne
	2. Uploadez au moins **1 photo**
	3. Les photos doivent être claires et bien éclairées
	4. Cliquez sur "Ajouter au système"
	5. Désolé les photos de mangas , qui ne contiennent rien ou trop floues seront refusés 😏🙄
	
	💡 **Conseils :**
	- Utilisez des photos de qualité (1080p minimum)
	- Variez les angles (face, 3/4, profil)
	- Assurez-vous que le visage occupe au moins 30% de l'image
	- Évitez les lunettes de soleil et les casques
	""")
	st.markdown('</div>', unsafe_allow_html=True)

	# Vérification
	st.markdown('<div class="help-card">', unsafe_allow_html=True)
	st.markdown('<div class="help-title">🔍 Vérification d\'identité</div>', unsafe_allow_html=True)
	st.markdown("""
	Testez une image contre la base de données pour identifier une personne.
	
	**3 modes disponibles :**
	
	📤 **Upload** : Charger une image depuis votre ordinateur
	- Format : JPG, PNG, WebP , JPEG
	- Taille recommandée : moins de 5 MB
	
	📷 **Photo** : Prendre une photo avec votre caméra
	- Mode rapide sans fichier
	- Idéal pour les identifications instantanées
	
	🎥 **Vidéo** : Analyse en temps réel avec flux vidéo
	- Traitement continu
	- Affichage des résultats en direct
	
	**Résultats :**
	- ✅ Vert : Identification certaine (confiance > 75%)
	- ⚠️ Orange : Identification partielle (50% - 75%)
	- ❌ Rouge : Identification faible ou non reconnu
	""")
	st.markdown('</div>', unsafe_allow_html=True)

	# Stats
	st.markdown('<div class="help-card">', unsafe_allow_html=True)
	st.markdown('<div class="help-title">📊 Statistiques</div>', unsafe_allow_html=True)
	st.markdown("""
	Suivi en temps réel de vos activités et performances.
	
	**Indicateurs affichés :**
	- 📈 Nombre total de requêtes du jour
	- 🎯 Taux de correspondance (matches réussis)
	- 🔐 Confiance moyenne des détections
	- 📉 Graphiques de tendance (7 derniers jours)
	- 📋 Tableau des dernières requêtes
	- 🍰 Distribution par mode d'utilisation
	
	**Données isolées par session :**
	- Chaque session (temporaire ou principale) a ses propres statistiques
	- Consultez vos métriques sans mélanger les données
	""")
	st.markdown('</div>', unsafe_allow_html=True)

	st.divider()

	# Section : Gestion des sessions
	st.markdown("## 🔐 Gestion des sessions")
	
	col1, col2 = st.columns([1, 1])
	
	with col1:
		st.markdown("""
		**Session Temporaire** (par défaut)
		- Données isolées dans un cache local
		- Données supprimées en quittant l'app
		- Idéale pour les tests
		""")
	
	with col2:
		st.markdown("""
		**Session Principale**
		- Base de données persistante
		- Requiert un mot de passe
		- Pour les données importantes
		""")

	st.info("🔑 Accédez à la session principale via le menu latéral en entrant le mot de passe.")

	st.divider()

	# Section : Conseils et bonnes pratiques
	st.markdown("## 💡 Conseils et bonnes pratiques")
	
	with st.expander("📸 Qualité des photos"):
		st.markdown("""
		- **Éclairage** : Lumière naturelle de face (évitez les contrejours)
		- **Résolution** : Minimum 1080x1080 pixels
		- **Visage** : Occupe 30-70% de l'image
		- **Distance** : À 30-60 cm de la caméra
		- **Angle** : Face bien centrée
		""")
	
	with st.expander("🚀 Performance"):
		st.markdown("""
		- Uploadez d'abord une dizaine de profils
		- Prenez plusieurs photos par personne (3+ photos)
		- Variez les conditions d'éclairage
		- Plus de profils = plus grande base de données
		
		""")
	
	with st.expander("🛡️ Sécurité"):
		st.markdown("""
		- Vos données ne seront pas stockés et si vous etes pas convaincus vous pouvez vérifier sur mon GitHub [Here](https://github.com/FreudArthur/DeepScan)
		- Les sessions sont séparés entre elles. Dès que vous vous déconnectez elle s'efface automatiquement
		- Les données sont stockées localement
		""")

	st.divider()

	# Footer
	st.markdown("""
	---
	### 🏗️ Architecture
	L'application est prête à accueillir des évolutions progressives de la logique IA :
	- Algorithmes de reconnaissance améliorés
	- Nouvelles méthodes d'analyse
	- Intégrations API tierces notamment avec FastAPI
	
	**Version** : 1.0 | **Session actuelle** : """ + settings.get("session_name", "temporaire"))
	
	st.markdown("""
	---
	### ❓ Questions ?
	Consultez cette page régulièrement pour des mises à jour et des conseils supplémentaires. Ou rendez vous sur mon [GitHub](https://github.com/FreudArthur) ou dans mon [Mail](mailto:bokossafreud6@gmail.com)
	""" , unsafe_allow_html=True)
