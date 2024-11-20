import streamlit as st
import session_state_handler as sh

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


    #EVENT TYPES
    temp_list = st.multiselect("Select all event types you are interested in", ["networking", "social", "workshop", "career", "podium_discussion"],)
    if st.button("Confirm"):
        event_categories_input = sorted(set(temp_list))
        sh.update_event_categories(event_categories_input)

    reset_event_categories()


    #TEST ONLY - to be removed
    st.subheader("TESTING")
    st.write("TEST entries:")
    st.write(st.session_state)



get_user_profile()

#st.write(type(test_user._user_event_categories))
#st.write(type(test_user._user_keywords))
#st.write(type(test_major_Econ._major_keywords))
