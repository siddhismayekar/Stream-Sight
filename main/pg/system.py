#system.py
# importing libaries

from streamlit_option_menu import option_menu
from pg import system_movies,system_tv

def app():
    class MultiTabs:
        def __init__(self):
            self.tabs = []

        def add_tab(self, title, function):
            self.tabs.append({
                "title": title,
                "function": function
            })

        def run_tab(self):
            
            tab = option_menu(None, ["Movies Recommendation","TV Show Recommendation",],
                            icons=["bi bi-camera-reels","bi bi-tv",], 
                            menu_icon=None, default_index=0, orientation="horizontal",
                            styles={
                        "container": {"background-color": "#15304e",},
                        "icon": {"color": "black", "font-size": "20px"}, 
                        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"3px", "--hover-color": "#639CD9"},
                        "nav-link-selected": {"background-color": "#176B87"},
                    })

            for item in self.tabs:
                if tab == item['title']:
                    item['function']()

    multi_tab = MultiTabs()
    multi_tab.add_tab("Movies Recommendation", system_movies.tab)
    multi_tab.add_tab("TV Show Recommendation", system_tv.tab)
    multi_tab.run_tab()