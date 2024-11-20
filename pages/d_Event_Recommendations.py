import streamlit as st
#import session_state_handler as sh
#import pandas as pd #not necessary

#load and display file (it did not work yet, so I implemented the list myself)
event_keywords = ['Volunteer Program', 'Oikos', 'Panel Discussion',
 'Keynote Speech', 'Sustainability', 'Case Competition', 'Guest Lecture', 'Fundraising', 'Social Gathering',
 'Tech Talks', 'Alumni Meet', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community']

st.write("### Event list Preview:")
st.dataframe(event_keywords)  # Interactive table

user_keywords = ['Workshops', 'Volunteer Program',
 'Keynote Speech', 'Club Fair', 'Case Competition', 'Guest Lecture',
 'Sports Tournament', 'Fundraising', 'Career Fair', 'Social Gathering',
 'Tech Talks', 'HSG', 'Community', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community']

st.write("### User list Preview:")
st.dataframe(user_keywords)  # Interactive table

#KMS CALCULATION
def calculate_kms(user_keywords, event_keywords): #will need to be changed to be values from instances
    matches = list(filter(lambda keyword: keyword in event_keywords, user_keywords))
    match_count = len(matches)
    total_keywords = len(user_keywords)
    match_rate = (match_count / total_keywords * 100) if total_keywords > 0 else 0
    return match_rate, matches
#may require session state

# definition of the kms bonus for event type match, adds 10% if kms is below 90
def apply_event_type_bonus(kms, event_type_match):
    if event_type_match == True:
        bonus = 10 if kms <= 90 else (100 - kms)
        return min(kms + bonus, 100)
    return kms

#event_type to be called from session states
#use list instead of dict
event_type_list = ["keynote", "seminar", "lecture", "conference"]
event_type = "keynote"
event_type_match = False

#CHANGE
def check_event_type_match(event_type, event_type_list, event_type_match):
    if event_type in event_type_list:
        event_type_match = True
    return event_type_match



# Calculate initial KMS das verstehe ich auch nicht
initial_kms, matches = calculate_kms(user_keywords, event_keywords)
print(f"Initial KMS: {initial_kms:.2f}%")
#print(f"Matched Keywords: {matches}")



# Apply event type bonus
event_type_match = check_event_type_match(event_type, event_type_list, event_type_match)
final_kms = apply_event_type_bonus(initial_kms, event_type_match)
print(f"Final KMS (with event type bonus): {final_kms:.2f}%")

match_rate, matches = calculate_kms(user_keywords,event_keywords)


progress_bar = st.progress(int(match_rate))

st.write(match_rate)
st.write(matches)




