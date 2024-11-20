
import d_Event_Recommendations as ER
import streamlit as st
import session_state_handler as sh
import csv

class Event_profile:
    def __init__(self, EventName, EventType, ClubName, ClubCategory, EventDescription, StartDate, EndDate, Location):
        self.EventName = EventName  # string
        self.EventType = EventType  # string
        self.ClubName = ClubName  # string
        self.ClubCategory = ClubCategory  # string
        self.EventDescription = EventDescription  # string
        self.StartDate = StartDate  # string (ou datetime si conversion)
        self.EndDate = EndDate  # string (ou datetime si conversion)
        self.Location = Location  # string
        self.event_keywords = []


class Club:
    def __init__(self, ClubName, ClubCategory, ClubLanguage, SkillDevelopment, Interest):
        self.ClubName = ClubName  # string
        self.ClubCategory = ClubCategory  # string
        self.ClubLanguage = ClubLanguage  # string
        self.SkillDevelopment = SkillDevelopment  # string
        self.Interest = Interest  # string
        self.club_keywords = []


class Keywords:
    def __init__(self, KeywordsCloud):
        self.KeywordsCloud = KeywordsCloud
        self.keywords_cloud = []


# Fonction pour lire un fichier CSV sans pandas
def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Lit le fichier CSV en tant que dictionnaires (colonnes -> clés)
        for row in reader:
            data.append(row)
    return data


# Charger les fichiers CSV
events_file = read_csv_file("/Users/alice/Downloads/Events_file.csv")
clubs_file = read_csv_file("/Users/alice/Downloads/Clubs_file.csv")
keywords_cloud_file = read_csv_file("/Users/alice/Downloads/Keywords_Cloud_file.csv")

# Listes pour stocker les objets
events_instances = []
clubs_instances = []
keywords_cloud_instances = []

# Création des objets Event_profile
for row in events_file:
    event_instance = Event_profile(
        EventName=row['event_name'],
        EventType=row['event_type'],
        ClubName=row['club_name'],
        ClubCategory=row['club_category'],
        EventDescription=row['event_description'],
        StartDate=row['start_date'],
        EndDate=row['end_date'],
        Location=row['location']
    )
    events_instances.append(event_instance)

# Création des objets Club
for row in clubs_file:
    club_instance = Club(
        ClubName=row['club_name'],
        ClubCategory=row['club_category'],
        ClubLanguage=row['club_language'],
        SkillDevelopment=row['skill_development'],
        Interest=row['interest']
    )
    clubs_instances.append(club_instance)

# Création des objets Keywords
for row in keywords_cloud_file:
    keyword_instance = Keywords(
        KeywordsCloud=row['keywords']
    )
    keywords_cloud_instances.append(keyword_instance)


# Fonction pour fusionner les mots-clés
def merge_keywords(event_keywords, keywords_cloud):
    for keyword in keywords_cloud:
        event_keywords.append(keyword)

#FUNCTIONS
#this should be the other way around; however, all of the event_keywords should already be in the keywords_cloud
#def merge_keywords(event_keywords, keywords_cloud):
    #for keyword in keywords_cloud:
        #event_keywords.append(keyword)

