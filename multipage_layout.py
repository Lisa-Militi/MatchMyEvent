import streamlit as st
import session_state_handler as sh
import sqlite3
from datetime import datetime
import pandas as pd


sh.initiate_session_state()

st.write("This temporarily serves as the data management page; this will be converted to the home page")
st.write("Instructions: please enter the file path of the database in line 84")

class Event_profile:
    def __init__(self, _id, title, event_type, clubName, description, startDate, endDate, location_text, language):
        self._id = _id
        self.title = title
        self.event_type = event_type
        self.clubName =clubName
        self.description = description
        self.startDate = startDate#datetime.strptime(startDate, '%Y-%m-%d')  # Conversion en datetime
        self.endDate = endDate#datetime.strptime(endDate, '%Y-%m-%d')  # Conversion en datetime
        self.location_text = location_text
        self.language = language
        self.event_keywords = []

    def __repr__(self):
        return (
            f"Event_profile(EventID={self._id!r}, EventName={self.title!r}, "
            f"EventType={self.event_type!r}, ClubName={self.clubName!r}, "
            f"StartDate={self.startDate!r}, EndDate={self.endDate!r}, Location={self.location_text!r}, language={self.language}"
            f"Keywords={self.event_keywords})"
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
    
# Classe pour les mots-clés globaux - NOT NECESSARY
class Keywords:
    def __init__(self, KeywordsCloud):
        self.KeywordCloud = KeywordsCloud.split(',') #check if split method works


    def __repr__(self):
        return f"KeywordCloud({self.KeywordCloud})"



#DEFINITION OF CLASS MAJOR
class Major:

    def __init__(self, major, major_keywords):
        self._major = major
        self._major_keywords = []

    def __repr__(self):
        return f"Major(major='{self._major}', major_keywords={self._major_keywords})"


#CLEARING SESSION STATES
def reset_session():
        if st.button("Reset all"):
            for key in st.session_state.keys():
                del st.session_state[key]
        sh.initiate_session_state()



#MAJOR INSTANCES - CREATE SEPARATE SECTION WITH LISTS AND ONLY INCLUDE LIST VARIABLES IN INSTANCES
test_major_BA = Major("Bachelor: BA", ["consulting", "business", "finance"])
test_major_Econ = Major("Bachelor: Econ", ["economics", "finance", "sustainability"])

db_path = r"C:\Users\leoru\OneDrive\Desktop\HSG\BA 3rd Semester\Computer Science\VS Computer Science\Test_Streamlit/test_file_DB.db"


connection = sqlite3.connect(db_path)

cur1 = connection.cursor()
events_data = cur1.execute('SELECT _id, EventName, EventType, ClubName, EventDescription, startDate, endDate, Location_1, Language FROM events_file')
cur2 = connection.cursor()
clubs_data = cur2.execute('SELECT clubName, InterestKeywords FROM club_profile_list')
cur3 = connection.cursor()
keywords_cloud_cursor = cur3.execute('SELECT keywords FROM keyword_cloud')

clubs_instances = []
for club in clubs_data:
    interest_keywords_temp = str(club[1])
    club_instance = Club(clubName=club[0], InterestKeywords=interest_keywords_temp.split(','))
    clubs_instances.append(club_instance)

# Créer une instance globale de mots-clés
#keywords_instance = Keywords(KeywordCloud=keywords_data[0]['Keywords'])
events_instances = []
for line in events_data:
    #event_start_date = datetime.strptime(event['startDate'], '%Y-%m-%d')
    if True == True: #event_start_date > today:
        event_instance = Event_profile(
            _id=line[0],
            title=line[1],
            event_type=line[2],
            clubName=line[3],
            description=line[4],
            startDate=line[5],
            endDate=line[6],
            location_text=line[7],
            language = line[8]
        )
        events_instances.append(event_instance)

for event in events_instances:
    for club in clubs_instances:
        if event.clubName == club.clubName:
            event.event_keywords.extend(club.InterestKeywords)

keywords_cloud = []
keywords_cloud = [row[0] for row in keywords_cloud_cursor]


'''
i_max = 0
i = 0

for value in keywords_cloud_tuple:
    i_max += 1
while i <= i_max:
    for value in keywords_cloud_tuple:
        keywords_cloud.append(keywords_cloud_tuple[i][0])
        i += 1
'''

#return events_instances#, clubs_instances, keywords_cloud
#SELECT _id, EventName, EventType, ClubName, EventDescription, startDate, endDate, Location_1, Language FROM Events_file


st.session_state['events_instances_list'] = events_instances
st.session_state['global_keyword_cloud'] = keywords_cloud





#reset_session()
