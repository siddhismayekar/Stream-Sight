#api.py
# import os
# from dotenv import load_dotenv
# load_dotenv()

# api_key = os.getenv("api_key")
# access_token=os.getenv("access_token")
# WebAPIKey =os.getenv("WebAPIKey")
# email=os.getenv("email")

import streamlit as st
# Access secrets directly from Streamlit's secrets management
api_key = st.secrets["api_key"]
access_token = st.secrets["access_token"]
WebAPIKey = st.secrets["WebAPIKey"]
email = st.secrets["email"]
