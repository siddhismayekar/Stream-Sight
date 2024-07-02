import streamlit as st
import firebase_admin
from firebase_admin import firestore, credentials, auth
import requests
import api
import os
from dotenv import load_dotenv
load_dotenv()

# Extract the Firebase credentials from st.secrets
firebase_credentials = {
    "type": st.secrets["firebase_credentials"]["type"],
    "project_id": st.secrets["firebase_credentials"]["project_id"],
    "private_key_id": st.secrets["firebase_credentials"]["private_key_id"],
    "private_key": st.secrets["firebase_credentials"]["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["firebase_credentials"]["client_email"],
    "client_id": st.secrets["firebase_credentials"]["client_id"],
    
}

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
def app():
    st.title('Welcome To :blue[StreamSight]')

    # Initialize session state variables
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'reason' not in st.session_state:
        st.session_state.reason = ''
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    if 'watchlist_movies' not in st.session_state:
        st.session_state.watchlist_movies = []
    if 'watchlist_tv_shows' not in st.session_state:
        st.session_state.watchlist_tv_shows = []
    if 'favourite_movies' not in st.session_state:
        st.session_state.favourite_movies = []
    if 'favourite_tv_shows' not in st.session_state:
        st.session_state.favourite_tv_shows = []

    # Function to handle login
    def handle_login(email, password):
        try:
            # Firebase sign-in endpoint
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api.WebAPIKey}"

            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }

            response = requests.post(url, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                user_id = response_data['localId']
                st.session_state.username = user_id
                st.session_state.useremail = email

                # Retrieve user data from Firestore
                db = firestore.client()
                doc_ref = db.collection('users').document(user_id)
                doc = doc_ref.get()
                if doc.exists:
                    user_data = doc.to_dict()
                    st.session_state.reason = user_data.get('reason', '')
                    st.session_state.watchlist_movies = user_data.get('watchlist_movies', [])
                    st.session_state.watchlist_tv_shows = user_data.get('watchlist_tv_shows', [])
                    st.session_state.favourite_movies = user_data.get('favourite_movies', [])
                    st.session_state.favourite_tv_shows = user_data.get('favourite_tv_shows', [])

                st.session_state.signedout = True
                st.session_state.signout = True
                st.success("Login Successfully")
            else:
                st.warning('Login Failed: ' + response_data.get('error', {}).get('message', 'Unknown error'))

        except Exception as e:
            st.warning('Login Failed: ' + str(e))

    # Function to handle logout
    def handle_logout():
        st.session_state.signedout = False
        st.session_state.signout = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.session_state.reason = ''
        st.session_state.watchlist_movies = []
        st.session_state.watchlist_tv_shows = []
        st.session_state.favourite_movies = []
        st.session_state.favourite_tv_shows = []

    # Function to handle password reset
    def handle_password_reset(email):
        try:
            # Firebase password reset endpoint
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api.WebAPIKey}"

            payload = {
                "requestType": "PASSWORD_RESET",
                "email": email
            }

            response = requests.post(url, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                st.success("Password reset email sent successfully")
            else:
                st.warning('Password reset failed: ' + response_data.get('error', {}).get('message', 'Unknown error'))

        except Exception as e:
            st.warning('Password reset failed: ' + str(e))

    # Function to handle account deletion
    def handle_account_deletion():
        try:
            user_id = st.session_state.username

            # Delete user from authentication
            auth.delete_user(user_id)

            # Delete user data from Firestore
            db = firestore.client()
            doc_ref = db.collection('users').document(user_id)
            doc_ref.delete()

            # Clear session state
            handle_logout()

            st.success("Account deleted successfully")
        except Exception as e:
            st.warning('Account deletion failed: ' + str(e))

    # Show login/signup,reset psswd form if not signed in
    if not st.session_state.signedout:
        choice = st.selectbox('Login | Signup | Forget Password', ['Login', 'Sign up', 'Forget Password'])

        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            st.button('Login', on_click=handle_login, args=(email, password))

        elif choice == 'Sign up':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')
            username = st.text_input("Enter your unique username")
            reason = st.radio("What's your reason to visit",
                ["Reports", "Suggestion", "Search", "Other"],
                
            )

            if st.button('Create my account'):
                try:
                    user = auth.create_user(email=email, password=password, uid=username)
                    st.session_state.reason = reason
                    # Add the reason to Firestore
                    db = firestore.client()
                    doc_ref = db.collection('users').document(user.uid)
                    doc_ref.set({
                        'email': email,
                        'username': username,
                        'reason': reason,
                        'watchlist_movies': [],
                        'watchlist_tv_shows': [],
                        'favourite_movies': [],
                        'favourite_tv_shows': []
                    }, merge=True)
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()
                except Exception as e:
                    st.error('Account creation failed: ' + str(e))

        elif choice == 'Forget Password':
            email = st.text_input('Enter your email address to reset password')
            if st.button('Reset Password'):
                handle_password_reset(email)

    # Show user info if signed in
    if st.session_state.signout:
        st.text('Name: ' + st.session_state.username)
        st.text('Email ID: ' + st.session_state.useremail)
        st.text('Reason: ' + st.session_state.reason)
        c,b =st.columns([1,2])
        with c:
            st.button('Sign out', on_click=handle_logout)
        with b:
            st.button('Delete Account', on_click=handle_account_deletion)
