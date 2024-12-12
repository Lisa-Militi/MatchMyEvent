import streamlit as st
from datetime import datetime
import re
#from exchangelib import Credentials, Account, CalendarItem, DELEGATE, EWSDateTime, EWSTimeZone
#from calendar_handler import handle_calendar_invite  #Current implementation attempts to use Microsoft Exchange Web Services (EWS)

user_keywords = st.session_state['user_keywords']
test_events = st.session_state['events_instances_list']



def preprocess_text(text): #normalize Text
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)  # removes tabs
    return text.lower().strip()


def calculate_kms(user_keywords, event_keywords):
    # Looks for matches between user keywords and event keywords
    matches = list(filter(lambda keyword: keyword.lower() in [kw.lower() for kw in event_keywords], user_keywords))
    match_count = len(matches)
    number_of_event_keywords = len(event_keywords)
    base_score = (match_count / number_of_event_keywords * 100) if number_of_event_keywords > 0 else 0
    
    #total_event_keywords = len(event_keywords)
    final_score = min(base_score, 100)  # Cap the score at 100%
    
    return final_score, matches


# Definition of the KMS bonus for event type match and language
def apply_event_type_bonus(kms, event_type_match):
    if event_type_match:
        bonus = 4 if kms <= 96 else (100 - kms)
        return min(kms + bonus, 100)
    return kms

def apply_language_bonus(kms, language_match):
    if language_match:
        bonus = 6 if kms <= 94 else (100 - kms)
        return min(kms + bonus, 100)
    return kms

# Match checks
def check_event_type_match(event_category, preferred_event_types):
    return event_category.lower() in [etype.lower() for etype in preferred_event_types]

def check_language_match(language, preferred_language):
    return language.lower() in [lang.lower() for lang in preferred_language]

# Preferred event and language types
preferred_event_types = st.session_state['event_categories']
preferred_language = st.session_state['language']

# Calculate and sort events
for event in test_events:
    event_kms, matches = calculate_kms(user_keywords, event.event_keywords)
    event_type_match = check_event_type_match(event.event_type, preferred_event_types)
    language_match = check_language_match(event.language, preferred_language)
    event.final_kms = apply_event_type_bonus(event_kms, event_type_match)
    event.final_kms = apply_language_bonus(event.final_kms, language_match)

sorted_events = sorted(test_events, key=lambda e: e.final_kms, reverse=True)[:5]

# HTML template for progress circle
def render_progress_circle(percentage):
    return f""" 
    <svg width="100" height="100" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
        <circle cx="18" cy="18" r="16" fill="none" stroke="#eee" stroke-width="4" />
        <circle cx="18" cy="18" r="16" fill="none" stroke="#008000" stroke-width="4"
            stroke-dasharray="{percentage}, 100" stroke-linecap="round" transform="rotate(-90 18 18)" />
        <text x="18" y="20.5" font-size="8" fill="#008000" text-anchor="middle" font-weight="bold">{percentage:.0f}%</text>
    </svg>
    """

# Helper to format the date and time
def format_date_time(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return dt.strftime("Date: %d.%m.%Y")
    except ValueError:
        return "Invalid Date"

def format_time(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return dt.strftime("%H:%M")
    except ValueError:
        return "Invalid Time"

description = event.description

# Helper to format description --> does not work yet
def preprocess_description(description):
    if not description:
        return "No description available."
    # Split the description into paragraphs
    paragraphs = description.split('\n\n')
    
    # Clean each paragraph
    cleaned_paragraphs = []
    for para in paragraphs:
        # Remove extra whitespace at start and end of paragraph
        cleaned_para = para.strip()
        # Replace multiple spaces with single space within the paragraph
        cleaned_para = re.sub(r'\s+', ' ', cleaned_para)
        
        # Only add non-empty paragraphs
        if cleaned_para:
            cleaned_paragraphs.append(cleaned_para)
    
    # Join paragraphs with double newline (HTML line break)
    return '<br><br>'.join(cleaned_paragraphs)


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

for rank, event in enumerate(sorted_events, start=1):
    formatted_date = format_date_time(event.startDate)
    formatted_start_time = format_time(event.startDate)
    formatted_end_time = format_time(event.endDate) if hasattr(event, 'endDate') and event.endDate else "Unknown"

    cleaned_description = preprocess_description(event.description)

    with st.container():
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
        
# CALENDAR BUTTON IMPLEMENTATION
    # Adds "Add to Calendar" button to each event
    # When clicked:
    # 1. Verifies user email exists
    # 2. Initiates Outlook connection if not exists
    # 3. Creates calendar event with event details
    # 4. Sends invitation to user's email

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Add Event to Outlook Calendar", key=f"outlook_{rank}"):
                if handle_calendar_invite(event):
                    st.success(f"Event {event.title} added to your calendar!")
        with col2:
            if st.button(f"👎 Dislike {event.title}", key=f"dislike_{rank}"):
                if event in st.session_state['events_instances_list']:
                    st.session_state['events_instances_list'].remove(event)
                    st.warning(f"Event '{event.title}' will be removed!")
                    st.rerun()
