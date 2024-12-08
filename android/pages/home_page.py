import flet as ft
import os
from time import sleep
import logging


class Home_Content:
    def __init__(self, page, config_repository):
        self.page = page
        self.config_repository = config_repository
        self.logger = logging.getLogger("frontend_main")

        self.page.update()

        self.content = ft.Column(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Doing things with stuff",
                            size=16,
                            italic=True,
                            text_align="center",
                        ),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Get Started",
                            icon=ft.icons.ROCKET_LAUNCH,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                            )
                        ),
                        ft.Container(
                            content=ft.Markdown(
                                self.get_config_markdown(),
                                selectable=True,
                            ),
                            padding=50,
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=50,
            ),
            ft.ResponsiveRow(
                [
                    # ft.Column([feature_card(ft.icons.SECURITY, "Secure Analysis", "Analyze malware safely in an interactive sandbox environment")], col={"sm": 12, "md": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    # ft.Column([feature_card(ft.icons.AUTO_AWESOME, "API-Powered", "Secure API for deep integration with other systems")], col={"sm": 12, "md": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    # ft.Column([feature_card(ft.icons.SPEED, "Real-time Results", "Get instant insights into potential threats")], col={"sm": 12, "md": 4}, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def get_content(self):
        return self.content

    def get_config_markdown(self):
        try:
            storage_type = self.config_repository.get_config("storage.type")
            connection_config = self.config_repository.get_config("connection.config")
            
            return f"""
                # Current Configuration

                ## Storage Type
                `{storage_type}`

                ## Connection Config
                ```json
                {connection_config}
            """ 

        except Exception as e:
            self.logger.error(f"Error formatting config: {str(e)}") 
            return "# Error loading configuration"


