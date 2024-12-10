import flet as ft
from custom_components.controls.exercise_card import ExerciseCard

class Workout_Creation_Content:
    def __init__(self, page: ft.Page, storage_repository):
        self.page = page
        self.storage = storage_repository
        self.exercise_cards = []
        
        # Get exercise suggestions
        self.suggestions = self.storage.get_exercise_suggestions()
        
        # Search field
        self.exercise_search = ft.AutoComplete(
            suggestions=self.suggestions,
            on_select=self.add_exercise
        )
        
        # Container for exercise cards
        self.exercises_column = ft.Column(scroll=ft.ScrollMode.AUTO)
        
        self.workout_name = ft.TextField(label="Workout Name", width=400)
        
        self.content = ft.Column([
            ft.Text("Create Workout", size=32, weight=ft.FontWeight.BOLD),
            self.workout_name,
            self.exercise_search,
            self.exercises_column,
            ft.ElevatedButton(
                text="Save Workout",
                on_click=self.save_workout
            )
        ])

    def save_workout(self, e):
        workout_data = {
            "name": self.workout_name.value,
            "exercises": [
                {
                    "name": card.exercise_name,
                    "weight": card.weight_input.value,
                    "sets": card.sets_input.value,
                    "reps": card.reps_input.value
                }
                for card in self.exercise_cards
            ]
        }
        
        try:
            self.storage.save_workout(workout_data)
            # Show success message
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Workout saved!")))
            self.page.go("/")
        except Exception as e:
            # Show error message
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error saving workout: {str(e)}")))
        
    def add_exercise(self, e):
        if e.selection.value:
            card = ExerciseCard(
                e.selection.value,
                on_delete=self.remove_exercise
            )
            self.exercise_cards.append(card)
            self.exercises_column.controls.append(card)
            self.exercise_search.value = ""
            self.page.update()
            
    def remove_exercise(self, card):
        self.exercise_cards.remove(card)
        self.exercises_column.controls.remove(card)
        self.page.update()
        
    def get_content(self):
        return self.content
