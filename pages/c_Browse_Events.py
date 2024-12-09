import streamlit as st
import sqlite3
import session_state_handler as sh
from datetime import datetime
import pandas as pd
import multipage_layout as ml
#from multipage_layout import ml.events_instances
#from multipage_layout import Club
#from multipage_layout import Keywords

st.title('Events Browser')
    
st.header('Complete list of events per clubs:')

#Clubs
#do it through calling the instances
if ml.clubs_instances:
    def display_clubs(clubs_data):
        for clubName in clubs_instances:
             print(f"Club: {ml.clubs_instances[0].clubName}")
st.header("{ml.clubs_instances[0].clubName}")            
st.header("Aargauer Verein", divider="gray")
st.header("ACM at the HSG", divider=True)
st.header("Academic SurfClub", divider=True)
st.header("Ad-Hoc Economics", divider=True)
st.header("Africa Association", divider=True)
st.header("Akademikerhaus", divider=True)
st.header("Albanian Student Association", divider=True)
st.header("Amnesty International", divider=True)
st.header("Amplify", divider=True)
st.header("Asia Club", divider=True)
st.header("Athletes Club", divider=True)
st.header("AV Kybelia", divider=True)
st.header("AV Mercuria", divider=True)
st.header("AV Steinacher", divider=True)
st.header("Aviation Club", divider=True)
st.header("BereichG", divider=True)
st.header("Bernerverein", divider=True)
st.header("Calanda B√ºndnerverein", divider=True)
st.header("Cercles des Francophones", divider=True)
st.header("Club Latino", divider=True)
st.header("Consulting Club", divider=True)
st.header("DocNet", divider=True)
st.header("ELSA", divider=True)
st.header("Esprit", divider=True)
st.header("ETHSG", divider=True)
st.header("Family Business Club", divider=True)
st.header("FLUX", divider=True)
st.header("Foraus St. Gallen", divider=True)
st.header("Healthcare Club", divider=True)
st.header("HIC", divider=True)
st.header("HSG Alumni", divider=True)
st.header("HSG Big Band", divider=True)
st.header("ICG", divider=True)
st.header("Impulse Network", divider=True)
st.header("Innovis VC", divider=True)
st.header("Italian Club", divider=True)
st.header("Marketing Club", divider=True)
st.header("MSASG (Muslim Students Association St. Gallen)", divider=True)
st.header("NEO Network", divider=True)
st.header("COrchester der Universität St. Gallen", divider=True)

st.header("Club Latino", divider=True)
st.header("Consulting Club", divider=True)
st.header("DocNet", divider=True)
st.header("ELSA", divider=True)
st.header("Esprit", divider=True)
st.header("ETHSG", divider=True)
st.header("Family Business Club", divider=True)
st.header("FLUX", divider=True)
st.header("Foraus St. Gallen", divider=True)
st.header("Healthcare Club", divider=True)
st.header("HIC", divider=True)
st.header("HSG Alumni", divider=True)
st.header("HSG Big Band", divider=True)
st.header("ICG", divider=True)
st.header("Impulse Network", divider=True)
st.header("Innovis VC", divider=True)
st.header("Italian Club", divider=True)
st.header("Marketing Club", divider=True)


if ml.events_instances:
    st.write("\nAttributes of the first instance:")
    print(f"EventName: {ml.events_instances[0].title}")
    print(f"StartDate: {ml.events_instances[0].startDate}")
    print(f"Event Type: {ml.events_instances[0].event_type}")
    print(f"Keywords: {ml.events_instances[0].event_keywords}")
    print(f"Description: {ml.events_instances[0].description}")

    st.write("\nAttributes of the first instance:")
    st.write(f"EventName: {ml.events_instances[0].title}")
    st.write(f"Event Type: {ml.events_instances[0].event_type}")
    st.write(f"StartDate: {ml.events_instances[0].startDate}")
    st.write(f"Keywords: {ml.events_instances[0].event_keywords}")
    st.write(f"Description: {ml.events_instances[0].description}")

st.session_state['ml.events_instances_list'] = ml.events_instances

db_path = r"test_file_DB.db"


connection = sqlite3.connect(db_path)

cur1 = connection.cursor()
events_data = cur1.execute('SELECT _id, EventName, EventType, ClubName, EventDescription, startDate, endDate, Location_1, Language FROM events_file')
cur2 = connection.cursor()
clubs_data = cur2.execute('SELECT clubName, InterestKeywords FROM club_profile_list')
cur3 = connection.cursor()
keywords_cloud_cursor = cur3.execute('SELECT keywords FROM keyword_cloud')

query = """
SELECT 
    EventName, 
    ClubName, 
    ClubCategory, 
    EventType, 
    Language, 
    EventDescription, 
    startDate, 
    endDate, 
    Location_1
FROM events_data
"""
events_df = pd.read_sql_query(query, connection)
connection.close()

st.dataframe(
    events_df,
    column_config={
        "ClubName": "Club",
        "EventName": "Event",
        "startDate": "Start",
        "endDate": "End",
        "EventType": "Type",
        "Language": "Language",
        "EventDescription": "Description",
        "Location_1": "Location",
    },
    hide_index=True,
)
