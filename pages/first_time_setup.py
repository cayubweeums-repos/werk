import flet as ft
import logging
import os
import json
import httpx
from repositories.config_repository import ConfigRepository

class Setup_Content:
    def __init__(self, page: ft.Page, config_repository: ConfigRepository):
        self.page = page
        self.selected_storage = None
        self.ph = ft.PermissionHandler()
        self.logger = logging.getLogger("frontend_main")
        self.config_repository = ConfigRepository()

        self.content = ft.Column(
            [
                ft.Container(
                    content=ft.Column([
                        ft.Text("Welcome to Werk!", 
                            size=32, 
                            weight="bold",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text("Let's get you set up", 
                            size=20,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.OutlinedButton(
                            "Request Storage Permission",
                            data=ft.PermissionType.STORAGE,
                            on_click=self.request_permission,
                        ),
                        ft.Container(height=20),  # Spacing
                        ft.Divider(),
                        ft.Container(height=20),  # Spacing
                        ft.Text("Choose where to store your data:", 
                            size=16,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=20),  # Spacing
                        
                        ft.RadioGroup(
                            content=ft.Column([
                                ft.Radio(
                                    value="local", 
                                    label="Local Storage (on device)",
                                    fill_color=ft.Colors.SECONDARY 
                                ),
                                ft.Radio(
                                    value="hosted", 
                                    label="Self Hosted Database (requires self hosted db)",
                                    fill_color=ft.Colors.SECONDARY  
                                ),
                            ]),
                            on_change=self.storage_changed
                        ),
                        
                        ft.Container(height=30),  # Spacing
                        ft.ElevatedButton(
                            "Continue",
                            width=200,  # Fixed width
                            on_click=self.setup_storage,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color=ft.Colors.ON_PRIMARY,  
                                bgcolor=ft.Colors.PRIMARY,  
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=50,
                    alignment=ft.alignment.center,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

    def request_permission(self, e):
        o = ph.request_permission(e.control.data)
        page.add(ft.Text(f"Requested {e.control.data.name}: {o}"))

    def storage_changed(self, e):
        self.selected_storage = e.control.value

    def setup_storage(self, e):
        try:
            if self.selected_storage == "local":
                # Initialize local storage
                self._init_local_storage()
                self._fetch_and_store_exercises()

                # Set configs
                local_config = {"type": "sqlite"}
                self.config_repository.set_config("connection.config", local_config)
                self.config_repository.set_config("storage.type", "local")
                
                # Update UI elements
                self.page.bottom_appbar.visible = True
                self.page.floating_action_button.visible = True
                self.logger.debug('Made bottom visible')
                
                # Navigate to home
                self.logger.debug("Navigating to home")
                self.page.go("/")
                self.logger.debug("Gone to home")
                
            elif self.selected_storage == "hosted":
                self.logger.error("Self hosted storage not implemented yet, Selecting local storage instead")
                # Fallback to local storage
                self._init_local_storage()
                self._fetch_and_store_exercises()

                # Set configs
                local_config = {"type": "sqlite"}
                self.config_repository.set_config("connection.config", local_config)
                self.config_repository.set_config("storage.type", "local")
                
                # Update UI elements
                self.page.bottom_appbar.visible = True
                self.page.floating_action_button.visible = True
                self.logger.debug('Made bottom visible')
                
                # Navigate to home
                self.logger.debug("Navigating to home")
                self.page.go("/")
                self.logger.debug("Gone to home")

        except Exception as ex:
            self.logger.error(f"Error setting up storage: {str(ex)}")

    def get_content(self):
        self.page.overlay.append(ph)
        self.page.update()
        return self.content

    def _init_local_storage(self):
        """Initialize local storage structure"""
        
        data_dir = "./data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        storage_template = {
            "workouts": [],  # User created workout templates
            "workout_logs": []  # Logs of completed workouts
        }
        
        storage_path = os.path.join(data_dir, "local_storage.json")
        with open(storage_path, 'w') as f:
            json.dump(storage_template, f, indent=2)
        
        self.logger.debug(f"Initialized local storage at {storage_path}")

    def _fetch_and_store_exercises(self):
        """Fetch exercises from GitHub and store locally"""
        
        EXERCISES_URL = "https://raw.githubusercontent.com/cayubweeums-repos/exercise-db/main/dist/exercises.json"
        
        try:
            # Fetch exercises
            with httpx.Client() as client:
                response = client.get(EXERCISES_URL)
                response.raise_for_status()
                exercises = response.json()
                
            # Add autocomplete keys to each exercise
            for exercise in exercises:
                exercise['autocomplete_keys'] = self._generate_autocomplete_keys(exercise['name'])
                
            # Store exercises
            exercises_path = os.path.join("./data", "exercises.json")
            with open(exercises_path, 'w') as f:
                json.dump(exercises, f, indent=2)
                
            self.logger.debug(f"Successfully stored exercises with autocomplete keys at {exercises_path}")
            
        except Exception as e:
            self.logger.error(f"Error processing exercises: {str(e)}")
            raise

    def _generate_autocomplete_keys(self, exercise_name: str) -> str:
        """Generate space-separated substrings for autocomplete"""
        lower_name = exercise_name.lower()
        return " ".join([lower_name[:i] for i in range(1, len(lower_name) + 1)])
