import streamlit as st


#SESSION STATE DICTIONARY
session_state_dict = {
                        "name": '',
                        "major": '',
                        "event_categories": [],
                        "user_keywords": [],
                        "language": '-select-',
                        "selected_clubs": [],
                        "user_email" : ''
                        }


#MAJOR KEYWORD DICTIONARY
major_keyword_dict = {
                        "Bachelor: BA": ["consulting", "finance", "banking"],
                        "Bachelor: Econ": ["economics", "politics", "finance"],
                        "Bachelor: IA": ["international_affairs", "politics", "law", "economics"],
                        "Bachelor: BLE": [],
                        "Bachelor: Computer Science": ["technology"],
                      }

clubs_dict = {
                "AIESEC in St. Gallen": ['networking', 'international', 'economics'],
                "CEMS Club St. Gallen": ['international', "business", "finance"],
                "Le Cercle des Francophones (CF)": ['social', 'french', 'party']
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
    if 'language' not in st.session_state:
        st.session_state['language'] = []

    #SELECTED CLUBS
    if 'selected_clubs' not in st.session_state:
        st.session_state['selected_clubs'] = []

    #EMAIL ADDRESS
    if 'user_email' not in st.session_state:
        st.session_state['user_email'] = ''


#def initiate_session_state_new():
#    for key, default_value in session_state_dict.items():
#        if key not in st.session_state:
#            st.session_state[key] = default_value

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

def update_email(email_input):
    st.session_state['user_email'] = email_input

def update_major_keywords():
    major_keywords_list = []
    if st.session_state['major'] == "Bachelor: BA":
        major_keywords_list += major_keyword_dict["Bachelor: BA"]
    elif st.session_state['major'] == "Bachelor: Econ":
        major_keywords_list += major_keyword_dict["Bachelor: Econ"]
    elif st.session_state['major'] == "Bachelor: IA":
        major_keywords_list += major_keyword_dict["Bachelor: IA"]
    elif st.session_state['major'] == "Bachelor: BLE":
        major_keywords_list += major_keyword_dict["Bachelor: BLE"]
    elif st.session_state['major'] == "Bachelor: Computer Science":
        major_keywords_list += major_keyword_dict["Bachelor: Computer Science"]
    st.session_state['user_keywords'] += sorted(set(major_keywords_list))

#fix this    
def update_clubs_keywords():
    club_keywords_list = []
    for club, keywords in clubs_dict.items():
        if club in st.session_state['selected_clubs']:
            club_keywords_list.append(clubs_dict(keywords))
    st.session_state['user_keywords'] += club_keywords_list

