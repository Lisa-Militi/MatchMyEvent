import streamlit as st
import sqlite3
import session_state_handler as sh
from datetime import datetime
import pandas as pd
import multipage_layout as ml
#from multipage_layout import ml.events_instances
#from multipage_layout import Club
#from multipage_layout import Keywords



# Vérifier les résultats
for event in ml.events_instances:
    print(event)
    
#TEST
# Display all event instances with print
'''
print("Complete list of events:")
for event in ml.events_instances:
    print(event)
'''
    

# Display a specific instance (e.g., the first one)
if ml.events_instances:
    print("\nFirst instance:")
    print(ml.events_instances[0])





# Access specific attributes of an instance
if ml.events_instances:
    print("\nAttributes of the first instance:")
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

import random
import pandas as pd
import streamlit as st

db_path = '/mnt/data/test_file_DB.db'

connection = sqlite3.connect(db_path)
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
FROM events_file
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
