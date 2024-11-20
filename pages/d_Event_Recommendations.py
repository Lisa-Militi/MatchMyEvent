import streamlit as st
import session_state_handler as sh


class Event_profile:

    def __init__(self, event_name, event_date, club_name, event_type, event_description, event_keywords):
        self.EventName = EventName #string
        self.EventType = EventType #string
        self.EventLanguage = EventLanguage #string
        self.ClubName = ClubName #string
        self.ClubCategory = ClubCategory #string
        self.EventDescription = EventDescription #string
        self.startDate = startDate #datetime
        self.endDate = endDate #datetime
        self.Location = Location #string

        self.event_keywords = event_keywords #list

        event_keywords = []


class Club:

    def __init__(self, ClubName, ClubCategory, ClubLanguage, SkillDevelopment, Interest):
        self.ClubName = ClubName #string
        self.ClubCategory = ClubCategory #string
        self.ClubLanguage = ClubLanguage #string
        self.SkillDevelopment = SkillDevelopment #string
        self.Interest = Interest #string

        self.club_keywords = club_keywords #list

        club_keywords = []


#TEST INSTANCES
test_event = Event_profile('Symposium', 'club_name', 'panel_discussion', 'this is where the description goes as a string', ['international', 'politics', 'economics'])

test_club = Club('HIC', ['finance', 'economics', 'banking'])



#FUNCTIONS
def merge_keywords(event_keywords, club_keywords):
    for keyword in club_keywords:
        event_keywords.append(keyword)




