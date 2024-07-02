# main.py
import streamlit as st
from pg import account, home, system, search_movies,search_tv
import hydralit_components as hc
import pg.favourites as favourites, pg.watchlist as watchlist

st.set_page_config(layout="wide", page_title="StreamSight", page_icon="	:cinema:", initial_sidebar_state='collapsed')

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function): #requires_login=False):
        self.apps.append({
            "title": title,
            "function": function,
            # "requires_login": requires_login
        })

    def run(self):
        menu_data = [
            {'icon': "bi bi-grid-1x2-fill", 'label': "Recommendation System", 'ttip': "Recommended System"},
            {'icon': "fa fa-search", 'label': "Search", 'ttip': "Search Bar",
             'submenu':[{'label': "Movie", 'icon': "fa fa-film"},
                {'label': "TV Search", 'icon': "fa fa-film"},]},
            {'icon': "fa fa-list", 'label': "Watchlist", 'ttip': "Watchlist"},
            {'icon': "fa fa-list", 'label': "Favourite", 'ttip': "Favourite List"},
            {'icon': "fa fa-user", 'label': "Sign Up", 'ttip': "Sign Up"},
            
        ]
        over_theme = {'txc_inactive': 'black', 'menu_background': "#95BDFF", 'txc_active': 'snow'}
        
        menu_id = hc.nav_bar(
            menu_definition=menu_data,
            override_theme=over_theme,
            home_name='Home',
            hide_streamlit_markers=True,
            sticky_nav=False,
            sticky_mode='sticky',
        )

        # if 'signedout' not in st.session_state:
        #     st.session_state.signedout = False

        # if not st.session_state.signedout and menu_id != 'Sign Up':
        #     st.warning("Please log in to access this section.")
        #     account.app()
        #     return

        for item in self.apps:
            if menu_id == item['title']:
                st.title(f"StreamSight - :green[{item['title']}]")
                item['function']()
                break
                # if item['requires_login'] and not st.session_state.signedout:
                #     st.warning("Please log in to access this section.")
                #     account.app()
                
                # else:
                #     item['function']()
                # break


# Instantiate the app
multi_app = MultiApp()
multi_app.add_app("Sign Up", account.app)
multi_app.add_app("Home", home.app)
multi_app.add_app("Recommendation System", system.app)
multi_app.add_app("Movie", search_movies.app)
multi_app.add_app("TV Search",search_tv.app)
multi_app.add_app("Watchlist", watchlist.app)
multi_app.add_app("Favourite", favourites.app)
multi_app.run()
# # Instantiate the app
# multi_app = MultiApp()
# multi_app.add_app("Sign Up", account.app)
# multi_app.add_app("Home", home.app)
# multi_app.add_app("Recommendation System", system.app, requires_login=True)
# multi_app.add_app("Movie", search_movies.app, requires_login=True)
# multi_app.add_app("TV Search",search_tv.app,requires_login=True)
# multi_app.add_app("Watchlist", watchlist.app, requires_login=True)
# multi_app.add_app("Favourite", favourites.app, requires_login=True)
# multi_app.run()