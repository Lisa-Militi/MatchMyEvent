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

st.write(ml.clubs_instances)
st.write(ml.events_instances)
st.write(f"Event Type: {ml.events_instances[0].event_type}")
st.write(f"StartDate: {ml.events_instances[0].startDate}")
st.write(f"Keywords: {ml.events_instances[0].event_keywords}")
st.write(f"Description: {ml.events_instances[0].description}")

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
        
def format_date(date_str):
    """Convertir une chaîne de date en format dd-mm-yyyy."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_obj.strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return date_str

def browse_events():
    st.title("Events Browser")

    # Vérifier si les instances existent
    if not hasattr(ml, 'clubs_instances') or not hasattr(ml, 'events_instances'):
        st.error("Clubs or events data not loaded. Please check your data.")
        return

    # Tri des clubs par ordre alphabétique
    sorted_clubs = sorted(ml.clubs_instances, key=lambda club: club.clubName)

    # Parcourir les clubs
    for club in sorted_clubs:
        st.header(f"{club.clubName}")

        # Trouver les événements associés à ce club
        club_events = [event for event in ml.events_instances if event.clubName == club.clubName]

        if club_events:
            for event in club_events:
                st.subheader(f"{event.title}")
                st.write(f"**Event Type**: {event.event_type}")
                st.write(f"**Start Date**: {format_date(event.startDate)}")
                st.write(f"**End Date**: {format_date(event.endDate)}")
                st.write(f"**Location**: {event.location_text}")
                st.write(f"**Language**: {event.language}")
                st.write(f"**Description**: {event.description}")
                st.markdown("---")  # Ligne de séparation entre les événements
        else:
            st.write("No events available for this club.")
        st.markdown("===")  # Ligne de séparation entre les clubs

# Lancer la fonction principale
if __name__ == "__main__":
    browse_events()
