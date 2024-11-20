import streamlit as st
import session_state_handler as sh
import pandas as pd

class Event_profile:

    def __init__(self, EventName, EventType, ClubName, ClubCategory, EventDescription, StartDate, EndDate, Location):
        self.EventName = event_name #string
        self.EventType = event_type #string
        self.ClubName = club_name #string
        self.ClubCategory = club_category #string
        self.EventDescription = event_description #string
        self.StartDate = start_date #datetime
        self.EndDate = end_date #datetime
        self.Location = location #string

        event_keywords = []


class Club:

    def __init__(self, ClubName, ClubCategory, ClubLanguage, SkillDevelopment, Interest):
        self.ClubName = club_name #string
        self.ClubCategory = club_category #string
        self.ClubLanguage = club_language #string
        self.SkillDevelopment = skill_development #string
        self.Interest = interest #string

        self.club_keywords = club_keywords #list

        club_keywords = []

class Keywords:

      def __init__(self, KeywordsCloud):
        self.KeywordsCloud = keywords
        keywords_cloud = []

#INSTANCES (objects of class Event_profile and Club)
#load excel files 
events_file = pd.read_csv(/Users/alice/Downloads/Events_file.csv)
clubs_file = pd.read_csv(/Users/alice/Downloads/Clubs_file.csv)
keywords_cloud_file = pd.read_csv(/Users/alice/Downloads/Keywords_Cloud_file.csv)

#lists to store objects
#TO BE ADDED TO SESSION STATES
events_instances = []
clubs_instances = []
keywords_cloud_instances = [] #there should only be one instance; technically the keyword cloud can be a hard-coded list, independent of sessions states

#Event_profile Objects
for _, row in events_file.iterrows():
    event_instance = Event_profile(
        EventName = row['event_name'],
        EventType = row['event_type'],
        EventLanguage = row['event_language'],
        ClubName = row['club_name'],
        ClubCategory = row['club_category'],
        EventDescription = row['event_description'],
        StartDate = row['start_date'],
        EndDate = row['end_date'],
        Location = row['location']
    )
    events_instances.append(event_instance)

# Club Objects
for _, row in clubs_file.iterrows():
    club_instance = Club(
        ClubName = row['club_name'],
        ClubCategory = row['club_category'],
        ClubLanguage = row['club_language'],
        SkillDevelopment = row['skill_development'],
        Interest = row['interest']
    )
    clubs_instances.append(club_instance)

# Keywords Cloud Objects
for _, row in keywords_cloud_file.iterrows():
    keyword_instance = Keywords(
        KeywordsCloud = row['keywords'],
    )
  keywords_cloud_instances.append(keyword_instance)

#FUNCTIONS
#this should be the other way around; however, all of the event_keywords should already be in the keywords_cloud
def merge_keywords(event_keywords, keywords_cloud):
    for keyword in keywords_cloud:
        event_keywords.append(keyword)




