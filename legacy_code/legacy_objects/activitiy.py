
import json
from utils import general, db_helpers

class Activity:
    def __init__(self, workout):
        
        self.workout = workout
        self.start_timedate = ''
        self.end_timedate = ''
        self.logs = {}
        
 
    def to_dict(self):
        # Convert the object to a dictionary
        return {
            "workout": self.workout,
            "start_timedate": self.start_timedate,
            "end_timedate": self.end_timedate,
            "logs": self.logs
        }

    @classmethod
    def from_dict(cls, data):
        # Create an instance of the class using the deserialized data
        return cls(
            workout=data.get('workout'),
            start_timedata=data.get('start_timedate'),
            end_timedate=data.get('end_timedate'),
            logs=data.get('logs')
        )

    def __repr__(self):
        return f"Activity(workout={self.workout}, logs={self.logs})"
