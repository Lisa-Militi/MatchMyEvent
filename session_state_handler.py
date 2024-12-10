import streamlit as st

# This is the session_state_handler file.  It is invisible to the user as it only serves as a coordinator for data being passed through the system.
# It contains all the session state infrastructure, consisting of the definition and initialization of the session states,
# as well as any functions that serve the purpose of updating or clearing session states.
# This page helps to coordinate information that needs to be saved during a session by using session states.
# It allows information to be stored centrally and to be called wherever needed through the use of st.session_state.
# This page further only contains one constant as well as all of the functions that are necessary that the session state infrastructure works.



# CONSTANTS

# The major-keyword dictionary contains the various Majors and Bachelor level as well as the keywords associated to them.
# This dictionary is hard coded as it is unlikely to change.
major_keyword_dict = {
    "Bachelor: BA": ["business", "accounting", "consulting", "marketing"],
    
    "Bachelor: Econ": ["philosophy", "economics", "finance"],
    
    "Bachelor: IA": ["diplomacy", "international_relations", 
                     "politics"],
    
    "Bachelor: BLE": ["business", "economics", "law"],
    
    "Bachelor: Computer Science": ["programming", "data_science", "technology"]
}



# FUNCTIONS

# The initiate_session_state-function initializes the session states by creating keys in the st.session_state dictionary.
# The function defines key-value pairs, where the keys are distinguished by a string and the value is created as an empty string or list, 
# depending on the variable type that will be associated with the respective session state
def initiate_session_state():
    #USER NAME
    if 'name' not in st.session_state:
        st.session_state['name'] = ''

    #USER MAJOR
    if 'major' not in st.session_state:
        st.session_state['major'] = ''

    #USER EVENT CATEGORIES LIST
    if 'event_categories' not in st.session_state:
        st.session_state['event_categories'] = []

    #USER KEYWORDS LIST
    if 'user_keywords' not in st.session_state:
        st.session_state['user_keywords'] = []

    #USER LANGUAGES LIST
    if 'language' not in st.session_state:
        st.session_state['language'] = []

    #SELECTED CLUBS
    if 'selected_clubs' not in st.session_state:
        st.session_state['selected_clubs'] = []

    #USER EMAIL ADDRESS
    if 'user_email' not in st.session_state:
        st.session_state['user_email'] = ''

    #EVENT INSTANCES LIST
    if 'events_instances_list' not in st.session_state:
        st.session_state['events_instances_list'] = []
    
    #EVENT CATEGORY VARIABLE
    if 'event_category' not in st.session_state:
        st.session_state['event_category'] = ''

    #EVENT RECOMMENDATIONS
    if 'event_recommendations_list' not in st.session_state:
        st.session_state['event_recommendations_list'] = []

    #GLOBAL KEYWORD CLOUD (list of all keywords allowed in the system)
    if 'global_keyword_cloud' not in st.session_state:
        st.session_state['global_keyword_cloud'] = []

    #CLUB INSTANCES LIST
    if 'club_instances_list' not in st.session_state:
        st.session_state['club_instances_list'] = []


#The following functions all take a temporary input variable and assign them to a session state to be stored more permanently
#These functions are all called in 2_User_Profile.py
#we distinguish "primary" and "secondary" session states in the user profile
#primary session states are created directly based on the user's inputs through streamlit widgets
#secondary session states are created based on previous inputs that in most cases are already assinged to session states
def update_name(name_input):
    st.session_state['name'] = name_input

def update_major(major_input):
    st.session_state['major'] = major_input

def update_event_categories(event_categories_input):
    st.session_state['event_categories'] = event_categories_input

#primary -> check redundancy
def update_user_keywords(user_keywords_input):
    st.session_state['user_keywords'] = user_keywords_input

def update_language(language_input):
    st.session_state['language'] = language_input

#primary
def update_selected_clubs(clubs_input):
    st.session_state['selected_clubs'] = clubs_input

#primary
def update_email(email_input):
    st.session_state['user_email'] = email_input

#secondary
def update_major_keywords():
    for major_name,major_keywords in major_keyword_dict.items():
        if st.session_state['major'] == major_name:    
            st.session_state['user_keywords'] += major_keywords

    
#primary
def update_interests(interests_input):
    st.session_state['user_keywords'] += interests_input

#secondary    
def update_clubs_keywords():
    local_club_instances = st.session_state['club_instances_list']
    club_keywords_list = []
    for club in local_club_instances:
        if club.clubName in st.session_state['selected_clubs']:
            club_keywords_list += club.InterestKeywords
    st.session_state['user_keywords'] += club_keywords_list

#reduce_user_keywords applies a simple set function to make sure that there are no duplicate keywords in the user_keywords session state list
def reduce_user_keywords():
    temp_user_keywords_list = set(st.session_state['user_keywords'])
    st.session_state['user_keywords'] = temp_user_keywords_list

#Browse_Events
#POTENTIAL FUNCTIONS TO BE ADDED
#def update_event_keywords(): #combines keywords from temporary keyword list (from keyword expander) with existing session state
#def update_events_instances_list(): save list to session state



#REMOVE AFTER TESTING

