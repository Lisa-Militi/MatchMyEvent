import streamlit as st
from datetime import datetime
from exchangelib import Credentials, Account, CalendarItem, DELEGATE, EWSDateTime, EWSTimeZone
import re


user_keywords = st.session_state['user_keywords']
test_events = st.session_state['events_instances_list']


def preprocess_text(text): #normalize Text
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)  # removes tabs
    return text.lower().strip()

def calculate_kms(user_keywords, title, clubName, description): #kms mit skalierender formel
    title_keywords = preprocess_text(title).split()
    club_keywords = preprocess_text(clubName).split()
    description_keywords = preprocess_text(description).split()
    # Event-Keywords kombinieren
    event_keywords = title_keywords + club_keywords + description_keywords
    # Matches zwischen User-Keywords und Event-Keywords finden
    matches = [kw for kw in event_keywords if any(user_kw in kw for user_kw in user_keywords)]
    # Match-Rate berechnen (aggressiv skaliert)
    match_count = len(matches)
    total_event_keywords = len(event_keywords)
    # Neue Formel: Bonus für jeden Match und Gesamtgewichtung
    base_score = (match_count / max(total_event_keywords, 1)) * 100  # Basis-Score
    scaled_score = base_score + (match_count * 10)  # Zusätzliche Skalierung pro Match
    final_score = min(scaled_score, 100)  # Maximal auf 100 begrenzen
    return final_score, matches

# Definition of the KMS bonus for event type match and language
def apply_event_type_bonus(kms, event_type_match):
    if event_type_match:
        bonus = 10 if kms <= 90 else (100 - kms)
        return min(kms + bonus, 100)
    return kms

def apply_language_bonus(kms, language_match):
    if language_match:
        bonus = 15 if kms <= 85 else (100 - kms)
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
    event_kms, matches = calculate_kms(user_keywords, event.title, event.clubName, event.description)
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
        <circle cx="18" cy="18" r="16" fill="none" stroke="#007bff" stroke-width="4"
            stroke-dasharray="{percentage}, 100" stroke-linecap="round" transform="rotate(-90 18 18)" />
        <text x="18" y="20.5" font-size="8" fill="#007bff" text-anchor="middle" font-weight="bold">{percentage:.0f}%</text>
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
def format_description(description):
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

# Streamlit presentation
st.title("Top 5 Matched Events")

for rank, event in enumerate(sorted_events, start=1):
    formatted_date = format_date_time(event.startDate)
    formatted_start_time = format_time(event.startDate)
    formatted_end_time = format_time(event.endDate) if hasattr(event, 'endDate') and event.endDate else "Unknown"
    formatted_description = format_description(event.description)

    with st.container():
        st.markdown(
            f"""
            <div style="border: 2px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #ffffff; display: flex; align-items: center; justify-content: space-between;">
                <div style="flex: 1;">
                    <p style="font-weight: bold; color: #333; font-size: 14px;">Rank {rank}</p>
                    <h3 style="margin-bottom: 10px;">{event.title}</h3>
                    <p style="font-size: 14px; color: #333; margin: 0;">
                        <strong>Club:</strong> {event.clubName}
                    </p>
                    <div style="margin-bottom: 10px;"></div>
                    <p style="font-size: 14px; color: #555; margin: 0;">
                        <strong>{formatted_date}</strong>
                    </p>
                    <p style="font-size: 14px; color: #555; margin: 0;">
                        Time: {formatted_start_time} - {formatted_end_time}
                    </p>
                    <div style="margin-bottom: 15px;"></div>
                    <p style="font-size: 12px; color: #555; margin: 0;">
                        <strong>Description:</strong> {formatted_description}
                    </p>
                </div>
                <div style="flex: 0;">
                    {render_progress_circle(event.final_kms)}
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Add Event to Outlook Calendar", key=f"outlook_{rank}"):
                st.info(f"Event {event.title} added to Outlook Calendar!")
        with col2:
            if st.button(f"👎 Dislike {event.title}", key=f"dislike_{rank}"):
                if event in st.session_state['events_instances_list']:
                    st.session_state['events_instances_list'].remove(event)
                    st.warning(f"Event '{event.title}' will be removed!")
                    st.rerun()
