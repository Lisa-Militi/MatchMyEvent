import streamlit as st
#import session_state_handler as sh
#import pandas as pd #not necessary


user_keywords = ['Workshops', 'Volunteer Program',
 'Keynote Speech', 'Club Fair', 'Case Competition', 'Guest Lecture',
 'Sports Tournament', 'Fundraising', 'Career Fair', 'Social Gathering',
 'Tech Talks', 'HSG', 'Community', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community', 'Volunteer Program', 'Oikos', 'Panel Discussion',
 'Keynote Speech', 'Sustainability', 'Case Competition', 'Guest Lecture', 'Fundraising', 'Social Gathering',
 'Tech Talks', 'Alumni Meet', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community']

#st.write("### User list Preview:")
#st.dataframe(user_keywords)   Interactive table

class test_event():
    def __init__(self, name, event_keywords, event_category): #chatgpt meinte ich soll final kms nicht hier machen
        self.name = name
        self.event_keywords = event_keywords
        self.event_category = event_category
        self.final_kms = 0

    def __repr__(self):
        return f"TestEvent(name={self.name}, final_kms={self.final_kms:.2f}%)"
    
#sample events
test_event1 = test_event('Club_Fair', ['social', 'Entrepreneurship', 'Sustainability', 'Innovation Challenge', 'Community'], 'lecture')
test_event2 = test_event('Real_Estate_Night', ['Business','Social Gathering',
 'Tech Talks', 'HSG'], 'conference')
test_event3 = test_event('Beer_Pong', ['Pieces', 'Community','Fundraising', 'Sports Tournament'], 'seminar') 

test_events = [test_event1, test_event2, test_event3]

#KMS CALCULATION
def calculate_kms(user_keywords, event_keywords): #will need to be changed to be values from instances
    matches = list(filter(lambda keyword: keyword.lower() in [kw.lower() for kw in event_keywords], user_keywords))
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

#den match überprüfen
def check_event_type_match(event_category, preferred_event_types):
    return event_category.lower() in [etype.lower() for etype in preferred_event_types]

# Preferred event types
preferred_event_types = ["keynote", "seminar", "lecture", "conference"]

for event in test_events:
    # Calculate initial KMS
    event_kms, matches = calculate_kms(user_keywords, event.event_keywords)
    
    # Check for event type match
    event_type_match = check_event_type_match(event.event_category, preferred_event_types)
    
    # Apply bonus
    event.final_kms = apply_event_type_bonus(event_kms, event_type_match)

# Sort events by final KMS in descending order
sorted_events = sorted(test_events, key=lambda e: e.final_kms, reverse=True)

# Display sorted events
st.write("### Your personal recommendations:")

for event in sorted_events:
    # Display event name and KMS
    st.write(f"Event: {event.name}, Match: {event.final_kms:.2f}%")
    
    # Display progress bar for the event's KMS
    progress_bar = st.progress(int(event.final_kms))



