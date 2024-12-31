from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def get_exercises(self):
        pass
        
    @abstractmethod 
    def get_workouts(self):
        pass
        
    @abstractmethod
    def save_workout(self, workout_data):
        """Save workout to configured storage"""
        pass
        
    @abstractmethod
    def log_workout(self, workout_log):
        pass

    @abstractmethod
    def get_exercise_suggestions(self):
        """Get all exercise autocomplete suggestions"""
        pass

    def delete_workout(self, workout_data):
        """Delete workout from storage"""
        pass
        
    def update_workout(self, workout_data):
        """Update existing workout in storage"""
        pass

    def get_workout_by_id(self, workout_id: str):
        """Get specific workout by ID from storage"""
        pass
