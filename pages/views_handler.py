import flet as ft

from pages.landing import Landing_Page

def views_handler(page, log):
    land = Landing_Page(page, log)
    return {
        '/': land,
    }

