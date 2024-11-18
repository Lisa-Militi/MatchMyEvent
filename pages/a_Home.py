import streamlit as st

st.set_page_config(
    page_title="Welcome to MatchMyEvent!",
    page_icon="✨",
    layout="centered"
)

st.title("Welcome to MatchMyEvent!")

image_path = "/Users/alice/Desktop/ClubsHSG.png"  
st.image(image_path, caption="HSG Clubs", use_column_width=True)

st.markdown(
    """
    *The Webpage to guide you through HSG campus events*  
    *Do you feel overwhelmed by the too big amount of clubs and events proposed at HSG?* Don't worry, this page's for you.*
    *We've created an algorithm that will perfectly match your preferences.*""",
    unsafe_allow_html=True
)
