#import d_Event_Recommendations as ER
import streamlit as st
#import session_state_handler as sh
import csv


class Event_profile:
    def __init__(self, EventID, EventName, EventType, ClubName, EventDescription, StartDate, EndDate, Location):
        self.EventID = EventID
        self.EventName = EventName  # string
        self.EventType = EventType  # string
        self.ClubName = ClubName  # string
        self.EventDescription = EventDescription  # string
        self.StartDate = StartDate  # string (ou datetime si conversion)
        self.EndDate = EndDate  # string (ou datetime si conversion)
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




class Club:
    def __init__(self, ClubName, ClubLanguage, SkillDevelopment, Interest):
        self.ClubName = ClubName  # string
        self.ClubLanguage = ClubLanguage  # string
        self.SkillDevelopment = SkillDevelopment  # string
        self.Interest = Interest  # string
        self.club_keywords = []

    def __repr__(self):
        return (
            f"Club(ClubName={self.ClubName!r}, "
            f"ClubLanguage={self.ClubLanguage!r}, SkillDevelopment={self.SkillDevelopment!r}, "
            f"Interest={self.Interest!r})"
        )


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

