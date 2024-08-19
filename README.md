# werk
werk is a workout app that I always wished was out there

# prereqs

Install poetry and python

# Setup

```
git clone # this repo
cd werk
poetry install
```

# Setup local dev env
```
# For conventional commits and versioning
sudo apt-get install npm -y

npm install -g commitizen
```

For all commits
```
git cz
```

# Running
```
poetry run python main.py
```

# Symantics for devs
- Workouts = contain exercises and schedule to help users build their own plans and track when to do them
- Exercises = can be any lift or movement and contain a name, muscles worked, equipment needed, difficulty, instructions, and images
- Activities = are a log of a workout performed by a user and contains time&date started, duration, sets and reps performed, weights used at each point, user inputted notes for each set

# Design Reference Ideas
- https://dribbble.com/shots/16340251-Tasking-Task-manager-mobile-app
- https://dribbble.com/shots/23355141-Dashboard-HR-Management
- https://dribbble.com/shots/22303434-Fitness-App-UI

# Will leverage this db for lifts
- https://github.com/cayubweeums-repos/exercise-db
