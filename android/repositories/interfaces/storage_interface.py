from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def get_exercises(self):
        pass
        
    @abstractmethod 
    def get_workouts(self):
        pass
        
    @abstractmethod
    def save_workout(self, workout):
        pass
        
    @abstractmethod
    def log_workout(self, workout_log):
        pass

    @abstractmethod
    def get_exercise_suggestions(self):
        """Get all exercise autocomplete suggestions"""
        pass
