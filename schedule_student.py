from z3 import *
import sys

def get_time_slot(var, sections):
    """
    Given an integer variable 'var' (representing the chosen section index)
    and a list of sections (tuples of (section_label, time_slot)), return a Z3
    expression representing the time slot for the chosen section.
    """
    expr = None
    for i, (_, time_slot) in enumerate(sections):
        expr = If(var == i, time_slot, expr) if expr is not None else If(var == i, time_slot, 0)
    return expr


# -------------------------------
# 1. Define Courses and Sections
# -------------------------------
# Each course is defined by its course code and a list of available sections.
# Each section is a tuple: (Section Label, Time Slot)
course_sections = {
    "EECS4401": [("A", 0), ("B", 1), ("C", 2)],
    "EECS1000": [("A", 1), ("B", 2), ("C", 3)],
    "MATH1000": [("A", 0), ("B", 2), ("C", 4)],
    "PHYS1000": [("A", 1), ("B", 3), ("C", 4)],
    "CHEM1000": [("A", 2), ("B", 3), ("C", 4)],
    "PSYC1000": [("A", 0), ("B", 3), ("C", 4)],
    "BIOL1000": [("A", 1), ("B", 2), ("C", 4)]
}

print("Available courses:")
for course in course_sections:
    print(f"  {course}")

# -------------------------------
# 2. Scan Student's Course Selection
# -------------------------------
# The student enters a comma-separated list of course codes to consider.
selected_input = input("Enter the course codes you want to consider (comma separated): ")
raw_courses = [course.strip() for course in selected_input.split(",")]

# Check for invalid course codes.
invalid_courses = [course for course in raw_courses if course not in course_sections]
if invalid_courses:
    print(f"Error: The following course codes are invalid: {', '.join(invalid_courses)}")
    sys.exit(1)

# Use only valid course codes.
selected_courses = raw_courses

# If more than 5 courses are provided, only consider the first 5.
if len(selected_courses) > 5:
    print("You have selected more than 5 courses. Only the first 5 will be considered.")
    selected_courses = selected_courses[:5]

# -------------------------------
# 3. Build the Z3 Model
# -------------------------------
solver = Solver()

# For each course, create two decision variables:
# - enroll: a Boolean indicating whether the course is taken.
# - section_choice: an integer representing the chosen section index.
enroll = {}
section_choice = {}
for course, sections in course_sections.items():
    enroll[course] = Bool(f"enroll_{course}")
    section_choice[course] = Int(f"section_{course}")
    # Constrain the section index to be within the valid range.
    solver.add(section_choice[course] >= 0, section_choice[course] < len(sections))
    # For courses not selected by the student, force enrollment to False.
    if course not in selected_courses:
        solver.add(enroll[course] == False)

# For courses in the student's selection, force enrollment to True.
for course in selected_courses:
    solver.add(enroll[course] == True)

# Constraint: The student can enroll in at most 5 courses.
solver.add(Sum([If(enroll[course], 1, 0) for course in course_sections]) <= 5)

# Constraint: If two courses are both enrolled, their chosen sections must not conflict.
all_courses = list(course_sections.keys())
for i in range(len(all_courses)):
    for j in range(i + 1, len(all_courses)):
        course_i = all_courses[i]
        course_j = all_courses[j]
        time_i = get_time_slot(section_choice[course_i], course_sections[course_i])
        time_j = get_time_slot(section_choice[course_j], course_sections[course_j])
        solver.add(Or(Not(enroll[course_i]), Not(enroll[course_j]), time_i != time_j))

# -------------------------------
# 4. Enumerate and Print All Valid Schedules
# -------------------------------
print("\nAll valid schedules:")

schedule_count = 0

# We build a blocking clause based only on the effective schedule for the student-selected courses.
while solver.check() == sat:
    m = solver.model()
    current_schedule = {}
    effective_clauses = []
    for course in selected_courses:
        # Enrollment is forced to True for selected courses.
        chosen_index = m.evaluate(section_choice[course]).as_long()
        section, time_slot = course_sections[course][chosen_index]
        current_schedule[course] = {"Section": section, "Time Slot": time_slot}
        effective_clauses.append(section_choice[course] == m[section_choice[course]])

    schedule_count += 1
    print(f"\nSchedule #{schedule_count}:")
    for course, details in current_schedule.items():
        print(f"  Course: {course} | Section: {details['Section']} | Time Slot: {details['Time Slot']}")
    total = len(selected_courses)
    print(f"  Total Enrolled Courses: {total}")

    # Block the current effective schedule.
    solver.add(Not(And(effective_clauses)))

print(f"\nTotal valid schedules found: {schedule_count}")