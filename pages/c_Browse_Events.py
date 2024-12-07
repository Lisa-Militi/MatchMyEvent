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

import sqlite3
import pandas as pd
import streamlit as st

# Charger la base de données SQLite
db_path = 'test_file_DB.db'

# Fonction pour charger les données de la base de données
def load_data():
    with sqlite3.connect(db_path) as conn:
        query = """
        SELECT 
            ClubName,
            EventName, 
            EventType, 
            EventDescription, 
            startDate, 
            endDate, 
            Language
        FROM events_table
        """
        df = pd.read_sql_query(query, conn)
    return df

# Charger les données
data = load_data()

# Grouper les données par club
clubs = data['ClubName'].unique()

# Créer une interface Streamlit
st.title("Événements par club")

# Afficher les tableaux pour chaque club
for club in clubs:
    st.subheader(f"Événements organisés par {club}")
    club_data = data[data['ClubName'] == club]
    st.dataframe(club_data[['EventName', 'EventType', 'EventDescription', 'startDate', 'endDate', 'Language']])


