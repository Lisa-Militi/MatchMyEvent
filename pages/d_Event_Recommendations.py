import streamlit as st
import session_state_handler as sh


class Event_profile:

    def __init__(self, event_name, event_type, event_language, club_name, club_name, club_category, event_description, start_date, end_date, location):
        self.EventName = event_name #string
        self.EventType = event_type #string
        self.ClubName = club_name #string
        self.ClubCategory = club_category #string
        self.EventDescription = event_description #string
        self.startDate = start_date #datetime
        self.endDate = end_date #datetime
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


#INSTANCES
Event1 = Event_profile('üß† Memory Clear Jan. 30th', 'club_name', 'panel_discussion', 'this is where the description goes as a string', ['international', 'politics', 'economics'])

test_club = Club('HIC', ['finance', 'economics', 'banking'])



#FUNCTIONS
def merge_keywords(event_keywords, club_keywords):
    for keyword in club_keywords:
        event_keywords.append(keyword)




