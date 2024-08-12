import flet as ft

from pages.login import Login_Page
from pages.landing import Landing_Page
from pages.create_workout import Create_Workout_Page

def views_handler(page, log):
    land = Landing_Page(page, log)
    login = Login_Page(page, log)
    create_workout = Create_Workout_Page(page, log)
    return {
        '/': login,
        '/home': land,
        '/create_workout': create_workout,
    }

