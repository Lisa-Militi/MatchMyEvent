import streamlit as st
from exchangelib import Credentials, Account, CalendarItem, DELEGATE, EWSDateTime, EWSTimeZone
from datetime import datetime, timedelta


def handle_calendar_invite(event):
    """Handle calendar invitation for an event"""
    st.write("Function called!")  # Debug print
    
    if not st.session_state['user_email']:
        st.warning("Please provide your email in your profile first!")
        return False
        
    st.write("Got email:", st.session_state['user_email'])  # Debug print
    
    try:
        if st.session_state.calendar_manager is None:
            st.write("No calendar manager, showing password input")  # Debug print
            password = st.text_input("Enter your Outlook password", type="password",
                                  help="If you use 2FA, use an app password instead")
            
            if st.button("Connect to Outlook", key="outlook_connect"):  # Added unique key
                st.write("Connect button clicked!")  # Debug print
                # ... rest of your code
                try:
                    # Debug messages
                    st.write(f"Using email: {st.session_state.user_email}")
                    
                    # Try creating credentials
                    st.write("Creating credentials...")
                    credentials = Credentials(st.session_state.user_email, password)
                    
                    # Try connecting to account
                    st.write("Connecting to account...")
                    account = Account(
                        st.session_state.user_email,
                        credentials=credentials,
                        autodiscover=True,
                        access_type=DELEGATE
                    )
                    
                    # Try accessing calendar
                    st.write("Accessing calendar...")
                    calendar = account.calendar
                    if calendar is None:
                        st.error("Could not access calendar")
                        return False
                        
                    st.session_state.calendar_manager = account
                    st.success("Connected to Outlook!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to connect to Outlook: {str(e)}")
                    # Print more detailed error information
                    import traceback
                    st.write("Detailed error:")
                    st.code(traceback.format_exc())
                    return False
                    
        else:
            try:
                tz = EWSTimeZone('Europe/Zurich')
                
                # Debug the dates
                st.write(f"Start date string: {event.startDate}")
                st.write(f"End date string: {event.endDate}")
                
                # Parse dates with explicit format
                start_date = datetime.strptime(event.startDate, "%Y-%m-%dT%H:%M:%S.%fZ")
                end_date = datetime.strptime(event.endDate, "%Y-%m-%dT%H:%M:%S.%fZ")
                
                st.write("Creating calendar event...")
                calendar_event = CalendarItem(
                    account=st.session_state.calendar_manager,
                    folder=st.session_state.calendar_manager.calendar,
                    subject=event.title,
                    start=EWSDateTime.from_datetime(start_date.replace(tzinfo=tz)),
                    end=EWSDateTime.from_datetime(end_date.replace(tzinfo=tz)),
                    body=f"""
                    Event: {event.title}
                    Organized by: {event.clubName}
                    Location: {event.location_text}
                    
                    Description:
                    {event.description}
                    """,
                    location=event.location_text,
                    required_attendees=[st.session_state.user_email]
                )
                
                st.write("Saving and sending invitation...")
                calendar_event.save(send_meeting_invitations=True)
                return True
                
            except Exception as e:
                st.error(f"Failed to create calendar event: {str(e)}")
                import traceback
                st.write("Detailed error:")
                st.code(traceback.format_exc())
                return False
                
    except Exception as e:
        st.error(f"Calendar error: {str(e)}")
        import traceback
        st.write("Detailed error:")
        st.code(traceback.format_exc())
        return False