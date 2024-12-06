import streamlit as st
#import session_state_handler as sh
#import pandas as pd #not necessary




#st.write("### User list Preview:")
#st.dataframe(user_keywords)   Interactive table

class test_event():
    def __init__(self, title, event_keywords, event_category): #chatgpt meinte ich soll final kms nicht hier machen
        self.title = title
        self.event_keywords = event_keywords
        self.event_category = event_category
        self.final_kms = 0

    def __repr__(self):
        return f"TestEvent(title={self.title}, final_kms={self.final_kms:.2f}%)"
    
#sample events
'''
test_event1 = test_event('Club_Fair', ['social', 'Entrepreneurship', 'Sustainability', 'Innovation Challenge', 'Community'], 'lecture')
test_event2 = test_event('Real_Estate_Night', ['Business','Social Gathering',
 'Tech Talks', 'HSG'], 'conference')
test_event3 = test_event('Beer_Pong', ['Pieces', 'Community','Fundraising', 'Sports Tourtitlent'], 'seminar') 
test_event4 = test_event('Hackathon_Night', ['Innovation', 'Coding', 'Programming', 'Teamwork'], 'workshop')
test_event5 = test_event('Charity_Run', ['Sports', 'Fundraising', 'Community', 'Health'], 'sport')
test_event6 = test_event('Art_Exhibition', ['Art', 'Culture', 'Painting', 'Creativity'], 'conference')
test_event7 = test_event('Startup_Pitch', ['Entrepreneurship', 'Business', 'Networking', 'Investors'], 'panel discussion')
st.session_state['event_recommendations_list'] = [test_event1, test_event2, test_event3, test_event4, test_event5, test_event6, test_event7]
'''

user_keywords = st.session_state['user_keywords']
test_events = st.session_state['events_instances_list']

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
preferred_event_types = st.session_state['event_categories']

for event in test_events:
    # Calculate initial KMS
    event_kms, matches = calculate_kms(user_keywords, event.event_keywords)
    
    # Check for event type match
    event_type_match = check_event_type_match(event.event_type, preferred_event_types)
    
    # Apply bonus
    event.final_kms = apply_event_type_bonus(event_kms, event_type_match)

# Sort events by final KMS in descending order
sorted_events = sorted(test_events, key=lambda e: e.final_kms, reverse=True)[:5]

# Streamlit presentation
st.title("Top 5 Matched Events")

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

# Display events with ranking, thumbs-up/down buttons, and progress circles
for rank, event in enumerate(sorted_events, start=1):
    with st.container():
        # Create box layout
        st.markdown(
            f"""
            <div style="border: 2px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 15px; background-color: #ffffff; display: flex; align-items: center; justify-content: space-between;">
                <div style="flex: 1;">
                    <p style="font-weight: bold; color: #333; font-size: 14px;">Rank {rank}</p>
                    <h3 style="margin-bottom: 10px;">{event.title}</h3>
                </div>
                <div style="flex: 0;">
                    {render_progress_circle(event.final_kms)}
               
            """,
            unsafe_allow_html=True,
        )

        # Add thumbs-up and thumbs-down buttons inside the box
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👍 Like {event.title}", key=f"like_{event.title}"):
                st.success(f"Thanks for liking {event.title}!")
        with col2:
            if st.button(f"👎 Dislike {event.title}", key=f"dislike_{event.title}"):
                st.error(f"We're sorry {event.title} didn't match well!")



