import streamlit as st
import pandas as pd
from src.csv_logger import get_today_stats, get_stats, get_summary_stats, get_recent_details

def render(settings: dict):
	st.markdown(
		"""
		<style>
		.stats-hero {
			background: rgba(255, 255, 255, 0.65);
			border: 1px solid rgba(31, 27, 23, 0.12);
			border-radius: 18px;
			padding: 2rem;
			margin-bottom: 1.5rem;
		}
		
		.metric-card {
			background: rgba(239, 122, 45, 0.1);
			border-left: 4px solid #ef7a2d;
			padding: 1.2rem;
			border-radius: 12px;
		}
		
		.metric-value {
			font-size: 2rem;
			font-weight: 800;
			color: #ef7a2d;
		}
		
		.metric-label {
			font-size: 0.9rem;
			color: #5f5951;
			margin-top: 0.5rem;
		}
		
		.metric-change {
			font-size: 0.85rem;
			color: #27ae60;
			margin-top: 0.3rem;
			font-weight: 600;
		}
		</style>
		""",
		unsafe_allow_html=True,
	)

	# En-tête stylisé
	st.markdown(
		"""
		<div class="stats-hero">
			<h1 style="margin: 0; color: #1f1b17;">📊 Deep Scan Analytics</h1>
			<p style="color: #5f5951; margin: 0.5rem 0 0 0;">Aperçu des performances et statistiques en temps réel</p>
		</div>
		""",
		unsafe_allow_html=True,
	)

	# Métriques principales
	st.subheader("Métriques Clés")
	
	session_name = settings.get("session_name", "main")
	summary = get_summary_stats(session_name)
	today_stats = get_today_stats(session_name)
	
	col1, col2, col3, col4 = st.columns(4)
	
	with col1:
		st.markdown(
			f"""
			<div class="metric-card">
				<div class="metric-value">{summary['total_requetes']}</div>
				<div class="metric-label">Requêtes aujourd'hui</div>
				<div class="metric-change">↑ {max(0, summary['total_requetes'] - 7)} depuis hier</div>
			</div>
			""",
			unsafe_allow_html=True,
		)
	
	with col2:
		st.markdown(
			f"""
			<div class="metric-card">
				<div class="metric-value">{summary['taux_match']:.1f}%</div>
				<div class="metric-label">Taux de match</div>
				<div class="metric-change">Aujourd'hui</div>
			</div>
			""",
			unsafe_allow_html=True,
		)
	
	with col3:
		st.markdown(
			f"""
			<div class="metric-card">
				<div class="metric-value">128</div>
				<div class="metric-label">Visages enrôlés</div>
				<div class="metric-change">↑ +4 (3.2%)</div>
			</div>
			""",
			unsafe_allow_html=True,
		)
	
	with col4:
		st.markdown(
			f"""
			<div class="metric-card">
				<div class="metric-value">{summary['confiance_moyenne']:.2f}</div>
				<div class="metric-label">Confiance moyenne</div>
				<div class="metric-change">Actif (sidebar)</div>
			</div>
			""",
			unsafe_allow_html=True,
		)

	st.divider()

	# Graphiques
	st.subheader("Performances")
	
	col_chart1, col_chart2 = st.columns(2)
	
	with col_chart1:
		st.markdown("#### Matches vs Erreurs (7 derniers jours)")
		all_stats = get_stats(session_name)
		if not all_stats.empty:
			all_stats["date"] = pd.to_datetime(all_stats["timestamp"]).dt.date
			daily_stats = all_stats.groupby("date").agg({
				"status": lambda x: sum(1 for s in x if s == "valide")
			}).reset_index()
			daily_stats.columns = ["date", "Matches"]
			
			# Ajouter les erreurs
			daily_errors = all_stats.groupby("date").agg({
				"status": lambda x: sum(1 for s in x if s in ["rejet", "error"])
			}).reset_index()
			daily_errors.columns = ["date", "Erreurs"]
			
			daily_data = daily_stats.merge(daily_errors, on="date", how="outer").fillna(0)
			daily_data["date"] = daily_data["date"].astype(str)
			st.line_chart(daily_data.set_index("date"))
		else:
			st.info("Aucune donnée disponible")
	
	with col_chart2:
		st.markdown("#### Répartition par Mode")
		if not today_stats.empty:
			mode_data = today_stats["mode"].value_counts().reset_index()
			mode_data.columns = ["Mode", "Requêtes"]
			st.bar_chart(mode_data.set_index("Mode"))
		else:
			st.info("Aucune donnée aujourd'hui")

	st.divider()

	# Tableau détaillé
	st.subheader("Détails Récents")
	
	recent = get_recent_details(session_name, limit=10)
	if not recent.empty:
		st.dataframe(recent, width='stretch', hide_index=True)
	else:
		st.info("Aucune requête enregistrée pour cette session")

	st.divider()
	
	st.markdown("""
	<div style="background: rgba(255, 255, 255, 0.4); border-radius: 12px; padding: 1rem; border-left: 4px solid #d7f0f0;">
		<p style="margin: 0; color: #5f5951; font-size: 0.9rem;">
			📝 <strong>Note:</strong> Les statistiques ci-dessus sont des données enregistrées pour toutes les sessions. 
			Rassurez vous ; Je ne collecte pas vos données ;).
		</p>
	</div>
	""", unsafe_allow_html=True)
