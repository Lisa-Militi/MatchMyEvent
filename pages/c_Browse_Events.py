import streamlit as st
import sqlite3
import session_state_handler as sh
from datetime import datetime
import pandas as pd
import multipage_layout as ml
#from multipage_layout import ml.events_instances
#from multipage_layout import Club
#from multipage_layout import Keywords
    
st.header('Complete list of events per clubs:')

def browse_events():
    st.title("Events browser")
    
    # Tri des clubs par ordre alphabétique
    sorted_clubs = sorted(ml.clubs_instances, key=lambda club: club.clubName)
    
    for club in sorted_clubs:
        # Afficher le nom du club en en-tête
        st.header(f"{club.clubName}", divider=True)
        
        # Récupérer les événements associés à ce club
        club_events = [event for event in ml.events_instances if event.clubName == club.clubName]
        
        if club_events:
            for event in club_events:
                # Afficher le nom de l'événement en sous-en-tête
                st.subheader(f"{event.title}", divider=True)
                
                # Afficher les détails de l'événement
                st.caption(f"Event Type: {event.event_type}")
                st.caption(f"Start: {event.startDate}")
                st.caption(f"End: {event.endDate}")
                st.caption(f"Location: {event.location_text}")
                st.caption(f"Language: {event.language}")
                st.caption(f"Description: {event.description}")
                st.markdown("---")  # Ligne de séparation entre les événements
        else:
            # Si aucun événement n'est associé à ce club
            st.write("No events available for this club.")
        st.markdown("===")  # Ligne de séparation entre les clubs

# Exécuter la fonction pour afficher la page
if __name__ == "__main__":
    browse_events()

if ml.events_instances:
    st.write("\nAttributes of the first instance:")
    print(f"EventName: {ml.events_instances[0].title}")
    print(f"StartDate: {ml.events_instances[0].startDate}")
    print(f"Event Type: {ml.events_instances[0].event_type}")
    print(f"Keywords: {ml.events_instances[0].event_keywords}")
    print(f"Description: {ml.events_instances[0].description}")

    st.write("\nAttributes of the first instance:")
    st.write(f"EventName: {ml.events_instances[0].title}")
    st.write(f"Event Type: {ml.events_instances[0].event_type}")
    st.write(f"StartDate: {ml.events_instances[0].startDate}")
    st.write(f"Keywords: {ml.events_instances[0].event_keywords}")
    st.write(f"Description: {ml.events_instances[0].description}")

st.session_state['ml.events_instances_list'] = ml.events_instances

