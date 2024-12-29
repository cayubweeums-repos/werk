import flet as ft
import time
import threading

class WorkoutTimerCircle(ft.Container):
    def __init__(self, current_set, total_sets, exercise_name, expected_weight=0, expected_reps=0, cycle_duration=60):
        super().__init__()
        # Add animation property to container
        self.animate_scale = ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
        self.scale = 1.0
        # Timer state
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.update_thread = None
        self.cycle_duration = cycle_duration
        
        # Workout state
        self.current_set = current_set
        self.total_sets = total_sets
        self.exercise_name = exercise_name
        # Add expected values
        self.expected_weight = expected_weight
        self.expected_reps = expected_reps

        # Initialize UI components
        self.time_text = ft.Text(
            "00:00:00.000",
            size=28,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.progress_ring = ft.ProgressRing(
            width=200,
            height=200,
            stroke_width=8,
            value=0,
            color=ft.colors.BLUE,
        )

        # Add text displays for exercise and set info
        self.set_text = ft.Text(
            f"Set {current_set}/{total_sets}",
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.exercise_text = ft.Text(
            exercise_name,
            size=16,
            text_align=ft.TextAlign.CENTER,
        )

        # Add expected values display
        self.expected_values_text = ft.Text(
            f"Target: {expected_weight}lbs × {expected_reps} reps",
            size=16,
            text_align=ft.TextAlign.CENTER,
        )

        # Update container content to include new text elements
        self.content = ft.Column([
            self.set_text,
            ft.Stack([
                self.progress_ring,
                ft.Container(
                    content=self.time_text,
                    alignment=ft.alignment.center,
                    width=200,
                    height=200,
                ),
            ]),
            self.exercise_text,
            self.expected_values_text,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # def animate_size(self, is_resting: bool):
    #     # Animate between full size and compact size
    #     target_scale = 0.7 if is_resting else 1.0
    #     self.scale = ft.Scale(target_scale)
    #     self.update()

    def update_loop(self):
        target_fps = 60
        frame_time = 1.0 / target_fps
        
        while self.running:
            loop_start = time.time()
            
            current_time = time.time() - self.start_time
            hours = int(current_time // 3600)
            minutes = int((current_time % 3600) // 60)
            seconds = int(current_time % 60)
            milliseconds = int((current_time * 1000) % 1000)
            
            self.time_text.value = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
            self.progress_ring.value = (current_time % self.cycle_duration) / self.cycle_duration
            
            self.time_text.update()
            self.progress_ring.update()
            
            elapsed = time.time() - loop_start
            sleep_time = max(0, frame_time - elapsed)
            time.sleep(sleep_time)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.update_thread = threading.Thread(target=self.update_loop)
            self.update_thread.daemon = True
            self.update_thread.start()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            if self.update_thread:
                self.update_thread.join(timeout=0.1)

    def reset_timer(self):
        self.elapsed_time = 0
        self.time_text.value = "00:00:00.000"
        self.progress_ring.value = 0
        self.time_text.update()
        self.progress_ring.update()