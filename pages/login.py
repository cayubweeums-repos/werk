import flet as ft
from utils import db_helpers

class Login_Page(ft.View):
    def __init__(self, page: ft.Page, log):
        super(Login_Page, self).__init__(
            route="/", horizontal_alignment="center", vertical_alignment="center"
        )
        self.page = page
        
        self.log = log
        
        self.text_username: ft.TextField = ft.TextField(label='Username', width=200, on_change=self.validate)
        self.text_password: ft.TextField = ft.TextField(label='Password', width=200, password=True, on_change=self.validate)
        self.button_submit: ft.ElevatedButton = ft.ElevatedButton(text='Login', width=200, disabled=True, on_click=self.submit)
        

        self.controls = [
            ft.Column(
                alignment = 'center',
                controls=[
                    self.text_username,
                    self.text_password,
                    self.button_submit
                ]
            )
        ]

    def validate(self, e: ft.ControlEvent) -> None:
        if all([self.text_username.value, self.text_password.value]):
            self.button_submit.disabled = False
        else:
            self.button_submit.disabled = True
            
        self.page.update()

    def submit(self, e: ft.ControlEvent) -> None:
        if db_helpers.auth_user('users', self.text_username.value, self.text_password.value, self.page.session_id, self.log):
            self.page.go(f"/home")
        else:
            self.controls.append(
                ft.Text(value='Bad Username or Password try again scrub')
            )
            self.page.update()
