import streamlit as st
import session_state_handler as sh

#IMPORT ALL INSTANCES OF CLASSES
from multipage_layout import test_major_BA
from multipage_layout import test_major_Econ

def reset_event_categories():
    if st.button("Reset Event Categories"):
        st.session_state['event_categories'] = []
            

def get_user_profile():
    st.subheader("User Profile")
    st.write("Please answer the questions below to create your User Profile")


    #NAME
    name_input = st.text_input("What is you name?", value=st.session_state['name'])
    if name_input != '':
        sh.update_name(name_input)
    
    
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
