from repositories.interfaces.storage_interface import StorageInterface

class LocalStorageRepository(StorageInterface):
    def __init__(self):
        self.exercises_path = "./data/exercises.json"
        self.storage_path = "./data/local_storage.json"
        
    def get_exercises(self):
        # Implementation for local JSON file
        pass
        
    def get_workouts(self):
        # Implementation for local JSON file
        pass

    def log_workout(self):
        # Implementation for local JSON file
        pass

    def save_workout(self, workout_data):
        """Save workout to local storage JSON file"""
        import json
        
        try:
            # Read existing storage
            with open(self.storage_path, 'r') as f:
                storage = json.load(f)
                
            # Add new workout
            storage['workouts'].append(workout_data)
            
            # Write back to file
            with open(self.storage_path, 'w') as f:
                json.dump(storage, f, indent=2)
                
        except Exception as e:
            raise Exception(f"Failed to save workout: {str(e)}")

    def get_exercise_suggestions(self):
        """Returns list of AutoCompleteSuggestion objects for exercises"""
        import json
        import flet as ft
        
        with open(self.exercises_path, 'r') as f:
            exercises = json.load(f)
            
        return [
            ft.AutoCompleteSuggestion(
                key=exercise['autocomplete_keys'],
                value=exercise['name']
            ) for exercise in exercises
        ]
