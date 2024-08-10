import json
from utils import general, db_helpers

class Exercise:
    def __init__(self, name, level, mechanic, equipment, primaryMuscles, secondaryMuscles, instructions, category, images):
        
        self.name = name
        self.level = level
        self.mechanic = mechanic
        self.equipment = equipment
        self.primaryMuscles = primaryMuscles
        self.secondaryMuscles = secondaryMuscles
        self.instructions = instructions
        self.category = category
        self.images = images
 
    def to_dict(self):
        # Convert the object to a dictionary
        return {
            "name": self.name,
            "level": self.level,
            "mechanic": self.mechanic,
            "equipment": self.equipment,
            "primaryMuscles": self.primaryMuscles,
            "secondaryMuscles": self.secondaryMuscles,
            "instructions": self.instructions,
            "category": self.category,
            "images": self.images
        }

    @classmethod
    def from_dict(cls, data):
        # Create an instance of the class using the deserialized data
        return cls(
            name=data.get('username'),
            level=data.get('level'),
            mechanic=data.get('mechanic'),
            equipment=data.get('equipment'),
            primaryMuscles=data.get('primaryMuscles'),
            secondaryMuscles=data.get('secondaryMuscles'),
            instructions=data.get('instructions'),
            categroy=data.get('category'),
            images=data.get('images')
        )

    def __repr__(self):
        return f"Exercise(name={self.name}"
