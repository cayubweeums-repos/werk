import flet as ft

def create_bottom_app_bar(page: ft.Page):
    return ft.BottomAppBar(
        bgcolor=ft.colors.SURFACE_VARIANT,
        shape=ft.NotchShape.CIRCULAR, # can also be AUTO
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.FITNESS_CENTER,
                    icon_color=ft.Colors.PRIMARY,
                    icon_size=32,

                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.HISTORY,
                    icon_color=ft.Colors.PRIMARY,
                    icon_size=32,
                ),
            ]
        ),
    )

def create_floating_action_button():
    return ft.FloatingActionButton(
        icon=ft.icons.FITNESS_CENTER,
        bgcolor=ft.colors.SECONDARY,
        content=ft.Icon(
            name=ft.icons.FITNESS_CENTER,
            color=ft.colors.ON_SECONDARY,
            size=40,
        ),
        width=70,
        height=70,
    )
