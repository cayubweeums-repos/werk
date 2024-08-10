import flet as ft
from utils import db_helpers
from packages.controls.nav_button import Nav

class Landing_Page(ft.View):
    def __init__(self, page: ft.Page, log):
        super(Landing_Page, self).__init__(
            route="/home", horizontal_alignment="center", vertical_alignment="center"
        )
        self.page = page
        
        self.log = log
        
        # Get all autocomplete suggestions
        conn = db_helpers.connect_db('exercises')
        all_suggestions = []
        for row in conn[2].find():
            all_suggestions.append(ft.AutoCompleteSuggestion(key=row['autocomplete_keys'], value=row['name']))
        
        
        self.controls = [
            ft.Column(
                controls=[
                    ft.AutoComplete(
                        suggestions=all_suggestions,
                        on_select=lambda e: print(e.control.selected_index, e.selection),
                    )
                ]
            )
        ]


    def button1(self, e):
        self.log.info("button1 pressed")
        
    def button2(self, e):
        self.log.info("button2 pressed")