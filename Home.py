# Welcome to the backend of MatchMyEvent!

# Before you go on to examine this project, we would like to briefly explain the layout of this project.

# As should evident, this project makes use of a multipage layout to structure both the code and user interface,
# while also facilitating a way to split coding work between group members.

# This here is the entry-page into the multipage layout of the code; we recommend that you proceed to the session_state_handler-file next,
# and then move on to the rest of the actual pages as this will help to better understand this multipage-layout

# Regarding the structure of the code: all pages are structured after the following principle: Imports - Constants - Classes - Functions - Execution

# Besides being the entry page of the program, this page also serves the purpose of accessing the data from an sql-database
# The reason for this is that this page is inevitable the first page to load;
# feeding data into the system here makes sense as there is no need to perform any other action to ensure the readiness of the data
# On the front-end, this is only functions as an welcome- and information page without any further user interaction





from datetime import datetime
import pandas as pd
import sqlite3
import streamlit as st
import session_state_handler as sh

# CONTSTANTS
# DATABASE CONNECTION using sqlite3-library
# specification of file path using raw string; WHEN USING LOCAL COPIES, ENTER FILE PATH HERE
db_path = r"events_database.db"
connection = sqlite3.connect(db_path)

# using cursors to access data in the database
cur1 = connection.cursor()
events_data = cur1.execute('SELECT _id, EventName, EventType, ClubName, EventDescription, startDate, endDate, Location_1, Language, expanded_keywords FROM events_file')
cur2 = connection.cursor()
clubs_data = cur2.execute('SELECT clubName, InterestKeywords FROM club_profile_list')
cur3 = connection.cursor()
keywords_cloud_cursor = cur3.execute('SELECT keywords FROM keyword_cloud')

#this function defined in the session_state_handler-file initates the sessions states as soon as the file is opened
#this avoids session state key errors that might otherwise occur when other parts of the code are accessed before initializing session states
sh.initiate_session_state()

# CLASSES
# The Event-profile class defines events as well as their relevant attributes for further use in other pages, specifically Browse Events and Event Recommendations
class Event_profile:
    def __init__(self, _id, title, event_type, clubName, description, startDate, endDate, location_text, language, event_keywords):
        self._id = _id
        self.title = title
        self.event_type = event_type
        self.clubName = clubName
        self.description = description
        self.startDate = startDate#datetime.strptime(startDate, '%Y-%m-%d')  # Conversion en datetime
        self.endDate = endDate#datetime.strptime(endDate, '%Y-%m-%d')  # Conversion en datetime
        self.location_text = location_text
        self.language = language
        self.event_keywords = event_keywords
        self.event_keywords = []

    def __repr__(self):
        return (
            f"Event_profile(EventID={self._id!r}, title={self.title!r}, "
            f"event_type={self.event_type!r}, clubName={self.clubName!r}, "
            f"etartDate={self.startDate!r}, endDate={self.endDate!r}, location_text={self.location_text!r}, language={self.language}, "
            f"event_keywords={self.event_keywords})"
        )



# Classe pour les clubs
class Club:
    def __init__(self, clubName, InterestKeywords):
        self.clubName = clubName
        self.InterestKeywords = InterestKeywords
        InterestKeywords = []


    def __repr__(self):
            return (
                f"Club(ClubName={self.clubName!r}, club_keywords={self.InterestKeywords})"
            )

#FUNCTIONS

#CLEARING SESSION STATES
#deletes all session state values through iteration to reset the session
def reset_session():
        if st.button("Reset all"):
            for key in st.session_state.keys(): #change from keys to values
                del st.session_state[key]
        sh.initiate_session_state()



# EXECUTION - backend

#iterating through cursor list of clubs to create a list of club instances containing the clubs' names and associated keywords
clubs_instances = []
for club in clubs_data:
    interest_keywords_temp = str(club[1])
    club_instance = Club(clubName=club[0], InterestKeywords=interest_keywords_temp.split(', '))
    clubs_instances.append(club_instance)


#iterating through cursor-list to create a list of event profile instances by using the indices of the values in the cursor list
events_instances = []
fixed_date = datetime(2024, 10, 1, 0, 0, 0) #for demonstration purpses; fixed date to be removed if actual future events are to be displayed
for line in events_data:
    event_start_date = datetime.strptime(line[5], "%Y-%m-%dT%H:%M:%S.%fZ")
    if event_start_date > fixed_date: #can be replaced with datetime.now(): to view actual future events
        event_instance = Event_profile(
            _id = line[0],
            title = line[1],
            event_type= line[2],
            clubName = line[3],
            description = line[4],
            startDate = line[5],
            endDate = line[6],
            location_text = line[7],
            language = line[8],
            event_keywords = []
        )
        event_instance.event_keywords.append(str(line[9]).split(', '))
        for keyword in event_instance.event_keywords[0]:
            event_instance.event_keywords.append(keyword)
        event_instance.event_keywords.remove(event_instance.event_keywords[0])
        events_instances.append(event_instance)

for event in events_instances:
    for club in clubs_instances:
        if event.clubName == club.clubName:
            event.event_keywords.extend(club.InterestKeywords)
            #event.event_keywords += club.InterestKeywords

keywords_cloud = []
keywords_cloud = [row[0] for row in keywords_cloud_cursor]

#include set-function to reduce event keywords?

#assigning local list-variables to session states to facilitate global access and store data for the duration of the session
st.session_state['club_instances_list'] = clubs_instances
st.session_state['events_instances_list'] = events_instances
st.session_state['global_keyword_cloud'] = keywords_cloud


# EXECUTION - frontend
    
# Ajouter le style CSS pour centrer le contenu
st.markdown(
    """
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Contenu de la page avec la classe CSS centrée
st.markdown("<h1 class=""centered"">Welcome to MatchMyEvent :) </h1>", unsafe_allow_html=True)
st.markdown('<p class="centered">The webpage to guide you through HSG campus events</p>', unsafe_allow_html=True)
st.markdown('<h4 class="centered">Do you feel overwhelmed by the too big amount of clubs and events proposed at HSG?</h4>', unsafe_allow_html=True)

# URL brute de l'image
image_url = "MatchMyEvent Logo.png"

# Afficher l'image
st.image(image_url, use_column_width=True)
    
st.markdown('<h4 class="centered">Don\'t worry, this page\'s for you</h4>', unsafe_allow_html=True)
st.markdown('<p class="centered">We\'ve created an algorithm that will perfectly match your preferences</p>', unsafe_allow_html=True)



#reset_session()
