import streamlit as st
import sqlite3
import session_state_handler as sh
from datetime import datetime
import pandas as pd
import multipage_layout as ml
#from multipage_layout import ml.events_instances
#from multipage_layout import Club
#from multipage_layout import Keywords
st.markdown(
    """
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("<h1 class=""centered"">Browse Events </h1>", unsafe_allow_html=True)

def format_date(date_str):
    """Convertir une chaîne de date en format dd-mm-yyyy."""
    try:
        # Convertir la chaîne en objet datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Reformatter en dd-mm-yyyy
        return date_obj.strftime("%d-%m-%Y")
    except ValueError:
        # Retourner la date d'origine si elle ne correspond pas au format attendu
        return date_str
        
def browse_events():  
    # Tri des clubs par ordre alphabétique
    sorted_clubs = sorted(ml.clubs_instances, key=lambda club: club.clubName)

    for club in sorted_clubs:
        # Afficher le nom du club en en-tête
        st.title(f"{club.clubName}", divider="green")

        # Récupérer les événements associés à ce club
        club_events = [event for event in ml.events_instances if event.clubName == club.clubName]

        if club_events:
            for event in club_events:
                # Afficher le nom de l'événement en sous-en-tête
                st.header(f"{event.title}", divider="black")

                # Afficher les détails de l'événement
                st.subheader(f"Event Type: {event.event_type}")
                st.subheader(f"Start: {format_date(event.startDate)}")
                st.subheader(f"End: {format_date(event.endDate)}")
                st.subheader(f"Location: {event.location_text}")
                st.subheader(f"Language: {event.language}")
                st.subheader(f"Description: {event.description}")
                st.markdown("---")  # Ligne de séparation entre les événements
        else:
            # Si aucun événement n'est associé à ce club
            st.write("No events available for this club.")
        st.markdown("===")  # Ligne de séparation entre les clubs


# Exécuter la fonction pour afficher la page
if __name__ == "__main__":
    browse_events()
