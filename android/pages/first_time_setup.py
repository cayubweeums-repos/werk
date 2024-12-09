import flet as ft
import logging
from repositories.storage_repository import StorageRepository
from repositories.config_repository import ConfigRepository

class Setup_Content:
    def __init__(self, page: ft.Page, config_repository: ConfigRepository, storage_repository: StorageRepository):
        self.page = page
        self.selected_storage = None
        self.logger = logging.getLogger("frontend_main")
        self.config_repository = ConfigRepository()
        self.storage_repository = storage_repository


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

    def storage_changed(self, e):
        self.selected_storage = e.control.value

    def setup_storage(self, e):
        try:
            if self.selected_storage == "local":
                # Initialize local storage DB
                self.storage_repository._service._init_db()
                
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
                # self.page.update()
                
            elif self.selected_storage == "hosted":
                self.logger.error("Self hosted storage not implemented yet, Selecting local storage instead")
                # Fallback to local storage
                self.storage_repository._service._init_db()
                
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
        return self.content
