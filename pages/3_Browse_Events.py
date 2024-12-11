import streamlit as st
import sqlite3
import session_state_handler as sh
from datetime import datetime
import pandas as pd
import Home as ml
#from multipage_layout import ml.events_instances
#from multipage_layout import Club
#from multipage_layout import Keywords
st.markdown(
    """
    <style>
    .centered {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("<h1 class=""centered"">Browse Events </h1>", unsafe_allow_html=True)

def format_date(date_str):
    """Convert a date string to format dd-mm-yyyy."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return date_str

def browse_events():
    st.subheader("Events per Club 2024")

    # Check if instances are loaded
    if not hasattr(ml, 'clubs_instances') or not hasattr(ml, 'events_instances'):
        st.error("Clubs or events data not loaded. Please check your setup in multipage_layout.")
        return

    # Get all club names
    club_names = [club.clubName for club in ml.clubs_instances]

    # Add a multiselect dropdown for clubs with no default selection
    selected_clubs = st.multiselect(
        "Select Clubs to Display:",
        options=sorted(club_names),
        default=[]  # Default: no clubs selected
    )

    # If no clubs are selected, display a message
    if not selected_clubs:
        st.info("Please select one or more clubs from the dropdown above.")
        return

    # Filter clubs based on selection
    filtered_clubs = [
        club for club in ml.clubs_instances if club.clubName in selected_clubs
    ]

    # Display clubs and their events
    for club in filtered_clubs:
        # Club name in green
        st.markdown(f"<h2 style='color: green;'>{club.clubName}</h2>", unsafe_allow_html=True)

        # Get events associated with the current club
        club_events = [event for event in ml.events_instances if event.clubName == club.clubName]
        
        if not club_events:
            st.write("No events available for this club.")
        else:
            for event in club_events:
                st.subheader(event.title)
                st.write(f"**Event Type**: {event.event_type}")
                st.write(f"**Start Date**: {format_date(event.startDate)}")
                st.write(f"**End Date**: {format_date(event.endDate)}")
                st.write(f"**Location**: {event.location_text}")
                st.write(f"**Language**: {event.language}")
                st.write(f"**Description**: {event.description}")
                st.markdown("---")
        
        # Add a green line separator after each club
        st.markdown("<hr style='border: 2px solid green;'>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    browse_events()
