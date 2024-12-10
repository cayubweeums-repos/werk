import flet as ft

class WorkoutCard(ft.UserControl):
    def __init__(self, workout_data, on_delete=None, on_edit=None):
        super().__init__()
        self.workout_data = workout_data
        self.on_delete = on_delete
        self.on_edit = on_edit
        
    def build(self):
        exercises_list = ft.Column([
            ft.Text(f"• {exercise['name']} - {exercise['sets']}x{exercise['reps']} @ {exercise['weight']}lbs")
            for exercise in self.workout_data["exercises"]
        ])
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(self.workout_data["name"], 
                               size=20, 
                               weight=ft.FontWeight.BOLD),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                on_click=self.edit_clicked
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                on_click=self.delete_clicked
                            )
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    exercises_list
                ]),
                padding=10
            )
        )
        
    def delete_clicked(self, e):
        if self.on_delete:
            self.on_delete(self.workout_data)
            
    def edit_clicked(self, e):
        if self.on_edit:
            self.on_edit(self.workout_data)
