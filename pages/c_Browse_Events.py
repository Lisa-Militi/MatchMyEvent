import streamlit as st
import sqlite3
import session_state_handler as sh
from datetime import datetime
import pandas as pd
import multipage_layout as ml
#from multipage_layout import ml.events_instances
#from multipage_layout import Club
#from multipage_layout import Keywords



# Vérifier les résultats
for event in ml.events_instances:
    print(event)
    
#TEST
# Display all event instances with print
'''
print("Complete list of events:")
for event in ml.events_instances:
    print(event)
'''
    

# Display a specific instance (e.g., the first one)
if ml.events_instances:
    print("\nFirst instance:")
    print(ml.events_instances[0])





# Access specific attributes of an instance
if ml.events_instances:
    print("\nAttributes of the first instance:")
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

# Connexion à la base de données
db_path = '/mnt/data/test_file_DB.db'
connection = sqlite3.connect(db_path)

# Charger les données des tables
events_data = connection.execute(
    'SELECT _id, EventName, EventType, ClubName, EventDescription, startDate, endDate, Location_1, Language FROM events_file'
).fetchall()

clubs_data = connection.execute(
    'SELECT clubName FROM club_profile_list'
).fetchall()

# Convertir en DataFrame pour affichage
events_df = pd.DataFrame([{
    "EventName": event.title,
    "EventType": event.event_type,
    "ClubName": event.clubName,
    "EventDescription": event.description,
    "startDate": event.startDate,
    "endDate": event.endDate,
    "Location": event.location_text,
    "Language": event.language
} for event in events_instances])

# Affichage sur Streamlit
st.title("Events per Clubs")
clubs = events_df["ClubName"].unique()

for club in clubs:
    st.subheader(f"Événements organisés par {club}")
    club_events = events_df[events_df["ClubName"] == club]
    st.dataframe(
        club_events,
        column_config={
            "EventName": "Nom de l'Événement",
            "EventType": st.column_config.TextColumn("Type d'Événement"),
            "EventDescription": "Description",
            "startDate": st.column_config.DateColumn("Date de Début"),
            "endDate": st.column_config.DateColumn("Date de Fin"),
            "Language": st.column_config.TextColumn("Langue"),
        },
        hide_index=True,
    )
