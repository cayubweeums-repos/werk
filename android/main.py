"""
Imports
#------------------------------------------
"""
import flet as ft
import os
import logging
import datetime
from rich.logging import RichHandler
from rich.traceback import install
from rich import pretty
from utils.theme import get_app_theme, get_dark_theme
from pages.base_page import create_app_bar, create_side_panel
from pages.home_page import Home_Content

"""
Dir setup
#------------------------------------------
"""
_time = datetime.date.today()
if not os.path.exists('./data'):
    os.makedirs('./data')
    os.makedirs('./data/logs')
elif not os.path.exists('./data/logs'):
    os.makedirs('./data/logs')

"""
Logging config
#------------------------------------------
"""
FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
logging.basicConfig(filename='./data/logs/{}.log'.format(_time), format=FORMAT, level=logging.DEBUG, datefmt="[%X]")
log = logging.getLogger("frontend_main")
log.addHandler(RichHandler())

def main(page: ft.Page):
    page.title = "W.I.P. Werk app"
    page.theme_mode = 'system'
    page.theme = get_app_theme()
    page.dark_theme = get_dark_theme()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Initialize page contents and routing
    home_page = Home_Content(page)
    # settings_page = Settings_Content(page)

    def route_change(route):
        troute = ft.TemplateRoute(page.route)
        content_column.controls.clear()

        if troute.match("/"):
            content_column.controls.append(home_page.get_content())
        # elif troute.match("/tasks/:task_id"):
        #     task_page = Task_Content(page, troute.task_id)
        #     content_column.controls.append(task_page.get_content())
        else:
            content_column.controls.append(home_page.get_content())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def change_view(view_name, task_id=None):
        if view_name == "home":
            page.go("/")
        # elif view_name == "task" and task_id is not None:
        #     page.go(f"/tasks/{task_id}")

    content_column = ft.Column(expand=True)
    sidebar = create_side_panel(change_view)

    def toggle_sidebar(e):
        sidebar.width = 200 if sidebar.width == 0 else 0
        sidebar.update()

    page.appbar = create_app_bar(page, toggle_sidebar)

    page.add(
        ft.Row(
            [
                sidebar,
                ft.Column(
                    [content_column],
                    expand=True
                )
            ],
            expand=True
        )
    )

    page.go("/")

ft.app(main)