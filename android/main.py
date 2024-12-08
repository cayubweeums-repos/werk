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
from pages.base_page import create_bottom_app_bar, create_floating_action_button
from pages.home_page import Home_Content
from pages.first_time_setup import Setup_Content
from services.storage_service import LocalStorageService
from repositories.storage_repository import StorageRepository
from repositories.config_repository import ConfigRepository



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

    storage_service = LocalStorageService()
    storage_repository = StorageRepository(storage_service)
    config_repository = ConfigRepository()
    is_first_time = config_repository.check_initial_setup()

    # Initialize page contents and routing
    home_page = Home_Content(page, config_repository)
    setup_page = Setup_Content(page, config_repository, storage_repository)

    content_column = ft.Column(expand=True)

    def route_change(route):
        log.debug(f"First time: {is_first_time}")
        log.debug(f"Route change: {route.route}")
        troute = ft.TemplateRoute(page.route)
        content_column.controls.clear()

        if is_first_time:
            content_column.controls.append(setup_page.get_content())
            # Hide navigation elements for setup
            page.bottom_appbar.visible = False
            page.floating_action_button.visible = False
        else:
            if troute.match("/"):
                log.debug(f"ROUTEING TO HOME")
                content_column.controls.append(home_page.get_content())
                page.bottom_appbar.visible = True
                page.floating_action_button.visible = True
            else:
                log.debug(f"NO MATCH FOUND, ROUTING TO HOME")
                content_column.controls.append(home_page.get_content())
                page.bottom_appbar.visible = True
                page.floating_action_button.visible = True

        page.update()

    page.on_route_change = route_change

    page.bottom_appbar = create_bottom_app_bar(page)
    page.floating_action_button = create_floating_action_button()
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.add(
        ft.Row(
            [
                ft.Column(
                    [content_column],
                    expand=True
                )
            ],
            expand=True
        )
    )

    if is_first_time:
        content_column.controls.append(setup_page.get_content())
        # Hide navigation elements for setup
        page.bottom_appbar.visible = False
        page.floating_action_button.visible = False
        page.update()
        is_first_time = False
    else:
        page.go("/")

ft.app(main)