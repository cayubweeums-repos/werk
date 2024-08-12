import flet as ft
from objects.exercise import Exercise

class ExerciseContainer(ft.UserControl):
    def __init__(self, exercise):
        super().__init__()
        self.exercise: Exercise = exercise
        self.num_of_sets: ft.TextField = ft.TextField(label="Sets", value='5')
        self.num_of_reps: ft.TextField = ft.TextField(label="Reps", value='5')

    # TODO returns the Exercise and the final amount of recorded sets and reps to be performed
    def return_values(self):
        return {
            'object': self.exercise,
            'sets': self.num_of_sets.value,
            'reps': self.num_of_reps.value
        }

    def build(self):
        return ft.Container(
            expand=True,
            content=ft.Row(
                controls=[
                    ft.Column(
                        alignment = 'left',
                        controls=[
                            ft.Text(self.exercise.name)
                        ]
                    ),
                    ft.Column(
                        alignment = 'right',
                        controls=[
                            self.num_of_sets,
                            ft.Text('x'),
                            self.num_of_reps
                        ]
                    )
                ]
            )
        )
        
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
        self.text = text
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