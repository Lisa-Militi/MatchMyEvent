import streamlit as st
import session_state_handler as sh


class Event_profile:

    def __init__(self, event_name, club_name, event_type, event_description, event_keywords):
        self.event_name = event_name #string
        self.club_name = club_name #string
        self.event_type = event_type #string
        self.event_description = event_description #string
        self.event_keywords = [] #list


class Club:

    def __init__(self, club_name, club_keywords):
        self.club_name = club_name #string
        self.club_keywords = [] #list


test_event = Event_profile('Symposium', 'panel_discussion', 'this is where the description goes as a string', ['international', 'politics', 'economics'])

test_club = Club('HIC', ['finance', 'economics', 'banking'])




def merge_keywords(event_keywords, club_keywords):
    for keyword in club_keywords:
        event_keywords.append(keyword)
