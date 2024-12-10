import streamlit as st
import session_state_handler as sh
import pandas as pd
from datetime import datetime

#IMPORT ALL INSTANCES OF CLASSES
#import page, access as ml.test_major_BA._major_keywords
from multipage_layout import test_major_BA
from multipage_layout import test_major_Econ

# Explicitly initialize session state
#move to session_state_handler, import session states
for key, default_value in sh.session_state_dict.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

#hard-coded list of clubs for use in st-widget
STUDENT_CLUBS = [
    "AIESEC in St. Gallen", "CEMS Club St. Gallen", "Le Cercle des Francophones (CF)", 
    "Club Latino", "European Nations' Society (ENSo)", "Hungarian Society", 
    "Italian Club", "Model WTO", "East Slavic Club", "Scandinavian Society", 
    "St. Gallen Model United Nations (SGMUN)", "Turkish Business Club", 
    "Academic Surf Club", "Combat Sports Club", "Cycling Club", "HSG Sailing", 
    "Salsa & Latin Dance Club", "HSG Tennis Team", "HSG Debating Club", 
    "The Philosophy Club", "HSG Big Band", "Consulting Club", "Social Business Club", 
    "Tech Club", "FinTech Club", "Marketing Club", "Crypto Society", "Toastmasters"
]


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

#hard-coded list of languages for use in st-widget, would require a language-attribute in the event-instance to come up with multiplication factor for kms
LANGUAGES = [
    "English", "Spanish", "Italian", "German", "Turkish", "French"
]

'''
#hard-coded list of interests for use in st-widget; should be equal to keywords_cloud; import as variable form hard coded list in multipage_layout
INTERESTS = [
    "Artistic expression",
    "Business strategy",
    "Communication",
    "Creative thinking",
    "Critical analysis",
    "Entrepreneurship",
    "Event planning",
    "Innovation",
    "Leadership",
    "Management",
    "Negotiation",
    "Philosophy",
    "Presentation",
    "Problem-solving",
    "Project management",
    "Public speaking",
    "Research",
    "Social engagement",
    "Strategy",
    "Teamwork",
    "Workshops",
    "Arts",
    "Business",
    "Cultural awareness",
    "Diplomacy",
    "Economics",
    "Environment",
    "Global issues",
    "History",
    "Innovation",
    "International relations",
    "Language",
    "Literature",
    "Local culture",
    "Networking",
    "Philosophy",
    "Policy",
    "Politics",
    "Science",
    "Social justice",
    "Sustainability",
    "Technology",
    "Trading"
]
'''

INTERESTS = st.session_state['global_keyword_cloud']
'''
['Workshops', 'Volunteer Program',
 'Keynote Speech', 'Club Fair', 'Case Competition', 'Guest Lecture',
 'Sports Tournament', 'Fundraising', 'Career Fair', 'Social Gathering',
 'Tech Talks', 'HSG', 'Community', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community', 'Volunteer Program', 'Oikos', 'Panel Discussion',
 'Keynote Speech', 'Sustainability', 'Case Competition', 'Guest Lecture', 'Fundraising', 'Social Gathering',
 'Tech Talks', 'Alumni Meet', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community']
'''

#hard-coded list of interests for use in st-widget; should be equal to keywords_cloud; import as variable form hard coded list in multipage_layout
EVENT_TYPES = [
    "Introduction",
    "Sport",
    "Trip",
    "Panel discussion",
    "Party",
    "Recruitment",
    "Q&A",
    "Drink",
    "Networking",
    "Conference",
    "Drink/Introduction",
    "Workshop",
    "Beerpong Tournament",
    "Other",
    "Cultural",
    "Concert",
    "Giveaway",
    "Conference/Food and Wine Tasting",
    "Karaoke",
    "Food Tasting",
    "Food and Drink",
    "BBQ",
    "Olma Messen",
    "Lunch",
    "Kick-off",
    "Mini-Golf",
    "Info event",
    "Food and Wine Tasting"
]

     

def get_user_profile():
    st.subheader("User Profile")
    st.write("Please answer the questions below to create your User Profile")


    #NAME
    name_input = st.text_input("What is you name?", value=st.session_state['name'])
    if name_input != '':
        sh.update_name(name_input)
    
    
    #EMAIL ADDRESS
    email_input = st.text_input("What is your email address?", value=st.session_state['user_email'])
    if email_input != '':
        sh.update_email(email_input)

    #LANGUAGE
    language_input = st.multiselect("What is your preferred language(s)?", LANGUAGES)

    

    #MAJOR
    major_input = st.selectbox("What is your major?", ("-select-", "Bachelor: BA","Bachelor: Econ", "Bachelor: IA",
                                                                "Bachelor: BLE", "Bachelor: Computer Science"),) #to be completed
    if major_input != "-select-":
        sh.update_major(major_input)
    

    #CLUBS
    clubs_input = st.multiselect("Which clubs are you a member of or interested in?", STUDENT_CLUBS)
    


    #EVENT TYPES
    event_categories_input = st.multiselect("Select all event types you are interested in", EVENT_TYPES,)


    #INTERESTS = user_keywords
    interests_input = st.multiselect("Select your interests below", INTERESTS)



    
    #SAVE USER BUTTON
    #saves temporary lists to permanent session state variable
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
        sh.update_clubs_keywords

def reset_user():
    if st.button("Reset User"):
        sh.initiate_session_state()


#EXECUTION
get_user_profile()
reset_user()

#TEST ONLY - to be removed
st.subheader("TESTING")
st.write("TEST entries:")
st.write(st.session_state)


