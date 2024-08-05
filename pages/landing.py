import flet as ft

class Landing_Page(ft.View):
    def __init__(self, page: ft.Page, log):
        super(Landing_Page, self).__init__(
            route="/", horizontal_alignment="center", vertical_alignment="center"
        )
        self.page = page
        
        self.log = log
        
        self.controls = [
            ft.Row(
                alignment = 'center',
                controls=[
                    ft.ElevatedButton("button 1", on_click=self.button1),
                    ft.ElevatedButton("button 2", on_click=self.button2)
                ]
            )
        ]


    def button1(self, e):
        self.log.info("button1 pressed")
        
    def button2(self, e):
        self.log.info("button2 pressed")