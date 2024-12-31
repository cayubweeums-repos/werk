import flet as ft
import datetime
from custom_components.controls.workout_timer_circle import WorkoutTimerCircle
from custom_components.controls.set_logger import SetLogger

class Workout_Performance_Content:
    def __init__(self, page: ft.Page, storage_repository, workout_data):
        self.page = page
        self.storage = storage_repository
        self.workout_data = workout_data
        self.current_exercise_index = 0
        self.current_set = 1
        self.is_resting = False
        
        # Initialize performance tracking dictionary
        self.performance_data = {
            'workout_id': workout_data['id'],
            'workout_name': workout_data['name'],
            'start_time': datetime.datetime.now().isoformat(),
            'exercise_logs': {}
        }
        
        # Initialize exercise logs structure
        for exercise in workout_data['exercises']:
            self.performance_data['exercise_logs'][exercise['name']] = {
                'planned_sets': exercise['sets'],
                'planned_reps': exercise['reps'],
                'planned_weight': exercise['weight'],
                'set_performances': []
            }
        
        # Initialize timer with first exercise
        current_exercise = self.workout_data["exercises"][0]
        self.timer_circle = WorkoutTimerCircle(
            current_set=self.current_set,
            total_sets=current_exercise["sets"],
            exercise_name=current_exercise["name"],
            expected_weight=current_exercise["weight"],
            expected_reps=current_exercise["reps"],
            cycle_duration=60
        )

        # Create logging fields (initially hidden)
        self.weight_input = ft.TextField(
            label="Weight (lbs)",
            value=str(current_exercise["weight"]),
            width=200,
            visible=False
        )
        self.reps_input = ft.TextField(
            label="Reps completed",
            value=str(current_exercise["reps"]),
            width=200,
            visible=False
        )
        self.notes_input = ft.TextField(
            label="Notes",
            width=200,
            multiline=True,
            visible=False
        )

        self.logging_column = ft.Column(
            controls=[
                self.weight_input,
                self.reps_input,
                self.notes_input
            ],
            visible=False
        )
        
        self.action_button = ft.ElevatedButton(
            text="Start Rest",
            on_click=self.toggle_rest,
            width=200,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            )
        )

        self.content = ft.Column(
            controls=[
                ft.Text(self.workout_data["name"], size=32, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.timer_circle,
                    alignment=ft.alignment.center,
                    padding=20
                ),
                self.logging_column,
                self.action_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def toggle_rest(self, e):
        self.is_resting = not self.is_resting
        
        if self.is_resting:
            # Starting rest period - show logging fields
            self.action_button.text = "Start Next Set"
            self.timer_circle.scale = 0.7  # Scale down
            self.timer_circle.start_timer()
            
            # Animate in logging fields
            self.logging_column.visible = True
            self.weight_input.visible = True
            self.reps_input.visible = True
            self.notes_input.visible = True
        else:
            # Ending rest period - hide logging fields
            self.action_button.text = "Complete Set"
            self.timer_circle.scale = 1.0  # Scale back to full size
            self.timer_circle.stop_timer()
            self.timer_circle.reset_timer()
            
            # Log the set and hide fields
            self.log_set()
            self.logging_column.visible = False
            self.advance_set()
        
        self.timer_circle.update()
        self.content.update()

    def log_set(self):
        current_exercise = self.workout_data["exercises"][self.current_exercise_index]
        exercise_name = current_exercise["name"]
        
        # Add set performance to tracking dictionary
        self.performance_data['exercise_logs'][exercise_name]['set_performances'].append({
            'set_number': self.current_set,
            'actual_weight': float(self.weight_input.value),
            'actual_reps': int(self.reps_input.value),
            'notes': self.notes_input.value
        })

    def advance_set(self):
        current_exercise = self.workout_data["exercises"][self.current_exercise_index]
        
        if self.current_set < int(current_exercise["sets"]):
            self.current_set += 1
        else:
            # Move to next exercise
            self.current_set = 1
            self.current_exercise_index += 1
            
            if self.current_exercise_index >= len(self.workout_data["exercises"]):
                self.complete_workout()
                return
            
            # Update set logger for new exercise
            next_exercise = self.workout_data["exercises"][self.current_exercise_index]
            self.set_logger.update_planned_values(
                weight=next_exercise["weight"],
                reps=next_exercise["reps"]
            )
        
        self.update_display()

    def update_display(self):
        current_exercise = self.workout_data["exercises"][self.current_exercise_index]
        
        # Update timer circle display
        self.timer_circle.set_text.value = f"Set {self.current_set}/{current_exercise['sets']}"
        self.timer_circle.exercise_text.value = current_exercise["name"]
        self.timer_circle.update()

    def complete_workout(self):
        # Add end time to performance data
        self.performance_data['end_time'] = datetime.datetime.now().isoformat()
        
        # Log the complete workout performance
        self.storage.log_workout(self.performance_data)
        self.page.go("/list_workout")

    def get_content(self):
        return self.content