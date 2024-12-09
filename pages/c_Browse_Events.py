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
        
def format_date(date_str):
    """Convertir une chaîne de date en format dd-mm-yyyy."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_obj.strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return date_str

def browse_events():
    st.subheader("2024 events for each club:")

    # Vérifier si les instances existent
    if not hasattr(ml, 'clubs_instances') or not hasattr(ml, 'events_instances'):
        st.error("Clubs or events data not loaded. Please check your data.")
        return

    # Tri des clubs par ordre alphabétique
    sorted_clubs = sorted(ml.clubs_instances, key=lambda club: club.clubName)

    # Display clubs and their events
    for club in sorted_clubs:
        # Club name in green
        st.markdown(f"<h2 style='color: green;'>{club.clubName}</h2>", unsafe_allow_html=True)
        

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

 # Add a green line separator after each club
        st.markdown("<hr style='border: 2px solid green;'>", unsafe_allow_html=True)


# Lancer la fonction principale
if __name__ == "__main__":
    browse_events()
