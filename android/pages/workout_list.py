import flet as ft
from custom_components.controls.workout_card import WorkoutCard

class Workout_List_Content:
    def __init__(self, page: ft.Page, storage_repository):
        self.page = page
        self.storage = storage_repository
        
        self.workouts_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=10
        )
        
        self.content = ft.Column([
            ft.Text("My Workouts", size=32, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                text="Create New Workout",
                on_click=lambda _: self.page.go('/create_workout')
            ),
            self.workouts_column
        ], scroll=ft.ScrollMode.AUTO)  # Add scroll here
        
        self.load_workouts()
        
    def load_workouts(self):
        workouts = self.storage.get_workouts()
        self.workouts_column.controls = [
            WorkoutCard(
                workout_data=workout,
                on_delete=self.delete_workout,
                on_edit=self.edit_workout
            )
            for workout in workouts
        ]
        self.page.update()
        
    def delete_workout(self, workout_data):
        try:
            # Add delete_workout method to storage interface
            self.storage.delete_workout(workout_data)
            self.load_workouts()
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Workout deleted!"))
            )
        except Exception as e:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Error deleting workout: {str(e)}"))
            )
            
    def edit_workout(self, workout_data):
        self.page.go(f'/create_workout?edit=true&workout_id={workout_data["id"]}')
        
    def get_content(self):
        return self.content
