#home.py
import streamlit as st
from streamlit_lottie import st_lottie
import json
import api
import base64

# Function to load Lottie animations from a file
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
# Function to convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
from pathlib import Path
def app():
    # Load Lottie animations
    lottie_hero = load_lottie_file("animation/man_watching_movie.json")
    logo_net = load_lottie_file("animation/netflix_logo.json")
    logo_pri = load_lottie_file("animation/prime_video_logo.json")
    logo_dis = load_lottie_file("animation/disney_logo.json")

    # Display logos
    l1, l2, l3 = st.columns(3)
    with l1:
        st_lottie(logo_net, height=150, speed=2)
    with l2:
        st_lottie(logo_pri, height=150, speed=2)
    with l3:
        st_lottie(logo_dis, height=150, speed=2)
    
    # Hero section with background image
    c1, c2 = st.columns([3, 1])
    with c2:
        st_lottie(lottie_hero, height=400)
    with c1:
        # Convert image to base64
        bg_image_base64 = get_base64_image("image/hgbg.jpg")

        # Hero Section
        st.markdown(f"""
            <style>
            .hero {{
                background-image: url('data:image/jpg;base64,{bg_image_base64}');
                background-size: cover;
                background-position: center;
                padding: 80px 0;
                text-align: center;
                color: white;
                position: relative;
                border-radius: 50px;
            }}
            .hero::after {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                border-radius: 50px;
                z-index: 1;
            }}
            .hero-content {{
                position: relative;
                border-radius: 50px;
                z-index: 2;
            }}
            .hero h1 {{
                font-size: 3em;
                margin-bottom: 0.6em;
            }}
            .hero p {{
                font-size: 1.5em;
                margin-bottom: 3em;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="hero">
                <div class="hero-content">
                    <h1>Welcome to StreamSight</h1>
                    <p>Discover Movies and TV Shows across different streaming platforms. Add your movies and tv shows to watchlist also can aad to favourites  </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
        <div style="text-align: center; padding: 50px 0;">
            <h2>About StreamSight</h2>
            <p>Explore across Netflix, Amazon Prime, and Disney+ with StreamSight, your ultimate destination for recommendations and the latest releases.</p>
        </div>
    """, unsafe_allow_html=True)

    # Contact feedback session
    st.header(":mailbox: Get In Touch With Us!")

    contact_form = f"""
    <form action="https://formsubmit.co/{api.email}" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Define the CSS content directly as a string
    css_content = """
    /* Style inputs with type="text", type="email" and textareas */
    input[type=text], input[type=email], textarea {
      width: 100%; /* Full width */
      padding: 12px; /* Some padding */
      border: 1px solid #ccc; /* Gray border */
      border-radius: 4px; /* Rounded borders */
      box-sizing: border-box; /* Make sure that padding and width stays in place */
      margin-top: 6px; /* Add a top margin */
      margin-bottom: 16px; /* Bottom margin */
      resize: vertical; /* Allow the user to vertically resize the textarea (not horizontally) */
    }
    
    /* Style the submit button with a specific background color etc */
    button[type=submit] {
      background-color: #295190;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    
    /* When moving the mouse over the submit button, add a darker green color */
    button[type=submit]:hover {
      background-color: #45a049;
    }
    """
    
    # Apply the CSS using Streamlit's markdown function
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


    # Footer Section
    st.markdown("""
        <style>
        .footer {
            text-align: center;
            padding: 20px 0;
            background-color: "#639CD9";
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="footer">
            <p>&copy; 2024 StreamSight. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)



