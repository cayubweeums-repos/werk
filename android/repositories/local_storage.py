import os
import json
import flet as ft
import uuid
from repositories.interfaces.storage_interface import StorageInterface

class LocalStorageRepository(StorageInterface):
    def __init__(self):
        self.exercises_path = "./data/exercises.json"
        self.storage_path = "./data/local_storage.json"
        
    def get_exercises(self):
        # Implementation for local JSON file
        pass
        
    def get_workouts(self):
        """Get all workouts from local storage"""
        
        try:
            # Create storage file if it doesn't exist
            if not os.path.exists(self.storage_path):
                os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
                with open(self.storage_path, 'w') as f:
                    json.dump({'workouts': []}, f)
            
            # Read workouts
            with open(self.storage_path, 'r') as f:
                storage = json.load(f)
                return storage.get('workouts', [])
                
        except Exception as e:
            raise Exception(f"Failed to get workouts: {str(e)}")

    def log_workout(self):
        # Implementation for local JSON file
        pass

    def save_workout(self, workout_data):
        """Save workout to local storage JSON file"""
        
        try:
            # Read existing storage
            with open(self.storage_path, 'r') as f:
                storage = json.load(f)
                    
            # Add unique ID if not present
            if 'id' not in workout_data:
                workout_data['id'] = str(uuid.uuid4())
                
            # Add new workout
            storage['workouts'].append(workout_data)
                
            # Write back to file
            with open(self.storage_path, 'w') as f:
                json.dump(storage, f, indent=2)
                    
        except Exception as e:
            raise Exception(f"Failed to save workout: {str(e)}")

    def get_exercise_suggestions(self):
        """Returns list of AutoCompleteSuggestion objects for exercises"""
        
        with open(self.exercises_path, 'r') as f:
            exercises = json.load(f)
            
        return [
            ft.AutoCompleteSuggestion(
                key=exercise['autocomplete_keys'],
                value=exercise['name']
            ) for exercise in exercises
        ]

    def delete_workout(self, workout_data):
        """Delete workout from local storage"""
        
        try:
            # Read existing storage
            with open(self.storage_path, 'r') as f:
                storage = json.load(f)
            
            # Filter out the workout to delete
            storage['workouts'] = [
                w for w in storage['workouts'] 
                if w['name'] != workout_data['name']  # Using name as unique identifier
            ]
            
            # Write back to file
            with open(self.storage_path, 'w') as f:
                json.dump(storage, f, indent=2)
                
        except Exception as e:
            raise Exception(f"Failed to delete workout: {str(e)}")

    def update_workout(self, workout_data):
        """Update existing workout in local storage"""
        
        try:
            # Read existing storage
            with open(self.storage_path, 'r') as f:
                storage = json.load(f)
            
            # Find and update workout by ID
            for i, workout in enumerate(storage['workouts']):
                if workout.get('id') == workout_data['id']:
                    storage['workouts'][i] = workout_data
                    break
            
            # Write back to file
            with open(self.storage_path, 'w') as f:
                json.dump(storage, f, indent=2)
                
        except Exception as e:
            raise Exception(f"Failed to update workout: {str(e)}")
