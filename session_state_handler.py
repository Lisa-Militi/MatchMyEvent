import streamlit as st

#SESSION STATE DICTIONARY
session_state_dict = {
                        "name": '',
                        "major": '',
                        "event_categories": [],
                        "user_keywords": [],
                         "language": '-select-',
                        "selected_clubs": []
                        }


def initiate_session_state():
    #NAME
    if 'name' not in st.session_state:
        st.session_state['name'] = ''

    #MAJOR
    if 'major' not in st.session_state:
        st.session_state['major'] = ''

    #EVENT CATEGORIES LIST
    if 'event_categories' not in st.session_state:
        st.session_state['event_categories'] = []

    #USER KEYWORDS LIST
    if 'user_keywords' not in st.session_state:
        st.session_state['user_keywords'] = []

    #LANGUAGE
    if 'selected_language' not in st.session_state:
        st.session_state['selected_language'] = []

    #SELECTED CLUBS
    if 'selected_clubs' not in st.session_state:
        st.session_state['selected_clubs'] = []



#FUNCTIONS
def update_name(name_input):
    st.session_state['name'] = name_input

def update_major(major_input):
    st.session_state['major'] = major_input

def update_event_categories(event_categories_input):
    st.session_state['event_categories'] = event_categories_input

def update_user_keywords(user_keywords_input):
    st.session_state['user_keywords'] = user_keywords_input

def update_language(language_input):
    st.session_state['language'] = language_input

def update_selected_clubs(clubs_input):
    st.session_state['selected_clubs'] = clubs_input