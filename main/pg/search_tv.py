#search_tv.py
import streamlit as st
import base64
from api import access_token
from utils import popular_tv_shows_data, trending_tv_shows_data
from utils import search_tv_shows, fetch_tv_provider_and_poster
from pg.favourites import add_to_favourite_tv_shows
from pg.watchlist import add_to_watchlist_tv_shows

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def app():
    st.title("TV Show Search App")
    query = st.text_input("Enter TV show name:")
    if st.button("Search"):
        if query:
            tv_shows = search_tv_shows(query, access_token)
            if tv_shows:
                st.write("Search Results:")
                num_tv_shows = len(tv_shows)
                num_columns = min(7, num_tv_shows)

                filtered_tv_shows = [tv_show for tv_show in tv_shows if tv_show.get('name') and tv_show.get('poster_url') and tv_show.get('provider_name')]

                # Load the base64 encoded images
                netflix_icon = get_img_as_base64("main/image/icons8-netflix-64.png")
                amazon_icon = get_img_as_base64("main/image/icons8-amazon-prime-64.png")
                disney_icon = get_img_as_base64("main/image/icons8-disney-64.png")

                for row in range(0, len(filtered_tv_shows), num_columns):
                    columns = st.columns([2]*num_columns)
                    for col_index, tv_show in enumerate(filtered_tv_shows[row:min(row+num_columns, len(filtered_tv_shows))]):
                        tv_show_title = f"{tv_show['release_date']} | {tv_show['name']}"
                        overview = tv_show['overview']
                        poster_html = ""
                        provider_html = ""

                        if tv_show['provider_name'] == 'Netflix':
                            poster_html = f"""
                            <a href="https://www.netflix.com/in/" target="_blank">
                                <div class="poster-container">
                                    <img src="{tv_show['poster_url']}" width="200px" class="poster"/>
                                    <div class="poster-overlay">
                                        <div class="overview">{overview}</div>
                                    </div>
                                </div>
                            </a>"""
                            provider_html = f"""
                            <a href="https://www.netflix.com/in/" target="_blank">
                                <img src="data:image/png;base64,{netflix_icon}"/>
                            </a>"""
                        elif tv_show['provider_name'] in ['Amazon Prime Video', 'Prime Video', 'Amazon Video']:
                            poster_html = f"""
                            <a href="https://www.primevideo.com/storefront/ref=atv_hm_hom_c_9zZ8D2_hm_tv?contentType=tv&contentId=home" target="_blank">
                                <div class="poster-container">
                                    <img src="{tv_show['poster_url']}" width="200px" class="poster"/>
                                    <div class="poster-overlay">
                                        <div class="overview">{overview}</div>
                                    </div>
                                </div>
                            </a>"""
                            provider_html = f"""
                            <a href="https://www.primevideo.com/storefront/ref=atv_hm_hom_c_9zZ8D2_hm_tv?contentType=tv&contentId=home" target="_blank">
                                <img src="data:image/png;base64,{amazon_icon}"/>
                            </a>"""
                        elif tv_show['provider_name'] == 'Disney Plus':
                            poster_html = f"""
                            <a href="https://www.hotstar.com/in/shows" target="_blank">
                                <div class="poster-container">
                                    <img src="{tv_show['poster_url']}" width="200px" class="poster"/>
                                    <div class="poster-overlay">
                                        <div class="overview">{overview}</div>
                                    </div>
                                </div>
                            </a>"""
                            provider_html = f"""
                            <a href="https://www.hotstar.com/in/tv_shows" target="_blank">
                                <img src="data:image/png;base64,{disney_icon}"/>
                            </a>"""

                        with columns[col_index]:
                            st.markdown(poster_html, unsafe_allow_html=True)
                            st.markdown(f"<div>{provider_html}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div>{tv_show_title}</div>", unsafe_allow_html=True)
                
                # Add custom CSS for hover effects
                custom_css = """
                <style>
                .poster-container {
                    position: relative;
                    width: 200px;
                    overflow: hidden;
                    margin: 10px 0;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.9);
                }
                .poster {
                    display: block;
                    width: 200px;
                    border-radius: 10px;
                    transition: transform 0.3s ease;
                }
                .poster-container:hover .poster {
                    transform: scale(1.05);
                }
                .poster-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.7);
                    color: white;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                    text-align: center;
                    border-radius: 10px;
                }
                .poster-container:hover .poster-overlay {
                    opacity: 1;
                }
                .tv_show-title {
                    font-size: 14px;
                }
                .overview {
                    padding: 10px;
                    font-size: 12px;
                    line-height: 1;
                }
                </style>
                """
                st.markdown(custom_css, unsafe_allow_html=True)

    #  ***********************  LIVE POPULAR & TRENDING TV SHOWS STARTS HERE ***********************
    # <<<<<<<<<<<<<<<<<<<<<<<<< LIVE POPULAR TV SHOWS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    st.markdown("""
        <style>
        .tv_show-poster-container {
            position: relative;
            display: inline-block;
            margin: 10px;
        }
        .tv_show-poster {
            width: 200px;
            border-radius: 10px;
            transition: transform 0.2s;
        }
        .tv_show-title {
            display: none;
            position: absolute;
            bottom: 10px;
            left: 10px;
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 5px;
            border-radius: 5px;
        }
        .tv_show-poster-container:hover .tv_show-poster {
            transform: scale(1.35);
        }
        .tv_show-poster-container:hover .tv_show-title {
            display: block;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def display_tv_shows(tv_shows, header):
        st.markdown(f"<h4>{header}</h4>", unsafe_allow_html=True)
        num_cols = 5
        for i, (title, poster_url) in enumerate(tv_shows):
            if i % num_cols == 0:
                cols = st.columns(num_cols)
            with cols[i % num_cols]:
                st.markdown(f"""
                    <div class="tv_show-poster-container">
                        <img src="{poster_url}" class="tv_show-poster"/>
                        <div class="tv_show-title">{title}</div>
                    </div>
                    """, unsafe_allow_html=True)
                p1, p2 = st.columns(2)
                with p1:
                    if st.button("Watchlist", key=f"watchlist_{header}_{i}_{tv_show_id}"):
                        # st.success(f"Added {title} to your watchlist.")
                        add_to_watchlist_tv_shows({'title': title, 'poster_url': poster_url, 'provider_name': header})
                with p2:
                    if st.button("Favourites", key=f"favourites_{header}_{i}_{tv_show_id}"):
                        add_to_favourite_tv_shows({'title': title, 'poster_url': poster_url, 'provider_name': header})

    # Initialize lists to store TV show titles and posters for each platform
    netflix_tv_shows = []
    amazon_tv_shows = []
    disney_tv_shows = []

    # Iterate over popular TV shows
    for tv_show in popular_tv_shows_data['results']:
        tv_show_id = tv_show['id']
        tv_show_title = tv_show['name']

        # Get provider name and poster
        provider_name, poster_url = fetch_tv_provider_and_poster(tv_show_id)

        # If provider name is found, add TV show to respective platform list
        if provider_name == 'Netflix':
            netflix_tv_shows.append((tv_show_title, poster_url))
        elif provider_name == 'Amazon Prime Video':
            amazon_tv_shows.append((tv_show_title, poster_url))
        elif provider_name == 'Disney Plus':
            disney_tv_shows.append((tv_show_title, poster_url))

    # Display TV shows for each platform
    st.header("Live Popular")
    display_tv_shows(netflix_tv_shows, "Netflix")
    display_tv_shows(amazon_tv_shows, "Amazon Prime Video")
    display_tv_shows(disney_tv_shows, "Disney Plus")

    # <<<<<<<<<<<<<<<<<<< LIVE TRENDING TV SHOWS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Initialize lists to store TV show titles and posters for each platform
    netflix_tv_shows = []
    amazon_tv_shows = []
    disney_tv_shows = []

    # Iterate over trending TV shows
    for tv_show in trending_tv_shows_data['results']:
        tv_show_id = tv_show['id']
        tv_show_title = tv_show['name']

        # Get provider name and poster
        provider_name, poster_url = fetch_tv_provider_and_poster(tv_show_id)

        # If provider name is found, add TV show to respective platform list
        if provider_name == 'Netflix':
            netflix_tv_shows.append((tv_show_title, poster_url))
        elif provider_name == 'Amazon Prime Video':
            amazon_tv_shows.append((tv_show_title, poster_url))
        elif provider_name == 'Disney Plus':
            disney_tv_shows.append((tv_show_title, poster_url))

    # Display TV shows for each platform
    st.header("Live Trending")
    display_tv_shows(netflix_tv_shows, "Netflix")
    display_tv_shows(amazon_tv_shows, "Amazon Prime Video")
    display_tv_shows(disney_tv_shows, "Disney Plus")

