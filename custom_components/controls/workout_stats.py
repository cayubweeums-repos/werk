import flet as ft
from datetime import datetime

class WorkoutSummaryCard(ft.Container):
    def __init__(self, workout_data):
        super().__init__()
        self.padding = 10
        self.border_radius = 10
        self.bgcolor = ft.colors.SURFACE_VARIANT
        
        start_time = datetime.fromisoformat(workout_data["start_time"])
        end_time = datetime.fromisoformat(workout_data["end_time"])
        duration = end_time - start_time
        
        self.content = ft.Column([
            ft.Text(
                workout_data["workout_name"],
                size=24,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                f"Date: {start_time.strftime('%Y-%m-%d %H:%M')}",
                size=16
            ),
            ft.Text(
                f"Duration: {duration.total_seconds() / 60:.1f} minutes",
                size=16
            ),
            ft.Divider(),
            self._build_exercise_summary(workout_data["exercise_logs"])
        ])

    def _build_exercise_summary(self, exercise_logs):
        exercise_columns = []
        for exercise_name, data in exercise_logs.items():
            total_volume = sum(
                perf["actual_weight"] * perf["actual_reps"]
                for perf in data["set_performances"]
            )
            
            exercise_columns.append(
                ft.Column([
                    ft.Text(exercise_name, size=18, weight=ft.FontWeight.W_500),
                    ft.Text(f"Sets completed: {len(data['set_performances'])}"),
                    ft.Text(f"Total volume: {total_volume} lbs")
                ])
            )
        return ft.Column(exercise_columns)

class PerformanceMetricCard(ft.Container):
    def __init__(self, title, value, subtitle=""):
        super().__init__()
        self.padding = 15
        self.border_radius = 8
        self.bgcolor = ft.colors.SURFACE_VARIANT
        
        self.content = ft.Column([
            ft.Text(title, size=16, color=ft.colors.ON_SURFACE_VARIANT),
            ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(subtitle, size=14, color=ft.colors.ON_SURFACE_VARIANT),
        ], spacing=5)
