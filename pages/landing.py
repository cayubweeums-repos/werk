import flet as ft
from utils import db_helpers
from packages.components.controls import NavTextButton

class Landing_Page(ft.View):
    def __init__(self, page: ft.Page, log):
        super(Landing_Page, self).__init__(
            route="/home", horizontal_alignment="center", vertical_alignment="center"
        )
        self.page = page
        
        self.log = log

        
        self.controls = [
            ft.Column(
                controls=[
                    NavTextButton('create workout', f"/create_workout")
                ]
            )
        ]