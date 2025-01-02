"""
Imports
#------------------------------------------
"""
import flet as ft
import os
import logging
import datetime
from utils.theme import get_app_theme, get_dark_theme
from pages.base_page import create_bottom_app_bar, create_floating_action_button
from pages.home_page import Home_Content
from pages.first_time_setup import Setup_Content
from repositories.config_repository import ConfigRepository
from repositories.local_storage import LocalStorageRepository
from pages.workout_creation import Workout_Creation_Content
from pages.workout_list import Workout_List_Content
from pages.workout_performance import Workout_Performance_Content
from pages.performance_stats import Performance_Stats_Content


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
# Setup logging
FORMAT = '%(asctime)s %(levelname)-8s %(message)s'

logging.basicConfig(
    filename=f'./data/logs/{_time}.log',
    format=FORMAT,
    level=logging.DEBUG,
    datefmt="[%X]"
)

log = logging.getLogger("frontend_main")

def main(page: ft.Page):
    page.title = "W.I.P. Werk app"
    page.theme_mode = 'system'
    page.theme = get_app_theme()
    page.dark_theme = get_dark_theme()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    config_repository = ConfigRepository()
    storage_repository = LocalStorageRepository() # TODO this should be dynamic and be the local storage if the user picked it otherwise should be the remote storage 
    is_first_time = config_repository.check_initial_setup()

    # Initialize page contents and routing
    home_page = Home_Content(page, config_repository, storage_repository)
    setup_page = Setup_Content(page, config_repository)

    content_column = ft.Column(expand=True)

    def route_change(route):
        log.debug(f"First time: {is_first_time}")
        log.debug(f"Route change: {route.route}")
        troute = ft.TemplateRoute(page.route)
        content_column.controls.clear()

        if troute.match("/"):
            log.debug(f"ROUTING TO HOME")
            content_column.controls.append(home_page.get_content())
            page.bottom_appbar.visible = True
            page.floating_action_button.visible = True
        elif troute.match("/create_workout?:query"):
            print(f"ROUTING TO WORKOUT CREATION with edit mode")
            query_params = {}
            if "?" in page.route:
                query_string = page.route.split("?")[1]
                query_params = dict(param.split("=") for param in query_string.split("&"))
                print(f"parsed query params: {query_params}")
            # Check if editing existing workout
            if query_params.get("edit") == "true":
                print(f"if statement for editing existing workout")
                workout_id = query_params.get("workout_id")
                workouts = storage_repository.get_workouts()
                workout_data = next((w for w in workouts if w["id"] == workout_id), None)
                workout_creation_page = Workout_Creation_Content(page, storage_repository, workout_data=workout_data)
            content_column.controls.append(workout_creation_page.get_content())
        elif troute.match("/create_workout"):
            workout_creation_page = Workout_Creation_Content(page, storage_repository)
            content_column.controls.append(workout_creation_page.get_content())
        elif troute.match("/list_workout"):
            workout_list_page = Workout_List_Content(page, storage_repository)
            content_column.controls.append(
                workout_list_page.get_content()
            )
        elif troute.match("/perform_workout?:query"):
            workout_id = page.route.split("=")[1]
            workout_data = storage_repository.get_workout_by_id(workout_id)
            content_column.controls = [
                Workout_Performance_Content(
                    page,
                    storage_repository,
                    workout_data
                ).get_content()
            ]
        elif page.route == "/stats":
            content_column.controls = [Performance_Stats_Content(page).get_content()]
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