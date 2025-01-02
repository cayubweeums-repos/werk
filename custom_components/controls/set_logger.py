import flet as ft

class SetLogger(ft.Container):
    def __init__(self, planned_weight, planned_reps):
        super().__init__()
        self.planned_weight = planned_weight
        self.planned_reps = planned_reps

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.TextField(
                    label="Weight (lbs)",
                    value=str(self.planned_weight),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    width=150
                ),
                ft.TextField(
                    label="Reps completed",
                    value=str(self.planned_reps),
                    keyboard_type=ft.KeyboardType.NUMBER,
                    width=150
                ),
                ft.TextField(
                    label="Notes",
                    multiline=True,
                    min_lines=2,
                    max_lines=4,
                    width=300
                )
            ])
        )
