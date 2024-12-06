import flet as ft

def get_app_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE,
            primary_container=ft.Colors.BLUE_100,
            secondary=ft.Colors.ORANGE,
            secondary_container=ft.Colors.ORANGE_100,
            surface_variant=ft.Colors.BLUE_50,
            on_secondary=ft.Colors.WHITE,
        )
    )

def get_dark_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_700,
            primary_container=ft.Colors.BLUE_900,
            secondary=ft.Colors.ORANGE_700,
            secondary_container=ft.Colors.ORANGE_900,
            surface_variant=ft.Colors.BLUE_900,
            on_secondary=ft.Colors.WHITE,
        )
    )
