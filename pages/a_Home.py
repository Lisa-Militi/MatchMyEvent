import streamlit as st
import session_state_handler as ss_handler


# Ajouter le style CSS pour centrer le contenu
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

# Contenu de la page avec la classe CSS centrée
st.markdown("<h1 class=""centered"">Welcome to MatchMyEvent:sparkles:</h1>", unsafe_allow_html=True)
st.markdown('<p class="centered">The webpage to guide you through HSG campus events</p>', unsafe_allow_html=True)
st.markdown('<h4 class="centered">Do you feel overwhelmed by the too big amount of clubs and events proposed at HSG?</h4>', unsafe_allow_html=True)
st.markdown('<h4 class="centered">Don\'t worry, this page\'s for you</h4>', unsafe_allow_html=True)
st.markdown('<p class="centered">We\'ve created an algorithm that will perfectly match your preferences</p>', unsafe_allow_html=True)
