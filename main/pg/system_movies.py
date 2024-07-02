#system_movies.py
import streamlit as st
import requests
import base64
import pickle
import gzip
import lzma
from api import api_key     

def load_data():
    with gzip.open("main/pickle/movies_list.pkl.gz", 'rb') as f:
        movies = pickle.load(f)
    with lzma.open("main/pickle/similarityy.pkl.xz", 'rb') as f:
        similarity = pickle.load(f)
    return movies, similarity

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def fetch_provider_info(movie_id, api_key):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}")
    providers_data = response.json()
    
    provider_names = []
    for country_code, country_data in providers_data.get('results', {}).items():
        if 'flatrate' in country_data:
            for provider in country_data['flatrate']:
                provider_name = provider.get('provider_name')
                if provider_name in ['Netflix', 'Amazon Prime Video', 'Prime Video', 'Disney Plus']:
                    provider_names.append(provider_name)
    provider_name = provider_names[0] if provider_names else None
    return provider_name

def recommend_by_title(movie, movies, similarity, api_key):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    recommend_movie = []
    recommend_poster = []
    recommend_provider = []
    
    for i in range(1, 6):
        movie_id = movies.iloc[distance[i][0]].id
        provider_name = fetch_provider_info(movie_id, api_key)
        
        recommend_movie.append(movies.iloc[distance[i][0]].title)
        poster_path = movies.iloc[distance[i][0]].poster_path
        recommend_poster.append("https://image.tmdb.org/t/p/w400" + poster_path)
        recommend_provider.append(provider_name)
    
    return recommend_movie, recommend_poster, recommend_provider


def tab():
    st.header("Movie Recommender System")
    
    category = ['--Select--', 'Title based', 'Genre based']
    cat_op = st.selectbox('Select Recommendation Type', category)
    
    if cat_op == 'Title based':
        movies, similarity = load_data()
        movies_list = movies['title'].values
        select_value = st.selectbox("Select movie", list(movies_list))
        
        if st.button("Show Recommendations"):
            movie_names, movie_posters, movie_providers = recommend_by_title(select_value, movies, similarity, api_key)
        
            provider_urls = {
                "Netflix": "https://www.netflix.com",
                "Amazon Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home",
                "Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home",
                "Disney Plus": "https://www.hotstar.com/in/movies"
            }
            
            netflix_icon = get_img_as_base64("main/image/icons8-netflix-64.png")
            amazon_icon = get_img_as_base64("main/image/icons8-amazon-prime-64.png")
            disney_icon = get_img_as_base64("main/image/icons8-disney-64.png")
            
            provider_icons = {
                "Netflix": netflix_icon,
                "Amazon Prime Video": amazon_icon,
                "Prime Video": amazon_icon,
                "Disney Plus": disney_icon
            }
            
            col1, col2, col3, col4, col5 = st.columns(5)
            for i in range(5):
                with locals()[f'col{i+1}']:
                    st.text(movie_names[i])
                    if movie_posters[i]:
                        st.markdown(f'<a href="{provider_urls.get(movie_providers[i], "#")}" target="_blank"><img src="{movie_posters[i]}" width="200"/></a>', unsafe_allow_html=True)
                    else:
                        st.text("No Poster Available")
                    if movie_providers[i]:
                        st.markdown(f'<a href="{provider_urls.get(movie_providers[i], "#")}" target="_blank"><img src="data:image/png;base64,{provider_icons.get(movie_providers[i], "")}" width="50"/></a>', unsafe_allow_html=True)
                        st.text(movie_providers[i])
                    elif any(movie_providers):
                        first_provider = next((p for p in movie_providers if p), "No streaming provider available")
                        st.markdown(f'<a href="{provider_urls.get(first_provider, "#")}" target="_blank"><img src="data:image/png;base64,{provider_icons.get(first_provider, "")}" width="50"/></a>', unsafe_allow_html=True)
                        st.text(first_provider)
                    else:
                        st.text("No streaming provider available")

                        

    elif cat_op == '--Select--':
        
        st.write("Please select a recommendation type.")
    
    else:
        # Define the CSS for the hover effect
        hover_css = """
        <style>
            .movie-poster {
            transition: transform 0.3s;
            border-radius: 10px;
        }
        .movie-poster:hover {
            transform: scale(1.3);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        </style>
        """
        st.markdown(hover_css, unsafe_allow_html=True)

        # URLs for providers
        provider_urls = {
            "Netflix": "https://www.netflix.com",
            "Amazon Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home",
            "Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=movie&contentId=home",
            "Disney Plus": "https://www.hotstar.com/in/movies"
        }

        # Function to get provider URL
        def get_provider_url(movie_title, providers):
            for provider in providers:
                if provider in provider_urls:
                    return provider_urls[provider]
            return "#"

        # Load the prepared DataFrame from the .pkl file
        with open('main/pickle/new_df.pkl', 'rb') as f:
            new_df = pickle.load(f)

        genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror',
                'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']

        # Container for genre selection and buttons
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                sel_gen = st.selectbox('Select Genre:', [""] + genres)
            with col2:
                st.text('Increase Or Decrease the numbers')
                if st.button(':heavy_minus_sign:'):
                    if 'num_movies' in st.session_state:
                        if st.session_state.num_movies >= 5:
                            st.session_state.num_movies -= 1
                    else:
                        st.session_state.num_movies = 5
            with col3:
                st.text('of Genres based recommendation')
                if st.button(':heavy_plus_sign:'):
                    if 'num_movies' in st.session_state:
                        st.session_state.num_movies += 1
                    else:
                        st.session_state.num_movies = 5

        # Initialize session state for the number of movies to display
        if 'num_movies' not in st.session_state:
            st.session_state.num_movies = 5

        # Base URL for poster images
        poster_base_url = "https://image.tmdb.org/t/p/w400"

        def display_movies(movies, platform_name, num_movies):
            st.header(f"{platform_name}  {sel_gen}")
            num_cols = 5
            num_rows = min(num_movies, len(movies))
            for i in range(num_rows):
                if i % num_cols == 0:
                    cols = st.columns(num_cols)
                movie_title, provider, poster_path = movies[i]
                provider_url = get_provider_url(movie_title, [provider])
                with cols[i % num_cols]:
                    st.markdown(f'<a href="{provider_url}" target="_blank"><img src="{poster_base_url + poster_path}" alt="{movie_title}" class="movie-poster" style="width:100%;"></a>', unsafe_allow_html=True)
                    st.write(movie_title)

        # Recommendation logic
        if sel_gen != "":
            # Filter movies by the selected genre
            recommended_movies = new_df[new_df[sel_gen] == 1]

            if recommended_movies.empty:
                st.write(f"No movies found for the selected genre: {sel_gen}")
            else:
                st.write(f"Movies in the {sel_gen} genre:")

                netflix_movies = []
                amazon_movies = []
                disney_movies = []

                for i, row in recommended_movies.head(st.session_state.num_movies * 3).iterrows():  # Fetching more to ensure we have enough per provider
                    movie_id = row['id']
                    movie_title = row['title']
                    poster_path = row['poster_path']

                    providers_data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}",)
                    providers_data = providers_data.json()

                    available = False

                    for country_code, country_data in providers_data.get('results', {}).items():
                        if 'flatrate' in country_data:
                            for provider in country_data['flatrate']:
                                provider_name = provider.get('provider_name')

                                if provider_name in ['Netflix', 'Amazon Prime Video', 'Prime Video', 'Disney Plus']:
                                    available = True

                                    if provider_name == 'Netflix':
                                        netflix_movies.append((movie_title, 'Netflix', poster_path))
                                    elif provider_name in ['Amazon Prime Video', 'Prime Video']:
                                        amazon_movies.append((movie_title, 'Amazon Prime Video', poster_path))
                                    elif provider_name == 'Disney Plus':
                                        disney_movies.append((movie_title, 'Disney Plus', poster_path))
                                    break
                            if available:
                                break

                if netflix_movies:
                    display_movies(netflix_movies, "Netflix", st.session_state.num_movies)
                if amazon_movies:
                    display_movies(amazon_movies, "Amazon", st.session_state.num_movies)
                if disney_movies:
                    display_movies(disney_movies, "Disney", st.session_state.num_movies)
        else:
            st.write("Please select a genre to get recommendations.")
    #  ***********************  RECOMMENDATION SYSTEM  SECTION  ENDED HERE  ******************************

    
