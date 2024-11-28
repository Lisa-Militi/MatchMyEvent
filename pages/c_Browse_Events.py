#import d_Event_Recommendations as ER
import streamlit as st
#import session_state_handler as sh
import csv
from datetime import datetime
import pandas as pd

# Classe pour les événements
class Event_profile:
    def __init__(self, _id, title, type, clubName, description, startDate, endDate, location.text):
        self._id = EventID
        self.title = EventName
        self.type = EventType
        self.clubName = ClubName
        self.description = EventDescription
        self.startDate = datetime.strptime(StartDate, '%Y-%m-%d')  # Conversion en datetime
        self.endDate = datetime.strptime(EndDate, '%Y-%m-%d')  # Conversion en datetime
        self.location.text = Location
        self.event_keywords = []

    def __repr__(self):
        return (
            f"Event_profile(EventID={self._id!r}, EventName={self.title!r}, "
            f"EventType={self.type!r}, ClubName={self.clubName!r}, "
            f"StartDate={self.startDate!r}, EndDate={self.endDate!r}, Location={self.location.text!r}, "
            f"Keywords={self.event_keywords})"
        )

# Classe pour les clubs
class Club:
    def __init__(self, clubName, InterestKeywords):
        self.clubName = ClubName
        self.InterestKeywords = club_keywords

def __repr__(self):
        return (
            f"Club(ClubName={self.clubName!r}, club_keywords={self.InterestKeywords})"
        )
    
# Classe pour les mots-clés globaux
class Keywords:
    def __init__(self, KeywordsCloud):
        self.KeywordCloud = KeywordCloud.split(',')

    def __repr__(self):
        return f"KeywordCloud({self.KeywordCloud})"

# Fonction pour lire les fichiers CSV
def read_csv_file(file_path):
   data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Charger les fichiers CSV - to be replaced
file_path_events = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Group 8 Project 20.11.2024\Events_file_updated.csv"
file_path_clubs = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Group 8 Project 20.11.2024\Clubs_file.csv"
file_path_keywords = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Group 8 Project 20.11.2024\Keywords_Cloud.csv"

events_data = read_csv_file(file_path_events)
clubs_data = read_csv_file(file_path_clubs)
keywords_data = read_csv_file(file_path_keywords)

# Créer des instances de Club
clubs_instances = []
for club in clubs_data:
    club_instance = Club(ClubName=club['ClubName'], club_keywords=club['Keywords'].split(','))
    clubs_instances.append(club_instance)

# Créer une instance globale de mots-clés
keywords_instance = Keywords(KeywordCloud=keywords_data[0]['Keywords'])

# Créer des instances de Event_profile uniquement pour les événements futurs
events_instances = []
today = datetime.now()
for event in events_data:
    event_start_date = datetime.strptime(event['StartDate'], '%Y-%m-%d')
    if event_start_date > today:
        event_instance = Event_profile(
            EventID=event['EventID'],
            EventName=event['EventName'],
            EventType=event['EventType'],
            ClubName=event['ClubName'],
            EventDescription=event['EventDescription'],
            StartDate=event['StartDate'],
            EndDate=event['EndDate'],
            Location=event['Location']
        )
        events_instances.append(event_instance)

# Associer les mots-clés des clubs et les mots-clés globaux aux événements
for event in events_instances:
    for club in clubs_instances:
        if event.ClubName == club.ClubName:
            event.event_keywords.extend(club.club_keywords)
    # Ajouter les mots-clés globaux
    event.event_keywords.extend(keywords_instance.KeywordCloud)

# Vérifier les résultats
for event in events_instances:
    print(event)
    
#TEST
# Display all event instances with print
print("Complete list of events:")
for event in events_instances:
    print(event)

# Display a specific instance (e.g., the first one)
if events_instances:
    print("\nFirst instance:")
    print(events_instances[0])

# Display all instances with Streamlit
st.write("Complete list of events:")
for event in events_instances:
    st.write(event)

# Display a specific instance with Streamlit
if events_instances:
    st.write("\nFirst instance:")
    st.write(events_instances[0])

# Access specific attributes of an instance
if events_instances:
    print("\nAttributes of the first instance:")
    print(f"EventName: {events_instances[0].EventName}")
    print(f"StartDate: {events_instances[0].StartDate}")
    print(f"Keywords: {events_instances[0].event_keywords}")

    st.write("\nAttributes of the first instance:")
    st.write(f"EventName: {events_instances[0].EventName}")
    st.write(f"StartDate: {events_instances[0].StartDate}")
    st.write(f"Keywords: {events_instances[0].event_keywords}")

