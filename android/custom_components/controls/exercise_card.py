import flet as ft

class ExerciseCard(ft.UserControl):
    def __init__(self, exercise_name, on_delete=None):
        super().__init__()
        self.exercise_name = exercise_name
        self.on_delete = on_delete
        
    def build(self):
        self.weight_input = ft.TextField(
            label="Weight (lbs)",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.sets_input = ft.TextField(
            label="Sets",
            width=80,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.reps_input = ft.TextField(
            label="Reps",
            width=80,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(self.exercise_name, size=16, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=self.delete_clicked
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        self.weight_input,
                        self.sets_input,
                        self.reps_input
                    ])
                ]),
                padding=10
            )
        )
        
    def delete_clicked(self, e):
        if self.on_delete:
            self.on_delete(self)
