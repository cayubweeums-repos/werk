import flet as ft

def create_app_bar(page: ft.Page, toggle_sidebar):
    return ft.AppBar(
        title=ft.Text("werk"),
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=toggle_sidebar),
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

def create_side_panel(change_view):
    return ft.Container(
        content=ft.Column(
            [
                # ft.Container(height=40),
                ft.Text("Menu", size=20, weight="bold"),
                ft.TextButton("Home", icon=ft.icons.HOME, on_click=lambda e: change_view('home')),
                ft.TextButton("Dashboard", icon=ft.icons.DASHBOARD, on_click=lambda e: change_view("dashboard")),
                ft.TextButton("Reports", icon=ft.icons.ASSESSMENT),
                ft.TextButton("Settings", icon=ft.icons.SETTINGS, on_click=lambda e: change_view("settings")),
            ],
            # tight=True,
        ),
        bgcolor=ft.colors.SURFACE_VARIANT,
        width=0,
        animate=ft.animation.Animation(300, "decelerate"),
        padding=ft.padding.only(left=20, top=20, bottom=20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )
