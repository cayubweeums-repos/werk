import os
import json
import logging

class ConfigRepository:
    def __init__(self):
        self.config_path = "./data/config.json"
        self.logger = logging.getLogger("frontend_main")
        
    def get_config(self, key: str):
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get(key)
        except Exception as e:
            self.logger.error(f"Error reading config: {str(e)}")
            return None
            
    def set_config(self, key: str, value: any):
        try:
            # Create config.json if it doesn't exist
            if not os.path.exists(self.config_path):
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w') as f:
                    json.dump({}, f)
            
            # Read existing config or start with empty dict
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                config = {}
                
            # Update and save config
            config[key] = value
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
                
        except Exception as e:
            self.logger.error(f"Error writing config: {str(e)}")
            
    def check_initial_setup(self) -> bool:
        try:
            if not os.path.exists(self.config_path):
                return True
            storage_type = self.get_config("storage.type")
            connection_config = self.get_config("connection.config")
            return not all([storage_type, connection_config])
        except Exception as e:
            self.logger.error(f"Error checking setup: {str(e)}")
            return True
