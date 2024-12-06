import json
from utils import general, db_helpers

class User:
    def __init__(self, username, password, authenticated_session, workouts, exercises, activities):

        # Ensure required fields are provided
        if not username or not password:
            raise ValueError("All fields 'username' and 'password' are required.")

        self.username = username
        self.password = general.get_hashed_pass(password)
        self.authenticated_session = authenticated_session
        self.workouts = workouts
        self.exercises = exercises
        self.activities = activities
 
    def to_dict(self):
        # Convert the object to a dictionary
        return {
            "username": self.username,
            "password": self.password,
            "authenticated_session": self.authenticated_session,
            "workouts": self.workouts,
            "exercises": self.exercises,
            "activities": self.activities
        }

    @classmethod
    def from_dict(cls, data):
        # Create an instance of the class using the deserialized data
        return cls(
            username=data.get('username'),
            password=str(data.get('password')),
            authenticated_session=data.get('authenticated_session'),
            workouts=data.get('workouts'),
            exercises=data.get('exercises'),
            activities=data.get('activities')
        )

    def __repr__(self):
        return f"User(username={self.username}, authenticated_session={self.authenticated_session})"
