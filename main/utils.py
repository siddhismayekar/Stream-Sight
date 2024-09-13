#utils.py
import streamlit as st
import requests
from api import api_key,access_token

def initialize_session_state():
    if 'watchlist_movies' not in st.session_state:
        st.session_state.watchlist_movies = []
    if 'watchlist_tv_shows' not in st.session_state:
        st.session_state.watchlist_tv_shows = []
    if 'favourite_movies' not in st.session_state:
        st.session_state.favourite_movies = []
    if 'favourite_tv_shows' not in st.session_state:
        st.session_state.favourite_tv_shows = []


#************************************* MOVIE APIs ******************************************************
popular_movies_data = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}", ).json()
trending_movies_data = requests.get(f"https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}", ).json()
# Function to fetch movie poster
def get_movie_poster(movie_id, api_key):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}", ).json()
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w400" + data['poster_path']
    return None 


# Search Movies API using GET
def search_movies(query, api_key, providers_data):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": api_key,  
        "include_adult": False,
        "language": "en",
        "query": query
    }
    response = requests.get(url, params=params, )
    if response.status_code == 200:
        data = response.json()
        movies = data.get('results', [])
        results = []
        for movie in movies:
            poster_url = get_movie_poster(movie['id'], api_key)
            provider_name = get_provider_name(movie['id'], providers_data)
            title = movie.get('title')  # Get the movie title
            release_date = movie.get('release_date')  # Get the release date
            overview=movie.get('overview')
            results.append({
                'title': title,
                'release_date': release_date,
                'poster_url': poster_url,
                'provider_name': provider_name,
                'overview':overview,
            })
        return results
    else:
        return []

def get_provider_name(movie_id, providers_data):
    # Fetch providers_data from the API
    providers_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}", )

    # Check if the response is successful
    if providers_response.status_code == 200:
        providers_data = providers_response.json()
    provider_names = []
    for country_code, country_data in providers_data.get('results', {}).items():
        if 'flatrate' in country_data:
            for provider in country_data['flatrate']:
                provider_name = provider.get('provider_name')
                if provider_name in ['Netflix', 'Amazon Prime Video', 'Prime Video', 'Disney Plus']:
                    provider_names.append(provider_name)
    # Return the first provider name found, or None if none are found
    provider_name = provider_names[0] if provider_names else None
    return provider_name

#Function to fetch provider name and poster
def fetch_provider_and_poster(movie_id):
    providers_data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}&language=en-US", ).json()
    provider_name = None
    poster_url = None
    for country_code, country_data in providers_data.get('results', {}).items():
        if 'flatrate' in country_data:
            for provider in country_data['flatrate']:
                provider_name = provider.get('provider_name')
                if provider_name == 'Netflix':
                    provider_name = 'Netflix'
                    poster_url = get_movie_poster(movie_id, api_key)
                    return provider_name, poster_url
                elif provider_name in ['Amazon Prime Video', 'Prime Video']:
                    provider_name = 'Amazon Prime Video'
                    poster_url = get_movie_poster(movie_id, api_key)
                    return provider_name, poster_url
                elif provider_name == 'Disney Plus':
                    provider_name = 'Disney Plus'
                    poster_url = get_movie_poster(movie_id, api_key)
                    return provider_name, poster_url
    return provider_name, poster_url

#************************************* MOVIE APIs ENDED HERE******************************************************

#************************************************ TV SHOW API *************************************************
# Fetch popular TV shows data
url = "https://api.themoviedb.org/3/tv/popular"
headers = {
    "accept": "application/json",
    "Authorization": access_token
}
popular_tv_shows_data = requests.get(url, headers=headers, ).json()

# Fetch trending TV shows data
url = "https://api.themoviedb.org/3/trending/tv/day"
trending_tv_shows_data = requests.get(url, headers=headers, ).json()

# Function to fetch TV show poster
def get_tv_show_poster(tv_show_id, access_token):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}"
    headers = {
        "accept": "application/json",
        "Authorization": access_token
    }
    try:
        response = requests.get(url, headers=headers, )
        response.raise_for_status()
        data = response.json()
        if 'poster_path' in data and data['poster_path'] is not None:
            return "https://image.tmdb.org/t/p/w400" + data['poster_path']
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Search TV shows using GET
def search_tv_shows(query, access_token):
    url = "https://api.themoviedb.org/3/search/tv"
    params = {
        "query": query,
        "include_adult": False,
    }
    headers = {
        "accept": "application/json",
        "Authorization": access_token
    }
    response = requests.get(url, headers=headers, params=params, )
    if response.status_code == 200:
        data = response.json()
        tv_shows = data.get('results', [])
        results = []
        for tv_show in tv_shows:
            poster_url = get_tv_show_poster(tv_show['id'], access_token)
            providers_data = get_tv_providers_data(tv_show['id'], access_token)
            provider_name = get_tv_provider_name(providers_data)
            name = tv_show.get('name')
            first_air_date = tv_show.get('first_air_date')
            overview = tv_show.get('overview')
            results.append({
                'name': name,
                'release_date': first_air_date,
                'poster_url': poster_url,
                'provider_name': provider_name,
                'overview': overview,
            })
        return results
    else:
        print(f"Failed to fetch search results. Status code: {response.status_code}")
        return []

def get_tv_providers_data(tv_show_id, access_token):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}/watch/providers"
    headers = {
        "accept": "application/json",
        "Authorization": access_token
    }
    response = requests.get(url, headers=headers, )
    if response.status_code == 200:
        return response.json().get('results', {})
    else:
        return {}

def get_tv_provider_name(providers_data):
    provider_names = []
    for country_code, country_data in providers_data.items():
        if 'flatrate' in country_data:
            for provider in country_data['flatrate']:
                provider_name = provider.get('provider_name')
                if provider_name in ['Netflix', 'Amazon Prime Video', 'Prime Video','Amazon Video','Disney Plus',]:
                    provider_names.append(provider_name)
    return provider_names[0] if provider_names else None

# Function to fetch provider name and poster
def fetch_tv_provider_and_poster(tv_show_id):
    providers_data = get_tv_providers_data(tv_show_id, access_token)
    provider_name = get_tv_provider_name(providers_data)
    poster_url = get_tv_show_poster(tv_show_id, access_token)
    return provider_name, poster_url
