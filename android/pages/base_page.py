import flet as ft

def create_bottom_app_bar(page: ft.Page):
    return ft.BottomAppBar(
        bgcolor=ft.Colors.ON_SURFACE_VARIANT,
        shape=ft.NotchShape.CIRCULAR, # can also be AUTO
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.FITNESS_CENTER,
                    icon_color=ft.Colors.PRIMARY,
                    icon_size=32,
                    on_click=lambda _: page.go('/list_workout')

                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.HOME,
                    icon_color=ft.Colors.PRIMARY,
                    icon_size=32,
                    on_click=lambda _: page.go('/')
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_color=ft.Colors.PRIMARY,
                    icon_size=32,
                    on_click=lambda _: page.go('/create_workout')
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.BAR_CHART,
                    icon_color=ft.Colors.PRIMARY,
                    icon_size=32,
                    on_click=lambda _: page.go('/stats')
                ),
            ]
        ),
    )

def create_floating_action_button():
    return ft.FloatingActionButton(
        icon=ft.Icons.FITNESS_CENTER,
        bgcolor=ft.Colors.SECONDARY,
        content=ft.Icon(
            name=ft.Icons.FITNESS_CENTER,
            color=ft.Colors.ON_SECONDARY,
            size=40,
        ),
        width=70,
        height=70,
    )
