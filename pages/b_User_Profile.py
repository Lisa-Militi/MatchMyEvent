import streamlit as st
import session_state_handler as sh
import pandas as pd
import os
from datetime import datetime

#IMPORT ALL INSTANCES OF CLASSES
from multipage_layout import test_major_BA
from multipage_layout import test_major_Econ

# Explicitly initialize session state
for key, default_value in sh.session_state_dict.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


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

LANGUAGES = [
    "English", "Spanish", "Italian", "German", "Turkish", "French"
]

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

def reset_event_categories():
    if st.button("Reset Event Categories"):
        sh.update_event_categories([])

def get_user_profile():
    st.subheader("User Profile")
    st.write("Please answer the questions below to create your User Profile")


    #NAME
    # changed Use .get() method to prevent KeyError
    name_input = st.text_input("What is your name?", 
                                value=st.session_state.get('name', ''))
    if name_input != '':
        sh.update_name(name_input)

    #Language
    language_list = st.multiselect("Select yout language prefferences", 
                                LANGUAGES)

        
    st.session_state['selected_languages'] = language_list

    
    #MAJOR
    major_input = st.selectbox("What is your major?", ("-select-", "Bachelor: BA","Bachelor: Econ", "Bachelor: IA",
                                                                "Bachelor: Law & Econ", "Master: MacFin", "Master: MBI"),) #to be completed
    sh.update_major(major_input)

    if st.session_state['event_categories'] == "Bachelor: BA":
        for keyword in test_major_BA._major_keywords:
            sh.session_state_dict["user_keywords"] += keyword
    elif st.session_state['event_categories'] == "Bachelor: Econ":
        for keyword in test_major_Econ._major_keywords:
            sh.session_state_dict["user_keywords"] += keyword


    #CLUBS
    clubs_list = st.multiselect("Select the student clubs you are interested in", 
                                STUDENT_CLUBS)

        
    st.session_state['selected_clubs'] = clubs_list


    #INTEREST TYPES
    interest_list = st.multiselect("Select your interests", 
                                INTERESTS)
    
    st.session_state['selected_interests'] = interest_list


def add_save_button():
    if st.button("Confirm and Save Profile"):
        # Create dictionary with current session state values
        profile_data = {
            "name": st.session_state.get('name', ''),
            "major": st.session_state.get('major', ''),
            "event_categories": ','.join(st.session_state.get('event_categories', [])),
            "user_keywords": ','.join(st.session_state.get('user_keywords', [])),
            "language": ','.join(st.session_state.get('selected_languages', [])),
            "selected_clubs": ','.join(st.session_state.get('selected_clubs', [])),
            "selected_interests": ','.join(st.session_state.get('selected_interests', []))
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([profile_data])
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_profiles_{timestamp}.csv"
        
        # Save to CSV
        if not os.path.exists('user_profiles'):
            os.makedirs('user_profiles')
            
        filepath = os.path.join('user_profiles', filename)
        df.to_csv(filepath, index=False)
        
        st.success(f"Profile saved successfully to {filename}!")



get_user_profile()
add_save_button()


#st.write(type(test_user._user_event_categories))
#st.write(type(test_user._user_keywords))
#st.write(type(test_major_Econ._major_keywords))
