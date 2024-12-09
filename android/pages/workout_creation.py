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
        
        self.content = ft.Column([
            ft.Text("Create Workout", size=32, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Workout Name", width=400),
            self.exercise_search,
            self.exercises_column
        ])
        
    def add_exercise(self, e):
        #print(e.control.selection)
        print(e.selection.value)
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
