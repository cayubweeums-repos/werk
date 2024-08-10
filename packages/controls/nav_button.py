import flet as ft


class NavIconButton(ft.UserControl):
    def __init__(self, icon, view):
        super().__init__()
        self.icon: ft.icons = icon
        self.view: str = view

    def go_to(self, e):
        self.page.go(self.view)

    def build(self):
        return ft.Container(
            content=ft.FloatingActionButton(
                icon = self.icon,
                on_click=self.go_to
            ),
            data=f"{self.view}",
        )

class NavTextButton(ft.UserControl):
    def __init__(self, text, view):
        super().__init__()
        self.text: text
        self.view: str = view

    def go_to(self, e):
        self.page.go(self.view)

    def build(self):
        return ft.Container(
            content=ft.FloatingActionButton(
                text = self.text,
                on_click=self.go_to
            ),
            data=f"{self.view}",
        )