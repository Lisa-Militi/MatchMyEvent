# IMPORTS
import streamlit as st
import session_state_handler as sh
import pandas as pd
from datetime import datetime
import Home as ml

# CONSTANTS

keywords_cloud_user = st.session_state['global_keyword_cloud']

student_clubs_names_list = []

# This is a hard-coded list of languages for use in the st-widget used to select the User's languages.
# This list is hard coded as we do not expect any variations in the events file in the future.
languages_list = ["English", "Spanish", "Italian", "German", "Turkish", "French"]

# This is a hard-coded list of event types as included in data provided by SHSG in the respective database.
# As this list is definitive, we have decided to hard-code it.
event_types_list = [
    "Introduction", "Sport", "Trip", "Panel discussion", "Party", "Recruitment", "Q&A","Drink", "Networking",
    "Conference", "Drink/Introduction", "Workshop", "Beerpong Tournament", "Other", "Cultural", "Concert",
    "Giveaway", "Conference/Food and Wine Tasting", "Karaoke", "Food Tasting", "Food and Drink", "BBQ",
    "Olma Messen", "Lunch", "Kick-off", "Mini-Golf", "Info event","Food and Wine Tasting"
    ]


# FUNCTIONS

def get_student_clubs_list():
    for club in ml.clubs_instances:
        student_clubs_names_list.append(club.clubName)
    return student_clubs_names_list


#GET USER PROFLE FUNCTION: function to 
def get_user_profile():
    #NAME
    name_input = st.text_input("What is you name?", value=st.session_state['name'])
    if name_input != '':
        sh.update_name(name_input)
    
    st.divider()

    #EMAIL ADDRESS
    email_input = st.text_input("What is your email address?", value=st.session_state['user_email'])
    if email_input != '':
        sh.update_email(email_input)

    st.divider()

    #LANGUAGE
    language_input = st.multiselect("What is your preferred language(s)?", languages_list)

    st.divider()

    #MAJOR
    major_input = st.selectbox("What is your major?", ("-select-", "Bachelor: BA","Bachelor: Econ", "Bachelor: IA",
                                                                "Bachelor: BLE", "Bachelor: Computer Science"),) #to be completed
    if major_input != "-select-":
        sh.update_major(major_input)
    
    st.divider()

    #CLUBS - selection of multiple clubs
    clubs_input = st.multiselect("Which clubs are you a member of or interested in?", student_clubs_names_list)

    st.divider()

    #EVENT TYPES - selection of multiple event types, to be appended into user event_types list
    event_categories_input = st.multiselect("Which types of events are you interested in? Select all that apply to you!", event_types_list,)

    st.divider()

    #USER INTERESTS: selection of interests directly from keyword-cloud in the database, to be appended to user_keywords list
    interests_input = st.multiselect("Which of these topics are you most interested in? Select as many as you like!", keywords_cloud_user)

    #SAVE USER BUTTON: saves temporary lists to permanent session state variable
    #this avoids double enty
    if st.button("Save User Profile"):
        #PRIMARY SESSION STATE UPDATES
        #permanently save language input to session state
        sh.update_language(language_input)
        #save list of clubs into session state
        sh.update_selected_clubs(clubs_input)
        #save event categories input to session state
        sh.update_event_categories(event_categories_input)
        #save interests into user_keywords sessions state
        sh.update_interests(interests_input)

        #SECONDARY SESSION STATE UPDATES
        #save user_keywords based on selected major
        sh.update_major_keywords()
        #update list of user_keywords based on values in st.session_state['selected_clubs']
        sh.update_clubs_keywords()

        #USER_KEYWORDS CLEAN UP
        #apply set-method to user_keywords directly in the session state to eliminate duplicates
        sh.reduce_user_keywords()

        st.success('Your User Profile has been created! Check Event Recommendations to see your personalized suggestions!')

# reset_user allows the user to completely reset his user profile overriding all session states with empty strings and lists.
def reset_user():
    if st.button("Reset User"):
        st.session_state['name'] = ''
        st.session_state['major'] = ''
        st.session_state['event_categories'] = []
        st.session_state['user_keywords'] = []
        st.session_state['language'] = []
        st.session_state['selected_clubs'] = []
        st.session_state['user_email'] = ''
        st.info('User Profile has been reset: please re-enter you information')



#EXECUTION - combination of frontend and backend

st.title("User Profile")
st.subheader("Please answer the questions below to create your User Profile", anchor=None, help=None, divider="green",)

#execution of functions defined above
get_student_clubs_list()
get_user_profile()
reset_user()

#TEST ONLY: un-comment to see contents of session states
#st.subheader("TESTING")
#st.write("Session State dictionary content:")
#st.write(st.session_state)




