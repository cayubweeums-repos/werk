import json
from utils import general, db_helpers

class Exercise:
    def __init__(self, name, level, mechanic, equipment, primaryMuscles, secondaryMuscles, instructions, category, images):

        def generate_autocomplete_string():
            lower_name = name.lower()
            return " ".join([lower_name[:i] for i in range(1, len(lower_name) + 1)])
        
        self.name = name
        self.autocomplete_keys = generate_autocomplete_string()
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
            "autocomplete_keys": self.autocomplete_keys,
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
            name=data.get('name'),
            level=data.get('level'),
            mechanic=data.get('mechanic'),
            equipment=data.get('equipment'),
            primaryMuscles=data.get('primaryMuscles'),
            secondaryMuscles=data.get('secondaryMuscles'),
            instructions=data.get('instructions'),
            category=data.get('category'),
            images=data.get('images')
        )

    def __repr__(self):
        return f"Exercise(name={self.name}"
