import json
from utils import general, db_helpers

class Workout:
    def __init__(self, name, included_exercises):
        
        self.name = name
        self.included_exercises = included_exercises
 
    def to_dict(self):
        # Convert the object to a dictionary
        return {
            "name": self.name,
            "included_exercises": self.included_exercises
        }

    @classmethod
    def from_dict(cls, data):
        # Create an instance of the class using the deserialized data
        return cls(
            name=data.get('username'),
            included_exercises=data.get('included_exercises'),
        )

    def __repr__(self):
        return f"Workout(name={self.name}, included_exercises={self.included_exercises})"
    
    