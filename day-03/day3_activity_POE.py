
# ============================================================
# Name: YOUR NAME
# Student Number: YOUR STUDENT NUMBER
# Date: 19 November 2026
# Program: Learner Records Management System
# Description: Demonstrates collections, list algorithms,
# searching, sorting and learner record management.
# ============================================================


# ============================================================
# QUESTION 1: COLLECTIONS AND DATA STRUCTURES
# ============================================================

print("\nQUESTION 1: COLLECTIONS")

# 1.1 LIST
marks_2024001 = [65, 72, 48, 90, 55]

print("All marks:", marks_2024001)
print("First mark:", marks_2024001[0])
print("Last mark:", marks_2024001[-1])
print("First two marks:", marks_2024001[:2])


# 1.2 TUPLE
# A tuple is appropriate because the classroom coordinate
# is fixed and should not be changed.

classroom = (3, 5)

row, seat = classroom

print("Row:", row)
print("Seat:", seat)


# 1.3 SET
# A set automatically removes duplicate values.

modules = {"PRG", "NET", "DBS", "PRG", "NET"}

print("Module codes:", modules)
print("Unique module codes:", len(modules))
print("Is PRG available?", "PRG" in modules)


# 1.4 DICTIONARY
# A dictionary uses student numbers as unique keys.
# Each learner has a name and a list of marks.
# This makes searching and updating learner records easier.


# ============================================================
# QUESTION 2: FIRST-PRINCIPLES LIST ALGORITHMS
# ============================================================

print("\nQUESTION 2: LIST ALGORITHMS")


# 2.1 TOTAL
def total_of(values):
    total = 0

    for value in values:
        total = total + value

    return total


# 2.2 MEAN
def mean_of(values):
    if len(values) == 0:
        return None

    return total_of(values) / len(values)


# 2.3 MAXIMUM
def max_of(values):
    if len(values) == 0:
        return None

    highest = values[0]

    for value in values:
        if value > highest:
            highest = value

    return highest


# MINIMUM
def min_of(values):
    if len(values) == 0:
        return None

    lowest = values[0]

    for value in values:
        if value < lowest:
            lowest = value

    return lowest


# 2.4 RANGE
def range_of(values):
    if len(values) == 0:
        return None

    return max_of(values) - min_of(values)


# ABOVE MEAN
def above_mean(values):
    average = mean_of(values)

    if average is None:
        return []

    result = []

    for value in values:
        if value > average:
            result.append(value)

    return result


data = [65, 72, 48, 90, 55, 72, 48, 72]

print("Data:", data)
print("Total:", total_of(data))
print("Mean:", mean_of(data))
print("Highest:", max_of(data))
print("Lowest:", min_of(data))
print("Range:", range_of(data))
print("Above mean:", above_mean(data))


# ============================================================
# QUESTION 3: SEARCHING, DUPLICATES AND MODE
# ============================================================

print("\nQUESTION 3: SEARCHING AND MODE")


# 3.1 FIND FIRST
def find_first(values, target):

    for index in range(len(values)):
        if values[index] == target:
            return index

    return -1


# 3.2 FIND ALL
def find_all(values, target):
    indices = []

    for index in range(len(values)):
        if values[index] == target:
            indices.append(index)

    return indices


# 3.3 COUNT WITHOUT count()
def count_of(values, target):
    counter = 0

    for value in values:
        if value == target:
            counter = counter + 1

    return counter


# 3.4 MODE USING A FREQUENCY DICTIONARY
def mode_of(values):
    if len(values) == 0:
        return []

    frequency = {}

    for value in values:
        if value in frequency:
            frequency[value] = frequency[value] + 1
        else:
            frequency[value] = 1

    highest_frequency = 0

    for value in frequency:
        if frequency[value] > highest_frequency:
            highest_frequency = frequency[value]

    modes = []

    for value in frequency:
        if frequency[value] == highest_frequency:
            modes.append(value)

    return modes


print("First index of 72:", find_first(data, 72))
print("All indices of 72:", find_all(data, 72))
print("Count of 72:", count_of(data, 72))

tie_data = [10, 20, 10, 20, 30]

print("Tie data:", tie_data)
print("Modes:", mode_of(tie_data))


# ============================================================
# QUESTION 4: SORTING ALGORITHMS
# ============================================================

print("\nQUESTION 4: SORTING")


# 4.1 BUBBLE SORT
def bubble_sort(values):

    result = values[:]
    n = len(result)

    for i in range(n):

        for j in range(0, n - i - 1):

            if result[j] > result[j + 1]:

                # Swap adjacent values
                temp = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temp

    return result


# 4.2 SELECTION SORT
def selection_sort(values):

    result = values[:]
    n = len(result)

    for i in range(n):

        smallest = i

        for j in range(i + 1, n):

            if result[j] < result[smallest]:
                smallest = j

        # Swap the smallest value into position i
        temp = result[i]
        result[i] = result[smallest]
        result[smallest] = temp

    return result


# 4.3 TEST BOTH SORTING ALGORITHMS

original = [65, 72, 48, 90, 55, 72, 48, 72]

print("Original:", original)
print("Bubble sort:", bubble_sort(original))
print("Selection sort:", selection_sort(original))
print("Original after sorting:", original)

# Bubble sort swaps adjacent values.
# Selection sort finds the smallest remaining value
# and swaps it into its correct position.


# ============================================================
# QUESTION 5: INTERACTIVE LEARNER RECORDS
# ============================================================

print("\nQUESTION 5: LEARNER RECORD MANAGEMENT")

# Dictionary:
# Student number = key
# Name and marks = values

learners = {}


# VALIDATE MARKS
def get_valid_mark():

    while True:

        try:
            mark = float(input("Enter mark (0-100): "))

            if 0 <= mark <= 100:
                return mark

            print("Invalid mark! Enter between 0 and 100.")

        except ValueError:
            print("Please enter a numeric mark.")


# FIND LEARNER
def find_learner(student_number):

    if student_number in learners:
        return learners[student_number]

    return None


# 5.2 ADD LEARNER
def add_learner():

    student_number = input("Enter student number: ").strip()

    if student_number == "":
        print("Student number cannot be empty.")
        return

    if student_number in learners:
        print("This student number already exists.")
        return

    name = input("Enter learner name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    marks = []

    number_of_marks = int(input("How many marks? "))

    if number_of_marks < 1:
        print("Enter at least one mark.")
        return

    for i in range(number_of_marks):

        print("Mark", i + 1)
        mark = get_valid_mark()
        marks.append(mark)

    learners[student_number] = {
        "name": name,
        "marks": marks
    }

    print("Learner added successfully!")


# 5.3 SEARCH LEARNER
def search_learner():

    student_number = input("Enter student number: ").strip()

    learner = find_learner(student_number)

    if learner is not None:

        print("Student number:", student_number)
        print("Name:", learner["name"])
        print("Marks:", learner["marks"])

    else:
        print("Learner not found!")


# 5.4 UPDATE LEARNER NAME
def update_name():

    student_number = input("Enter student number: ").strip()

    learner = find_learner(student_number)

    if learner is not None:

        new_name = input("Enter new name: ").strip()

        if new_name != "":
            learner["name"] = new_name
            print("Name updated successfully.")
        else:
            print("Name cannot be empty.")

    else:
        print("Learner not found!")


# ADD A MARK
def add_mark():

    student_number = input("Enter student number: ").strip()

    learner = find_learner(student_number)

    if learner is not None:

        mark = get_valid_mark()
        learner["marks"].append(mark)

        print("Mark added successfully.")

    else:
        print("Learner not found!")


# DELETE LEARNER
def delete_learner():

    student_number = input("Enter student number: ").strip()

    if student_number in learners:

        confirm = input("Are you sure? (yes/no): ").lower()

        if confirm == "yes":
            del learners[student_number]
            print("Learner deleted successfully.")
        else:
            print("Deletion cancelled.")

    else:
        print("Learner not found!")


# 5.5 DISPLAY RANKING
def display_ranking():

    if len(learners) == 0:
        print("No learner records available.")
        return

    ranking = []

    for student_number in learners:

        marks = learners[student_number]["marks"]

        average = mean_of(marks)

        ranking.append((average, student_number))

    # Bubble sort in descending order
    for i in range(len(ranking)):

        for j in range(0, len(ranking) - i - 1):

            if ranking[j][0] < ranking[j + 1][0]:

                temp = ranking[j]
                ranking[j] = ranking[j + 1]
                ranking[j + 1] = temp

    print("\nLEARNER RANKING")
    print("---------------------------------------")

    position = 1

    for average, student_number in ranking:

        name = learners[student_number]["name"]

        print(position, name, student_number,
              "Average:", round(average, 2))

        position = position + 1


# DISPLAY ALL LEARNERS
def display_all():

    if len(learners) == 0:
        print("No learner records available.")
        return

    for student_number in learners:

        print("\nStudent number:", student_number)
        print("Name:", learners[student_number]["name"])
        print("Marks:", learners[student_number]["marks"])


# MENU
def main_menu():

    while True:

        print("\n================================")
        print("       LEARNER MANAGEMENT")
        print("================================")
        print("1. Add learner")
        print("2. Search learner")
        print("3. Update learner name")
        print("4. Add mark")
        print("5. Delete learner")
        print("6. Display ranking")
        print("7. Display all learners")
        print("0. Exit")
        print("================================")

        choice = input("Select an option: ")

        if choice == "1":
            add_learner()

        elif choice == "2":
            search_learner()

        elif choice == "3":
            update_name()

        elif choice == "4":
            add_mark()

        elif choice == "5":
            delete_learner()

        elif choice == "6":
            display_ranking()

        elif choice == "7":
            display_all()

        elif choice == "0":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice! Try again.")


# ============================================================
# QUESTION 6: TESTING
# ============================================================

print("\nQUESTION 6: TESTING")

# Test 1: Empty list
print("Empty total:", total_of([]))
print("Empty mean:", mean_of([]))
print("Empty maximum:", max_of([]))
print("Empty minimum:", min_of([]))
print("Empty mode:", mode_of([]))

# Test 2: One mark
print("One mark total:", total_of([80]))
print("One mark mean:", mean_of([80]))

# Test 3: Repeated marks
print("Repeated marks count:",
      count_of([70, 70, 80, 70], 70))

# Test 4: Tied modes
print("Tied modes:", mode_of([10, 20, 10, 20]))

# Test 5: Missing target
print("Missing target:", find_first(data, 100))
print("Missing learner:", find_learner("9999999"))

print("\nAll demonstration tests completed.")


# START THE INTERACTIVE MENU
main_menu()
