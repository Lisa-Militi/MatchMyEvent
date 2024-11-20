import streamlit as st
import pandas as pd

#load and display file 
event_list = ['Workshops', 'Volunteer Program', 'Hackathon', 'Panel Discussion',
 'Keynote Speech', 'Club Fair', 'Case Competition', 'Guest Lecture',
 'Sports Tournament', 'Fundraising', 'Career Fair', 'Social Gathering',
 'Tech Talks', 'Alumni Meet', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community']

st.write("### Event list Preview:")
st.dataframe(event_list)  # Interactive table

user_list = ['Workshops', 'Volunteer Program',
 'Keynote Speech', 'Club Fair', 'Case Competition', 'Guest Lecture',
 'Sports Tournament', 'Fundraising', 'Career Fair', 'Social Gathering',
 'Tech Talks', 'HSG', 'Community', 'Skill Development',
 'Entrepreneurship', 'Entrepreneurship', 'Sustainability',
 'Innovation Challenge', 'Community']

st.write("### User list Preview:")
st.dataframe(user_list)  # Interactive table




def calculate_kms(user_list, event_list): #or user_list and event_list or just list 1 & 2?
    matches = list(filter(lambda keyword: keyword in event_list, user_list))
    match_count = len(matches)
    total_keywords = len(user_list)
    match_rate = (match_count / total_keywords * 100) if total_keywords > 0 else 0
    return match_rate, matches

match_rate, matches = calculate_kms(user_list,event_list)


progress_bar = st.progress(int(match_rate))

st.write(match_rate)
st.write(matches)
"""
# definition of a new function to load the keywords from the csv file and return them as a list
def load_keywords(file):
    df = pd.read_csv(file, header=None) #assumes no Header in the file
    return df[0].str.strip().str.lower.tolist() #removes spaces and makes everything lowercase (wie funktioniert diese line?)

# definition to calculate the Keyword matching Score (KMS)
# it compares two lists of keywords and returns the percentage of matched kw
def calculate_kms(user_list, event_list): #or user_list and event_list or just list 1 & 2?
    matches = list(filter(lambda keyword: keyword in event_list, user_list))
    match_count = len(matches)
    total_keywords = len(user_list)
    match_rate = (match_count / total_keywords * 100) if total_keywords > 0 else 0
    return match_rate, matches

# definition of the kms bonus for event type match, adds 10% if kms is below 90
def apply_event_type_bonus(kms, event_type_match):
    if event_type_match=True:
        bonus = 10 if kms <= 90 else (100 - kms)
        return min(kms + bonus, 100)
    return kms


event_type_keywords = {
"conference": ["keynote", "seminar", "lecture", "conference"],
"workshop": ["workshop", "training", "bootcamp"],
"networking": ["networking", "meetup", "mixer"],
"party": ["party", "celebration", "gala"],
"cultural": ["festival", "art", "cultural"],
"sport": ["sport", "tournament", "game"],
"info event": ["info", "session", "orientation"],
"other": []
}

def detect_event_type(matches):
    for event_type, keywords in event_type_keywords.items():
        if any(keyword in matches for keyword in keywords):
            return event_type
    return "other"

if __name__ == "__main__": #das verstehe ich nicht ganz
# Load example files
    user_keywords = load_keywords("1CSTestList.csv")  # Example user file
    event_keywords = load_keywords("2CSTestList.csv")  # Example event file

# Calculate initial KMS das verstehe ich auch nicht
initial_kms, matches = calculate_kms(user_keywords, event_keywords)
print(f"Initial KMS: {initial_kms:.2f}%")
print(f"Matched Keywords: {matches}")

# Detect event type

detected_event_type = detect_event_type(matches)
print(f"Detected Event Type: {detected_event_type}")

# Apply event type bonus
event_type_match = detected_event_type != "other"  # Simulate a match
final_kms = apply_event_type_bonus(initial_kms, event_type_match)
print(f"Final KMS (with event type bonus): {final_kms:.2f}%")
"""