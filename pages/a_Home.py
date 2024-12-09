import streamlit as st
import session_state_handler as ss_handler
import streamlit as st
from PIL import Image
import requests

# URL brute de l'image sur GitHub
image_url = r"MatchMyEvent Logo.tiff"

try:
    # Charger l'image depuis l'URL
    response = requests.get(image_url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    image = Image.open(BytesIO(response.content))

    # Réduire la taille de l'image (diviser les dimensions par 3)
    width, height = image.size
    resized_image = image.resize((width // 3, height // 3))

    # Afficher l'image redimensionnée dans Streamlit
    st.image(resized_image, caption="MatchMyEvent Logo (Reduced Size)", use_column_width=False)

except requests.exceptions.RequestException as e:
    st.error(f"Error loading image: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")
    
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
st.markdown("<h1 class=""centered"">Welcome to MatchMyEvent :) </h1>", unsafe_allow_html=True)
st.markdown('<p class="centered">The webpage to guide you through HSG campus events</p>', unsafe_allow_html=True)
st.markdown('<h4 class="centered">Do you feel overwhelmed by the too big amount of clubs and events proposed at HSG?</h4>', unsafe_allow_html=True)
st.markdown('<h4 class="centered">Don\'t worry, this page\'s for you</h4>', unsafe_allow_html=True)
st.markdown('<p class="centered">We\'ve created an algorithm that will perfectly match your preferences</p>', unsafe_allow_html=True)
