#import d_Event_Recommendations as ER
import streamlit as st
#import session_state_handler as sh
import csv
from datetime import datetime

class Event_profile:
    def __init__(self, EventID, EventName, EventType, ClubName, EventDescription, StartDate, EndDate, Location):
        self.EventID = EventID
        self.EventName = EventName  # string
        self.EventType = EventType  # string
        self.ClubName = ClubName  # string
        self.EventDescription = EventDescription  # string
        self.StartDate = datetime.strptime(StartDate, '%Y-%m-%d')  # string (ou datetime si conversion)
        self.EndDate = datetime.strptime(EndDate, '%Y-%m-%d')  # string (ou datetime si conversion)
        self.Location = Location  # string
        self.event_keywords = []

    def __repr__(self):
        return (
            f"Event_profile(EventID={self.EventID!r}, EventName={self.EventName!r}, "
            f"EventType={self.EventType!r}, ClubName={self.ClubName!r}, "
            f"StartDate={self.StartDate!r}, "
            f"EndDate={self.EndDate!r}, Location={self.Location!r})"
        )

#ADD KMS TO EVENT INSTANCE


class Keywords:
    def __init__(self, KeywordsCloud):
        self.KeywordsCloud = KeywordsCloud
        self.keywords_cloud = []


file_path_events = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Group 8 Project 20.11.2024\Events_file_updated.csv"
file_path_clubs = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Group 8 Project 20.11.2024\Clubs_file.csv"
file_path_keywords = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Group 8 Project 20.11.2024\Keywords_Cloud.csv"


# Fonction pour lire un fichier CSV sans pandas
def read_csv_file_events(file_path_events):
    events_file = []
    with open(file_path_events, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Lit le fichier CSV en tant que dictionnaires (colonnes -> clés) -> what exactly is the output of this?
        for row in reader:
            events_file.append(row)
    return events_file

def read_csv_file_clubs(file_path_clubs):
    clubs_file = []
    with open(file_path_clubs, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Lit le fichier CSV en tant que dictionnaires (colonnes -> clés)
        for row in reader:
            clubs_file.append(row)
    return clubs_file

def read_csv_file_keywords(file_path_keywords):
    keywords_cloud_file = []
    with open(file_path_keywords, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Lit le fichier CSV en tant que dictionnaires (colonnes -> clés)
        for row in reader:
            keywords_cloud_file.append(row)
    return keywords_cloud_file


# Charger les fichiers CSV
events_file = read_csv_file_events(file_path_events)
clubs_file = read_csv_file_clubs(file_path_clubs)
keywords_cloud_file = read_csv_file_keywords(file_path_keywords)


# Listes pour stocker les objets
events_instances = []
clubs_instances = []
keywords_cloud_instances = []

#print(type(events_file))
#print(events_file['_id;EventName;ClubName;ClubCategory;EventType;Language;EventDescription;startDate;endDate;Location;club;createdAt;updatedAt;__v;views;multiday;image;link;language2;type2;registration;video;location.coordinates.lat;location.coordinates.lng;location;isDeadline;sentScheduledNotifications;shouldSendScheduledNotifications;showInFeed;pinned;scheduledFor'])

#print(events_file[0]['_id;EventName;ClubName;ClubCategory;EventType;Language;EventDescription;startDate;endDate;Location;club;createdAt;updatedAt;__v;views;multiday;image;link;language2;type2;registration;video;location.coordinates.lat;location.coordinates.lng;location;isDeadline;sentScheduledNotifications;shouldSendScheduledNotifications;showInFeed;pinned;scheduledFor'])
print(clubs_file[0])
print('-'*100)
print(clubs_file[1])
#print(clubs_file[1]['ClubName'])



# Création des objets Event_profile
for row in events_file:
    event_instance = Event_profile(
        EventID = row['_id'],
        EventName = row['EventName'],
        EventType = row['EventType'],
        ClubName = row['ClubName'],
        ClubCategory = row['ClubCategory'],
        EventDescription = row['EventDescription'],
        StartDate = row['startDate'],
        EndDate = row['endDate'],
        Location = row['Location']
    )
    events_instances.append(event_instance)


# Création des objets Club
for row in clubs_file:
    club_instance = Club(
        ClubName=row['ClubName'],
        ClubCategory=row['ClubCategory'],
        ClubLanguage=row['ClubLanguage'],
        SkillDevelopment=row['SkillDevelopment'],
        Interest=row['Interest']
    )
    clubs_instances.append(club_instance)

# Création des objets Keywords
for row in keywords_cloud_file:
    keyword_instance = Keywords(
        KeywordsCloud=row['keywords']
    )
    keywords_cloud_instances.append(keyword_instance)

#merge club keywords into event_instance

#KEYWORD EXPANDER GOES HERE
#INPUT: event_instance.EventDescription and keywords_cloud, ouput: event_instance.event_keywords.append(keyword_output)




#FUNCTIONS
#this should be the other way around; however, all of the event_keywords should already be in the keywords_cloud
#def merge_keywords(event_keywords, keywords_cloud):
    #for keyword in keywords_cloud:
        #event_keywords.append(keyword)

'''
print(events_instances[0])
print(events_instances[1])
print("-"*30)
print(clubs_instances[0])
print(clubs_instances[1])
'''

# Classe pour les événements
class Event_profile:
    def __init__(self, EventID, EventName, EventType, ClubName, EventDescription, StartDate, EndDate, Location):
        self.EventID = EventID
        self.EventName = EventName
        self.EventType = EventType
        self.ClubName = ClubName
        self.EventDescription = EventDescription
        self.StartDate = datetime.strptime(StartDate, '%Y-%m-%d')  # Conversion en datetime
        self.EndDate = datetime.strptime(EndDate, '%Y-%m-%d')  # Conversion en datetime
        self.Location = Location
        self.event_keywords = []

    def __repr__(self):
        return (
            f"Event_profile(EventID={self.EventID!r}, EventName={self.EventName!r}, "
            f"EventType={self.EventType!r}, ClubName={self.ClubName!r}, "
            f"StartDate={self.StartDate!r}, EndDate={self.EndDate!r}, Location={self.Location!r}, "
            f"Keywords={self.event_keywords})"
        )

# Classe pour les clubs
class Club:
    def __init__(self, ClubName, club_keywords):
        self.ClubName = ClubName
        self.club_keywords = club_keywords

# Classe pour les mots-clés globaux
class Keywords:
    def __init__(self, KeywordsCloud):
        self.KeywordsCloud = KeywordsCloud.split(',')

    def __repr__(self):
        return f"KeywordsCloud({self.KeywordsCloud})"

# Fonction pour lire les fichiers CSV
def read_csv_file(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Charger les fichiers CSV
file_path_events = 'events.csv'  # Remplace par le chemin réel
file_path_clubs = 'clubs.csv'   # Remplace par le chemin réel
file_path_keywords = 'keywords.csv'  # Remplace par le chemin réel

# Lecture des données
events_data = read_csv_file(file_path_events)
clubs_data = read_csv_file(file_path_clubs)
keywords_data = read_csv_file(file_path_keywords)

# Créer des instances de Club
clubs_instances = []
for club in clubs_data:
    club_instance = Club(ClubName=club['ClubName'], club_keywords=club['Keywords'].split(','))
    clubs_instances.append(club_instance)

# Créer une instance globale de mots-clés
keywords_instance = Keywords(KeywordsCloud=keywords_data[0]['Keywords'])

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
    event.event_keywords.extend(keywords_instance.KeywordsCloud)

# Vérifier les résultats
for event in events_instances:
    print(event)

