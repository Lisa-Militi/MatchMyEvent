import streamlit as st
from datetime import datetime #is for date and time handling with the Event duration
import re #for text preprocessing
#from exchangelib import Credentials, Account, CalendarItem, DELEGATE, EWSDateTime, EWSTimeZone
#from calendar_handler import handle_calendar_invite  #Current implementation attempts to use Microsoft Exchange Web Services (EWS)

# the user and event keywords get retrieved
user_keywords = st.session_state['user_keywords']
test_events = st.session_state['events_instances_list']

def preprocess_text(text): #removes special caracters and extra spaces from input text
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip() # returns the cleaned and normalized text

# KMS = Keyword Matching Score
# Calculation of how well an event matches the usere's preferences
def calculate_kms(user_keywords, event_keywords):
    # Looks for matches between user keywords and event keywords
    matches = list(filter(lambda keyword: keyword.lower() in [kw.lower() for kw in event_keywords], user_keywords))
    # counts total matches and total keywords:
    match_count = len(matches)
    number_of_event_keywords = len(event_keywords)
    # calculates the KMS score
    base_score = (match_count / number_of_event_keywords * 100) if number_of_event_keywords > 0 else 0
    final_score = min(base_score, 100)  # Cap the score at 100%
    return final_score, matches


# Applies a bonus of 4% to the KMS if the event type matches the user's preference
def apply_event_type_bonus(kms, event_type_match):
    if event_type_match:
        bonus = 4 if kms <= 96 else (100 - kms)
        return min(kms + bonus, 100)
    return kms

# Applies a bonus of 6% to the KMS if the language matches the user's preference
def apply_language_bonus(kms, language_match):
    if language_match:
        bonus = 6 if kms <= 94 else (100 - kms)
        return min(kms + bonus, 100)
    return kms

# checks if the event category or language matches the users preferences
def check_event_type_match(event_category, preferred_event_types):
    return event_category.lower() in [etype.lower() for etype in preferred_event_types]

def check_language_match(language, preferred_language):
    return language.lower() in [lang.lower() for lang in preferred_language]

# Preferred event and language types
preferred_event_types = st.session_state['event_categories']
preferred_language = st.session_state['language']

# Loops trough each event
for event in test_events:
    # calculates the events KMS and checks for type and language matches
    event_kms, matches = calculate_kms(user_keywords, event.event_keywords)
    event_type_match = check_event_type_match(event.event_type, preferred_event_types)
    language_match = check_language_match(event.language, preferred_language)
    # applies bonuses to the events KMS
    event.final_kms = apply_event_type_bonus(event_kms, event_type_match)
    event.final_kms = apply_language_bonus(event.final_kms, language_match)
# sorts the events by KMS and selects top 5
sorted_events = sorted(test_events, key=lambda e: e.final_kms, reverse=True)[:5]

# renders a circular progress indicator for the KMS score
def render_progress_circle(percentage):
    # HTML Code was made with ChatGPT
    return f""" 
    <svg width="100" height="100" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
        <circle cx="18" cy="18" r="16" fill="none" stroke="#eee" stroke-width="4" />
        <circle cx="18" cy="18" r="16" fill="none" stroke="#008000" stroke-width="4"
            stroke-dasharray="{percentage}, 100" stroke-linecap="round" transform="rotate(-90 18 18)" />
        <text x="18" y="20.5" font-size="8" fill="#008000" text-anchor="middle" font-weight="bold">{percentage:.0f}%</text>
    </svg>
    """

# converts the date string to an easy readable format
def format_date_time(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return dt.strftime("Date: %d.%m.%Y")
    except ValueError:
        return "Invalid Date"

# extracts time from date string
def format_time(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return dt.strftime("%H:%M")
    except ValueError:
        return "Invalid Time"

description = event.description

# splits and cleans the description text into HTML friendly paragraphs --> does not work (/n)
def preprocess_description(description):
    if not description:
        return "No description available."
    # Split the description into paragraphs
    paragraphs = description.split('\n\n')
    
    # clean each paragraph
    cleaned_paragraphs = []
    for para in paragraphs:
        # remove extra whitespace at start and end of paragraph
        cleaned_para = para.strip()
        # replace multiple spaces with single space within the paragraph
        cleaned_para = re.sub(r'\s+', ' ', cleaned_para)
        
        # Only add non-empty paragraphs
        if cleaned_para:
            cleaned_paragraphs.append(cleaned_para)
    
    # Join paragraphs with double newline (HTML line break)
    return '<br><br>'.join(cleaned_paragraphs)

# made with ChatGPT:
st.markdown(
    """
    <style>
    .event-container {
        position: relative; /* Ensures child elements with 'absolute' positioning are aligned to this container */
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 15px; /* Padding to ensure space inside the container */
        margin-bottom: 20px;
        background-color: #ffffff;
        overflow: hidden; /* Prevents content from spilling out of the box */
    }
    .progress-circle {
        position: absolute; /* Positions the circle relative to the parent */
        top: 15px; /* Adjust vertical position */
        right: 15px; /* Adjust horizontal position */
        width: 100px; /* Increased size of the circle */
        height: 100px; /* Match width for a perfect circle */
    }
    .event-details {
        margin-right: 120px; /* Ensures no text overlaps the progress circle */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit presentation
st.title("Top 5 Matched Events")
# iterates over the top 5 events
for rank, event in enumerate(sorted_events, start=1):
    formatted_date = format_date_time(event.startDate)
    formatted_start_time = format_time(event.startDate)
    formatted_end_time = format_time(event.endDate) if hasattr(event, 'endDate') and event.endDate else "Unknown"

    cleaned_description = preprocess_description(event.description)
    # displays event details including the progress circle in a box
    with st.container():# made with ChatGPT
        st.markdown(
            f"""
            <div class="event-container">
                <div class="event-details">
                    <p style="font-weight: bold; color: #333; font-size: 14px;">Rank {rank}</p>
                    <h3 style="margin-bottom: 10px;">{event.title}</h3>
                    <p style="font-size: 14px; color: #333; margin: 0;">
                        <strong>Club:</strong> {event.clubName}
                    </p>
                    <p style="font-size: 14px; color: #555; margin: 0;">
                        <strong>{formatted_date}</strong>
                    </p>
                    <p style="font-size: 14px; color: #555; margin: 0;">
                        Time: {formatted_start_time} - {formatted_end_time}
                    </p>
                    <p style="font-size: 12px; color: #555; margin: 0;">
                        <strong>Description:</strong> {cleaned_description}
                    </p>
                </div>
                <div class="progress-circle">
                    {render_progress_circle(event.final_kms)}
            """,
            unsafe_allow_html=True,
        )

        # adds buttons for each event to add it to the outlook calendar or remove it from the list
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Add to Calendar", key=f"calendar_{event.title}"):
                    #st.write("1. Button clicked")  # Debug print
                    if st.session_state['user_email']:
                        st.write(f"2. Found email: {st.session_state['user_email']}")  # Debug print
                    else:
                        st.write("2. No email found")  # Debug print
                    #try:
                        #result = handle_calendar_invite(event)
                        #st.write(f"3. Calendar invite result: {result}")  # Debug print
                            #if result:
                        #st.success(f"Event {event.title} added to your calendar!")
                    #except Exception as e:
                        #st.write(f"3. Error occurred: {str(e)}")  # Debug print
                    
                    #st.markdown("---")
        #removes the event from the list if the user dislikes it
        with col2:
            if st.button(f"👎 Dislike {event.title}", key=f"dislike_{rank}"):
                if event in st.session_state['events_instances_list']:
                    st.session_state['events_instances_list'].remove(event)
                    st.warning(f"Event '{event.title}' will be removed!")
                    st.rerun()
