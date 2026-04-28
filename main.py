import streamlit as st
from pages import accueil, add_user, help as help_page, stats, verif
from utils.layout import setup_page, sidebar

setup_page()
menu, settings = sidebar()

if menu == "Accueil":
    accueil.render(settings)
elif menu == "Ajout visage":
    add_user.render(settings)
elif menu == "Verification":
    verif.render(settings)
elif menu == "Stats":
    stats.render(settings)
else:
    help_page.render(settings)