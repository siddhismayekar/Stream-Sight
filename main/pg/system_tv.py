#system_tv.py

import pickle
import requests
import base64
import streamlit as st
from api import api_key
import gzip


# Load data function
def load_data():
    with gzip.open("main/pickle/tv_ls.pkl.gz", 'rb') as f:
        tvs = pickle.load(f)
    with gzip.open("main/pickle/similarity_tv.pkl.gz.xz", 'rb') as f:
        similarity = pickle.load(f)
    return tvs, similarity

# Function to get base64 encoded image
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to fetch provider information
def fetch_provider_info(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}/watch/providers?api_key={api_key}"
    try:
        response = requests.get(url, )
        response.raise_for_status()  # Raises HTTPError for bad responses
        providers_data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return None
    except ValueError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    
    provider_names = []
    for country_code, country_data in providers_data.get('results', {}).items():
        if 'flatrate' in country_data:
            for provider in country_data['flatrate']:
                provider_name = provider.get('provider_name')
                if provider_name in ['Netflix', 'Amazon Prime Video', 'Prime Video', 'Disney Plus']:
                    provider_names.append(provider_name)
    
    return provider_names[0] if provider_names else None

# Recommendation function
def recommend_by_name(tv, tvs, similarity):
    index = tvs[tvs['name'] == tv].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommend_tv = []
    recommend_poster = []
    recommend_provider = []

    for i in distances[1:6]:
        recommended_index = i[0]
        recommend_tv.append(tvs.iloc[recommended_index]['name'])
        poster_path = tvs.iloc[recommended_index].poster_path
        recommend_poster.append("https://image.tmdb.org/t/p/w400" + poster_path)
        provider_name = fetch_provider_info(tvs.iloc[recommended_index].id)
        recommend_provider.append(provider_name)
    
    return recommend_tv, recommend_poster, recommend_provider
def tab():
    # Streamlit UI
    st.header("TV SHOWS Recommender System")

    category = ['--Select--', 'Name based', 'Genre based']
    cat_op = st.selectbox('Select Recommendation Type', category)

    if cat_op == 'Name based':
        tvs, similarity = load_data()
        tvs_list = tvs['name'].values
        select_value = st.selectbox("Select TV Show", list(tvs_list))
        
        if st.button("Show Recommendations"):
            tv_names, tv_posters, tv_providers = recommend_by_name(select_value, tvs, similarity)
        
            provider_urls = {
                "Netflix": "https://www.netflix.com",
                "Amazon Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=tv&contentId=home",
                "Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=tv&contentId=home",
                "Disney Plus": "https://www.hotstar.com/in"
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
                    st.text(tv_names[i])
                    if tv_posters[i]:
                        st.markdown(f'<a href="{provider_urls.get(tv_providers[i], "#")}" target="_blank"><img src="{tv_posters[i]}" width="200"/></a>', unsafe_allow_html=True)
                    else:
                        st.text("No Poster Available")
                    if tv_providers[i]:
                        st.markdown(f'<a href="{provider_urls.get(tv_providers[i], "#")}" target="_blank"><img src="data:image/png;base64,{provider_icons.get(tv_providers[i], "")}" width="50"/></a>', unsafe_allow_html=True)
                        st.text(tv_providers[i])
                    elif any(tv_providers):
                        first_provider = next((p for p in tv_providers if p), "No streaming provider available")
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
            .tv-poster {
            transition: transform 0.3s;
            border-radius: 10px;
        }
        .tv-poster:hover {
            transform: scale(1.3);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        </style>
        """
        st.markdown(hover_css, unsafe_allow_html=True)

        # URLs for providers
        provider_urls = {
            "Netflix": "https://www.netflix.com",
            "Amazon Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=tv&contentId=home",
            "Prime Video": "https://www.primevideo.com/storefront/ref=atv_hom_pri_c_9zZ8D2_hm_mv?contentType=tv&contentId=home",
            "Disney Plus": "https://www.hotstar.com/in/tvs"
        }

        # Function to get provider URL
        def get_provider_url(tv_name, providers):
            for provider in providers:
                if provider in provider_urls:
                    return provider_urls[provider]
            return "#"

        # Load the prepared DataFrame from the .pkl file
        with open('main/pickle/new_tv.pkl', 'rb') as f:
            new_df = pickle.load(f)

        genres = ['Action & Adventure','Animation','Comedy','Crime','Documentary','Drama','Family',
        'History','Kids','Musical','Mystery','News','Reality','Romance','Sci-Fi & Fantasy','Soap',
        'Talk','War & Politics','Western']

        # Container for genre selection and buttons
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                sel_gen = st.selectbox('Select Genre:', [""] + genres)
            with col2:
                st.text('Increase Or Decrease the numbers')
                if st.button(':heavy_minus_sign:'):
                    if 'num_tv' in st.session_state:
                        if st.session_state.num_tv >= 5:
                            st.session_state.num_tv -= 1
                    else:
                        st.session_state.num_tv = 5
            with col3:
                st.text('of Genres based recommendation')
                if st.button(':heavy_plus_sign:'):
                    if 'num_tv' in st.session_state:
                        st.session_state.num_tv += 1
                    else:
                        st.session_state.num_tv = 5

        # Initialize session state for the number of tvs to display
        if 'num_tv' not in st.session_state:
            st.session_state.num_tv = 5

        # Base URL for poster images
        poster_base_url = "https://image.tmdb.org/t/p/w400"

        def display_tvs(tvs, platform_name, num_tv):
            st.header(f"{platform_name}  {sel_gen}")
            num_cols = 5
            num_rows = min(num_tv, len(tvs))
            for i in range(num_rows):
                if i % num_cols == 0:
                    cols = st.columns(num_cols)
                tv_name, provider, poster_path = tvs[i]
                provider_url = get_provider_url(tv_name, [provider])
                with cols[i % num_cols]:
                    st.markdown(f'<a href="{provider_url}" target="_blank"><img src="{poster_base_url + poster_path}" alt="{tv_name}" class="tv-poster" style="width:100%;"></a>', unsafe_allow_html=True)
                    st.write(tv_name)

        # Recommendation logic
        if sel_gen != "":
            # Filter tvs by the selected genre
            recommended_tvs = new_df[new_df[sel_gen] == 1]

            if recommended_tvs.empty:
                st.write(f"No Tv Shows found for the selected genre: {sel_gen}")
            else:
                st.write(f" TV Shows in the {sel_gen} genre:")

                netflix_tvs = []
                amazon_tvs = []
                disney_tvs = []

                for i, row in recommended_tvs.head(st.session_state.num_tv * 3).iterrows():  # Fetching more to ensure we have enough per provider
                    tv_show_id = row['id']
                    tv_name = row['name']
                    poster_path = row['poster_path']

                    providers_data = requests.get(f"https://api.themoviedb.org/3/tv/{tv_show_id}/watch/providers?api_key={api_key}", )
                    providers_data = providers_data.json()
            
                    available = False

                    for country_code, country_data in providers_data.get('results', {}).items():
                        if 'flatrate' in country_data:
                            for provider in country_data['flatrate']:
                                provider_name = provider.get('provider_name')
                                if provider_name in ['Netflix', 'Amazon Prime Video', 'Prime Video','Amazon Video','Disney Plus',]:
                                    available = True

                                    if provider_name == 'Netflix':
                                        netflix_tvs.append((tv_name, 'Netflix', poster_path))
                                    elif provider_name in ['Amazon Prime Video', 'Prime Video']:
                                        amazon_tvs.append((tv_name, 'Amazon Prime Video', poster_path))
                                    elif provider_name == 'Disney Plus':
                                        disney_tvs.append((tv_name, 'Disney Plus', poster_path))
                                    break
                            if available:
                                break

                if netflix_tvs:
                    display_tvs(netflix_tvs, "Netflix", st.session_state.num_tv)
                if amazon_tvs:
                    display_tvs(amazon_tvs, "Amazon", st.session_state.num_tv)
                if disney_tvs:
                    display_tvs(disney_tvs, "Disney", st.session_state.num_tv)
        else:
            st.write("Please select a genre to get recommendations.")
            
#  ***********************  RECOMMENDATION SYSTEM  SECTION  ENDED HERE  ******************************
