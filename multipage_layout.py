import streamlit as st
import session_state_handler as ss_handler


ss_handler.initiate_session_state()

st.write("This temporarily serves as the data management page; this should be hidden")

#DEFINITION OF CLASS USER
class User:

    def __init__(self, user_name, user_major, user_event_categories, user_keywords):
        self.user_name = user_name
        self.user_major = user_major
        self._user_event_categories = []
        self._user_keywords = []



#DEFINITION OF CLASS MAJOR
class Major:

    def __init__(self, major, major_keywords):
        self._major = major
        self._major_keywords = []


#CLEARING SESSION STATES
def reset_session():
        if st.button("Reset all"):
            for key in st.session_state.keys():
                del st.session_state[key]




#MAJOR INSTANCES - CREATE SEPARATE SECTION WITH LISTS AND ONLY INCLUDE LIST VARIABLES IN INSTANCES
test_major_BA = Major("Bachelor: BA", ["consulting", "business", "finance"])
test_major_Econ = Major("Bachelor: Econ", ["economics", "finance", "sustainability"])






reset_session()