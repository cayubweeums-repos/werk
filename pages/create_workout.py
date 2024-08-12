import flet as ft
from utils import db_helpers
from packages.components.controls import NavTextButton
from packages.components.controls import ExerciseContainer
from objects.exercise import Exercise
from objects.workout import Workout
from objects.user import User

class Create_Workout_Page(ft.View):
    def __init__(self, page: ft.Page, log):
        super(Create_Workout_Page, self).__init__(
            route="/create_workout", horizontal_alignment="center", vertical_alignment="center"
        )
        self.page = page
        self.log = log
        
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Name Workout"),
            content=ft.Text("Enter the name for this workout"),
            actions=[
                ft.TextField(text_align = ft.TextAlign.CENTER, expand=1, read_only=False),
                ft.TextButton("Done", on_click=self.save_workout)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        
        self.included_exercises = {}
        
        # Get all autocomplete suggestions
        conn = db_helpers.connect_db('exercises')
        self.all_exercises = []
        self.all_suggestions = []
        for row in conn[2].find():
            self.all_exercises.append(Exercise.from_dict(row))
            self.all_suggestions.append(ft.AutoCompleteSuggestion(key=row['autocomplete_keys'], value=row['name']))
        
        
        self.controls = [
            ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.AutoComplete(
                        suggestions=self.all_suggestions,
                        on_select=self.add_exercise,
                    ),
                    ft.FloatingActionButton(
                        icon=ft.icons.SAVE,
                        on_click=self.open_dlg_modal,
                    ),
                    ft.FloatingActionButton(
                        icon=ft.icons.REMOVE,
                        on_click=self.remove_exercise,
                    )
                ]
            ),
            ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                controls=[]
            ),
            ft.Row(
                alignment = ft.MainAxisAlignment.END,
                vertical_alignment = ft.CrossAxisAlignment.END
            )
        ]
        

    def add_exercise(self, e):
        exercise_to_add = self.all_exercises[e.control.selected_index]
        self.controls[1].controls.append(ExerciseContainer(exercise_to_add))
        self.page.update()

    def remove_exercise(self, e):
        if self.controls[1].controls:
            self.controls[1].controls.pop()
        else:
            self.log.debug('Cannot remove exercise from list when it is empty')
        self.page.update()

    def open_dlg_modal(self, e):
        e.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        e.page.update()
        
    def save_workout(self, e):
        workout_name = self.dlg_modal.actions[0].value
        self.dlg_modal.open = False
        if self.controls[1].controls:
            for i in self.controls[1].controls:
                self.log.error(i.return_values())
                exercise = i.return_values()['object']
                self.included_exercises[exercise.name] = {
                    'object': exercise.to_dict(),
                    'sets': i.return_values()['sets'],
                    'reps': i.return_values()['reps'],
                    'weight': [225] * int(i.return_values()['sets'])
                }
        workout = Workout(workout_name, self.included_exercises)
        user = User.from_dict(db_helpers.get_row_db('users', 'authenticated_session', e.page.session_id))
        user.workouts[workout.name] = workout.to_dict()
        
        db_helpers.update_user_field_db(user.username, 'workouts', user.workouts, self.log)
        
        self.page.update()
        
        self.page.go(f"/home")
        