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

def app():
     # Load Lottie animations
    lottie_hero = load_lottie_file("main/animation/man_watching_movie.json")
    logo_net = load_lottie_file("main/animation/netflix_logo.json")
    logo_pri = load_lottie_file("main/animation/prime_video_logo.json")
    logo_dis = load_lottie_file("main/animation/disney_logo.json")

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
        bg_image_base64 = get_base64_image("main/image/hgbg.jpg")

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

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("main/style/style.css")


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


