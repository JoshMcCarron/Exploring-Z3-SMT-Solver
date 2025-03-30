from z3 import *

# -------------------------------
# 1. Define the Problem Domain
# -------------------------------

# Courses and their assigned professors.
courses = {
    "EECS4401": "Prof_A",
    "EECS3401": "Prof_A",
    "MATH1000": "Prof_B",
    "MATH1001": "Prof_B",
    "PSYC1000": "Prof_C",
    "PSYC1001": "Prof_C",
    "PHYS1000": "Prof_D"
}

# Number of available time slots (e.g., 0, 1, 2, 3)
num_slots = 4

# Number of available rooms (e.g., rooms 0, 1, 2)
num_rooms = 3

# -------------------------------
# 2. Set Up Z3 Variables & Solver
# -------------------------------

solver = Solver()

# Create an integer variable for each course representing its time slot.
course_slots = {course: Int(course) for course in courses}
# Create an integer variable for each course representing its assigned room.
course_rooms = {course: Int("room_" + course) for course in courses}

# Each course must be assigned a time slot between 0 and num_slots-1.
for course, slot_var in course_slots.items():
    solver.add(slot_var >= 0, slot_var < num_slots)

# Each course must be assigned a room between 0 and num_rooms-1.
for course, room_var in course_rooms.items():
    solver.add(room_var >= 0, room_var < num_rooms)

# -------------------------------
# 3. Encode Scheduling Constraints
# -------------------------------

# Constraint 1: If two courses are taught by the same professor,
# they cannot be scheduled at the same time.
for course1 in courses:
    for course2 in courses:
        if course1 < course2 and courses[course1] == courses[course2]:
            solver.add(course_slots[course1] != course_slots[course2])

# Constraint 2: If two courses are scheduled at the same time,
# they cannot be assigned the same room.
for course1 in courses:
    for course2 in courses:
        if course1 < course2:
            solver.add(Implies(course_slots[course1] == course_slots[course2],
                                course_rooms[course1] != course_rooms[course2]))

# (Additional constraints such as room limits per course or capacity constraints can be added here.)

# -------------------------------
# 4. Solve and Display the Schedule
# -------------------------------

if solver.check() == sat:
    model = solver.model()
    print("Z3-Generated Schedule:")
    for course in courses:
        time_slot = model[course_slots[course]]
        room = model[course_rooms[course]]
        professor = courses[course]
        print(f"  {course} (taught by {professor}) -> Time Slot {time_slot}, Room {room}")
else:
    print("No valid schedule found.")
