#search_movies.py
import streamlit as st
import base64
from streamlit.components.v1 import html
from api import api_key
from utils import popular_movies_data, trending_movies_data
from utils import search_movies, fetch_provider_and_poster, get_provider_name
from pg.favourites import add_to_favourite_movies
from pg.watchlist import add_to_watchlist_movies

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def app():
    st.title("Movie Search App")
    query = st.text_input("Enter movie name:")
    if st.button("Search"):
        if query:
            movies = search_movies(query, api_key, get_provider_name)
            if movies:
                st.write("Search Results:")
                num_movies = len(movies)
                num_columns = min(7, num_movies)

                filtered_movies = [movie for movie in movies if movie.get('title') and movie.get('poster_url') and movie.get('provider_name')]

                netflix_icon = get_img_as_base64("main/image/icons8-netflix-64.png")
                amazon_icon = get_img_as_base64("main/image/icons8-amazon-prime-64.png")
                disney_icon = get_img_as_base64("main/image/icons8-disney-64.png")

                for row in range(0, len(filtered_movies), num_columns):
                    columns = st.columns([2]*num_columns)
                    for col_index, movie in enumerate(filtered_movies[row:min(row+num_columns, len(filtered_movies))]):
                        movie_title = f"{movie['release_date']} | {movie['title']}"
                        overview = movie['overview']
                        poster_html = ""
                        provider_html = ""

                        if movie['provider_name'] == 'Netflix':
                            poster_html = f"""
                            <a href="https://www.netflix.com/in/" target="_blank">
                                <div class="poster-container">
                                    <img src="{movie['poster_url']}" width="200px" class="poster"/>
                                    <div class="poster-overlay">
                                        <div class="overview">{overview}</div>
                                    </div>
                                </div>
                            </a>"""
                            provider_html = f"""
                            <a href="https://www.netflix.com/in/" target="_blank">
                                <img src="data:image/png;base64,{netflix_icon}"/>
                            </a>"""
                        elif movie['provider_name'] in ['Amazon Prime Video', 'Prime Video']:
                            poster_html = f"""
                            <a href="https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home" target="_blank">
                                <div class="poster-container">
                                    <img src="{movie['poster_url']}" width="200px" class="poster"/>
                                    <div class="poster-overlay">
                                        <div class="overview">{overview}</div>
                                    </div>
                                </div>
                            </a>"""
                            provider_html = f"""
                            <a href="https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home" target="_blank">
                                <img src="data:image/png;base64,{amazon_icon}"/>
                            </a>"""
                        elif movie['provider_name'] == 'Disney Plus':
                            poster_html = f"""
                            <a href="https://www.hotstar.com/in/movies" target="_blank">
                                <div class="poster-container">
                                    <img src="{movie['poster_url']}" width="200px" class="poster"/>
                                    <div class="poster-overlay">
                                        <div class="overview">{overview}</div>
                                    </div>
                                </div>
                            </a>"""
                            provider_html = f"""
                            <a href="https://www.hotstar.com/in/movies" target="_blank">
                                <img src="data:image/png;base64,{disney_icon}"/>
                            </a>"""

                        with columns[col_index]:
                            st.markdown(poster_html, unsafe_allow_html=True)
                            st.markdown(f"<div>{provider_html}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div>{movie_title}</div>", unsafe_allow_html=True)
    
                custom_css = """
                <style>
                .poster-container {
                    position: relative;
                    width: 200px;
                    overflow: hidden;
                    margin: 10px 0;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }

                .poster {
                    display: block;
                    width: 100%;
                    height: auto;
                    transition: transform 0.2s ease-in-out;
                    border-radius: 10px;
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
                    transition: opacity 0.2s ease-in-out;
                    border-radius: 10px;
                }

                .poster-container:hover .poster-overlay {
                    opacity: 1;
                }

                .overview {
                    padding: 10px;
                    font-size: 14px;
                    text-align: center;
                    max-height: 100%;
                    overflow: hidden;
                }
                </style>
                """
                st.markdown(custom_css, unsafe_allow_html=True)

    #  ***********************   SEARCH BAR ENDS HERE    ******************************

    #  ***********************  LIVE POPULAR & TRENDING  MOVIES STARTS HERE    ******************************
    # <<<<<<<<<<<<<<<<<<<<<<<<< LIVE POPULAR MOVIES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  
    # API THROUGH POPULAR MOVIES
    # Fetch popular movies data
    # Custom CSS for hover effect
    st.markdown("""
        <style>
        .movie-poster-container {
            position: relative;
            display: inline-block;
            margin: 10px;
        }
        .movie-poster {
            width: 200px;
            border-radius: 10px;
            transition: transform 0.2s;
        }
        .movie-title {
            display: none;
            position: absolute;
            bottom: 10px;
            left: 10px;
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 5px;
            border-radius: 5px;
        }
        .movie-poster-container:hover .movie-poster {
            transform: scale(1.35);
        }
        .movie-poster-container:hover .movie-title {
            display: block;
        }
        </style>
        """, unsafe_allow_html=True)

    # URLs for providers
    provider_urls = {
        "Netflix": "https://www.netflix.com",
        "Amazon Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home",
        "Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home",
        "Disney Plus": "https://www.hotstar.com/in/movies"
    }

    def display_movies(movies, header):
        st.markdown(f"<h4>{header}</h4>", unsafe_allow_html=True)
        num_cols = 5
        for i, (id, title, poster_url, provider_name) in enumerate(movies):
            if i % num_cols == 0:
                cols = st.columns(num_cols)
            with cols[i % num_cols]:
                if provider_name in provider_urls:
                    provider_url = provider_urls[provider_name]
                else:
                    provider_url = "#"
                st.markdown(f"""
                    <div class="movie-poster-container">
                        <a href="{provider_url}" target="_blank">
                            <img src="{poster_url}" class="movie-poster"/>
                            <div class="movie-title">{title}</div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                p1, p2 = st.columns(2)
                with p1:
                    if st.button("Watchlist", key=f"watchlist_{header}_{i}_{id}_{p1}"):
                        add_to_watchlist_movies({'id': id, 'title': title, 'poster_url': poster_url, 'provider_name': provider_name})
                with p2:
                    if st.button("Favourites", key=f"favourites_{header}_{i}_{id}_{p2}"):
                        add_to_favourite_movies({'id': id, 'title': title, 'poster_url': poster_url, 'provider_name': provider_name})

    # Initialize lists to store movie titles and posters for each platform
    netflix_movies = []
    amazon_movies = []
    disney_movies = []

    # Iterate over popular movies
    for movie in popular_movies_data['results']:
        movie_id = movie['id']
        movie_title = movie['title']

        # Get provider name and poster
        provider_name, poster_url = fetch_provider_and_poster(movie_id)

        # If provider name is found, add movie to respective platform list
        if provider_name == 'Netflix':
            netflix_movies.append((movie_id, movie_title, poster_url, provider_name))
        elif provider_name == 'Amazon Prime Video':
            amazon_movies.append((movie_id, movie_title, poster_url, provider_name))
        elif provider_name == 'Disney Plus':
            disney_movies.append((movie_id, movie_title, poster_url, provider_name))

    # Display movies for each platform
    st.header("Live Popular")
    display_movies(netflix_movies, "Netflix")
    display_movies(amazon_movies, "Amazon")
    display_movies(disney_movies, "Disney")

    # <<<<<<<<<<<<<<<<<<< LIVE TRENDING MOVIES >>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Initialize lists to store movie titles and posters for each platform
    netflix_movies = []
    amazon_movies = []
    disney_movies = []

    # Iterate over trending movies
    for movie in trending_movies_data['results']:
        movie_id = movie['id']
        movie_title = movie['title']

        # Get provider name and poster
        provider_name, poster_url = fetch_provider_and_poster(movie_id)

        # If provider name is found, add movie to respective platform list
        if provider_name == 'Netflix':
            netflix_movies.append((movie_id, movie_title, poster_url, provider_name))
        elif provider_name == 'Amazon Prime Video':
            amazon_movies.append((movie_id, movie_title, poster_url, provider_name))
        elif provider_name == 'Disney Plus':
            disney_movies.append((movie_id, movie_title, poster_url, provider_name))

    # Display movies for each platform
    st.header("Live Trending")
    display_movies(netflix_movies, "Netflix")
    display_movies(amazon_movies, "Amazon")
    display_movies(disney_movies, "Disney")
