import flet as ft
import json
import os
from custom_components.controls.workout_stats import WorkoutSummaryCard, PerformanceMetricCard

class Performance_Stats_Content:
    def __init__(self, page: ft.Page):
        self.page = page
        
        # Create scrollable content
        self.content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=20,
            controls=self._build_content()
        )

    def _build_content(self):
        try:
            if not os.path.exists("./data/workout_logs.json"):
                return [ft.Text("No workout data available", size=20)]
                
            with open("./data/workout_logs.json", "r") as f:
                data = json.load(f)
                
            if not data.get("workout_logs"):
                return [ft.Text("No workout data available", size=20)]
                
            controls = []
            
            # Add summary metrics at the top
            total_workouts = len(data["workout_logs"])
            
            metrics_row = ft.Row([
                PerformanceMetricCard(
                    "Total Workouts",
                    str(total_workouts),
                    "Completed"
                ),
                PerformanceMetricCard(
                    "Last Workout",
                    data["workout_logs"][-1]["workout_name"],
                    "Most Recent"
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
            
            controls.append(metrics_row)
            controls.append(ft.Divider())
            
            # Add individual workout cards
            for workout in reversed(data["workout_logs"]):
                controls.append(WorkoutSummaryCard(workout))
            
            return controls
            
        except Exception as e:
            return [ft.Text(f"Error loading workout data: {str(e)}", size=20)]

    def get_content(self):
        return self.content
