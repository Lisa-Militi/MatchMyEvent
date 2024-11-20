import streamlit as st
import pandas as pd
import os

def load_keywords(keywords_str):
    """Convert comma-separated string to lowercase list of keywords"""
    return [kw.strip().lower() for kw in keywords_str.split(',') if kw.strip()]

def calculate_kms(user_list, event_list):
    """Calculate Keyword Matching Score"""
    matches = list(filter(lambda keyword: keyword in event_list, user_list))
    match_count = len(matches)
    total_keywords = len(user_list)
    match_rate = (match_count / total_keywords * 100) if total_keywords > 0 else 0
    return match_rate, matches

def load_event_profiles():
    """Load event profile CSV files"""
    event_files = [
        os.path.join('event_profiles', filename) 
        for filename in os.listdir('event_profiles') 
        if filename.endswith('.csv')
    ]
    
    if not event_files:
        st.warning("No event profiles found.")
        return None
    
    try:
        # Read all event profile files
        event_dfs = [pd.read_csv(file) for file in event_files]
        return pd.concat(event_dfs, ignore_index=True)
    except Exception as e:
        st.error(f"Error loading event profiles: {e}")
        return None

def load_user_profiles():
    """Load all user profile CSV files"""
    if not os.path.exists('user_profiles'):
        st.warning("No user profiles found.")
        return None
    
    profile_files = [
        os.path.join('user_profiles', filename) 
        for filename in os.listdir('user_profiles') 
        if filename.startswith('user_profiles_') and filename.endswith('.csv')
    ]
    
    if not profile_files:
        st.warning("No user profiles found.")
        return None
    
    try:
        profiles_df = pd.concat([pd.read_csv(file) for file in profile_files], ignore_index=True)
        return profiles_df
    except Exception as e:
        st.error(f"Error loading profiles: {e}")
        return None

def display_profiles():
    """Display User and Event Profiles with Matching Score"""
    st.title("Profile Matcher")
    
    # Load user and event profiles
    user_profiles = load_user_profiles()
    event_profiles = load_event_profiles()
    
    if user_profiles is not None and event_profiles is not None:
        # Select user profile
        selected_name = st.selectbox(
            "Select a User Profile", 
            [""] + list(user_profiles['name'])
        )
        
        if selected_name:
            # Get selected user profile
            selected_profile = user_profiles[user_profiles['name'] == selected_name].iloc[0]
            
            # Prepare user keywords
            user_keywords = load_keywords(selected_profile['selected_interests'])
            
            # Event Profile Selection
            st.subheader("Event Profile Matching")
            
            # Multiselect for event types
            unique_events = event_profiles[event_profiles.columns[0]].unique()
            selected_events = st.multiselect(
                "Select Event Types to Match", 
                list(unique_events)
            )
            
            # Matching for selected events
            if selected_events:
                matching_results = []
                
                for event in selected_events:
                    # Filter events of selected type
                    event_subset = event_profiles[event_profiles[event_profiles.columns[0]] == event]
                    
                    # Get event keywords (assuming second column contains keywords)
                    event_keywords = load_keywords(event_subset.iloc[0, 1] if len(event_subset.columns) > 1 else event)
                    
                    # Calculate matching score
                    match_percentage, matched_keywords = calculate_kms(user_keywords, event_keywords)
                    
                    matching_results.append({
                        'Event Type': event,
                        'Matching Score': match_percentage,
                        'Matched Keywords': matched_keywords
                    })
                
                # Display matching results
                results_df = pd.DataFrame(matching_results)
                st.dataframe(results_df)
                
                # Visualize top match
                if not results_df.empty:
                    top_match = results_df.loc[results_df['Matching Score'].idxmax()]
                    
                    st.subheader("Best Match Details")
                    st.write(f"**Best Matching Event Type:** {top_match['Event Type']}")
                    st.write(f"**Matching Score:** {top_match['Matching Score']:.2f}%")
                    
                    # Progress bar for top match
                    st.progress(int(top_match['Matching Score'])/100)
                    
                    st.write("**Matched Keywords:**")
                    st.write(", ".join(top_match['Matched Keywords']))


display_profiles()

