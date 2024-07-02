# favourites.py
import streamlit as st
from utils import initialize_session_state
from firebase_admin import firestore

# Initialize session state variables at the start
initialize_session_state()

def app():
    st.title("Your Favourites")

    st.header("Movies")
    if not st.session_state.favourite_movies:
        st.write("Your favourite movies list is empty.")
    else:
        display_items(st.session_state.favourite_movies, remove_from_favourite_movies)

    st.header("TV Shows")
    if not st.session_state.favourite_tv_shows:
        st.write("Your favourite TV shows list is empty.")
    else:
        display_items(st.session_state.favourite_tv_shows, remove_from_favourite_tv_shows)


def display_items(items, remove_callback):
    num_columns = 7
    for i in range(0, len(items), num_columns):
        cols = st.columns(num_columns)
        for j, item in enumerate(items[i:i+num_columns]):
            with cols[j]:
                item_title = item.get('title') or item.get('name', 'Unknown Title')
                st.write(f"**{item_title}**")
                st.image(item['poster_url'], width=200)
                st.write(f"Provider: {item['provider_name']}")
                st.button("Remove", key=f"remove_{i+j}_{item_title}", on_click=remove_callback, args=(item,))

# def add_to_favourite_movies(movie):
#     st.session_state.favourite_movies.append(movie)
#     save_to_firestore()

# def add_to_favourite_tv_shows(tv_show):
#     st.session_state.favourite_tv_shows.append(tv_show)
#     save_to_firestore()
def add_to_favourite_movies(movie):
    if 'username' not in st.session_state or not st.session_state.username:
        st.warning("Please log in to access this.")
    else:
        st.session_state.favourite_movies.append(movie)
        save_to_firestore()

def add_to_favourite_tv_shows(tv_show):
    if 'username' not in st.session_state or not st.session_state.username:
        st.warning("Please log in to access this.")
    else:
        st.session_state.favourite_tv_shows.append(tv_show)
        save_to_firestore()
def remove_from_favourite_movies(movie):
    st.session_state.favourite_movies = [m for m in st.session_state.favourite_movies if m != movie]
    st.success(f"{movie['title']} has been removed from your favourites.")
    save_to_firestore()

def remove_from_favourite_tv_shows(tv_show):
    tv_show_name = tv_show.get('title') or tv_show.get('name', 'Unknown Title')
    st.session_state.favourite_tv_shows = [t for t in st.session_state.favourite_tv_shows if t != tv_show]
    st.success(f"{tv_show_name} has been removed from your favourites.")
    save_to_firestore()

def save_to_firestore():
    db = firestore.client()
    doc_ref = db.collection('users').document(st.session_state.username)
    doc_ref.update({
        'favourite_movies': st.session_state.favourite_movies,
        'favourite_tv_shows': st.session_state.favourite_tv_shows
    })
