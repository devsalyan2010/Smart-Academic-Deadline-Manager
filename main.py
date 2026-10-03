import csv
import os
from datetime import datetime


# -------------------------------------------------
# FILE LOCATION
# -------------------------------------------------

# Always use assignments.csv from the same folder
# where main.py is located.

FILE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assignments.csv"
)


# -------------------------------------------------
# LOAD ASSIGNMENTS
# -------------------------------------------------

def load_assignments():

    assignments = []

    if os.path.exists(FILE_NAME):

        with open(FILE_NAME, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                row["difficulty"] = int(row["difficulty"])
                row["hours"] = float(row["hours"])

                assignments.append(row)

    return assignments


# -------------------------------------------------
# SAVE ASSIGNMENTS
# -------------------------------------------------

def save_assignments(assignments):

    with open(FILE_NAME, "w", newline="") as file:

        fieldnames = [
            "subject",
            "name",
            "deadline",
            "difficulty",
            "hours",
            "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(assignments)


# -------------------------------------------------
# CALCULATE DAYS REMAINING
# -------------------------------------------------

def calculate_days_remaining(deadline):

    deadline_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    ).date()

    today = datetime.now().date()

    difference = deadline_date - today

    return difference.days


# -------------------------------------------------
# GET DEADLINE STATUS
# -------------------------------------------------

def get_deadline_status(days_remaining):

    if days_remaining < 0:

        return "OVERDUE"

    elif days_remaining == 0:

        return "DUE TODAY"

    elif days_remaining <= 3:

        return "DUE SOON"

    else:

        return "UPCOMING"


# -------------------------------------------------
# CALCULATE PRIORITY SCORE
# -------------------------------------------------

def calculate_priority(assignment):

    days_remaining = calculate_days_remaining(
        assignment["deadline"]
    )

    difficulty = assignment["difficulty"]
    hours = assignment["hours"]


    # Deadline score
    if days_remaining <= 1:

        deadline_score = 100

    elif days_remaining <= 3:

        deadline_score = 80

    elif days_remaining <= 7:

        deadline_score = 60

    elif days_remaining <= 14:

        deadline_score = 40

    else:

        deadline_score = 20


    # Difficulty score
    difficulty_score = difficulty * 33.33


    # Workload score
    if hours >= 8:

        workload_score = 100

    elif hours >= 5:

        workload_score = 80

    elif hours >= 3:

        workload_score = 60

    elif hours >= 1:

        workload_score = 40

    else:

        workload_score = 20


    # Weighted priority score
    priority_score = (
        deadline_score * 0.50
        + difficulty_score * 0.30
        + workload_score * 0.20
    )


    return round(priority_score, 2)


# -------------------------------------------------
# GET PRIORITY LEVEL
# -------------------------------------------------

def get_priority_level(score):

    if score >= 70:

        return "HIGH"

    elif score >= 40:

        return "MEDIUM"

    else:

        return "LOW"


# -------------------------------------------------
# LOAD SAVED DATA
# -------------------------------------------------

assignments = load_assignments()


# -------------------------------------------------
# PROGRAM TITLE
# -------------------------------------------------

print("========================================")
print(" Smart Academic Deadline & Workload Manager")
print("========================================")


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------

while True:

    print("\n========== MAIN MENU ==========")

    print("1. Add Assignment")
    print("2. View Assignments")
    print("3. Search Assignments")
    print("4. Priority Analysis")
    print("5. Workload Analysis")
    print("6. Update Assignment Status")
    print("7. Student Dashboard")
    print("8. Exit")


    choice = input("Enter your choice: ")


    # =================================================
    # 1. ADD ASSIGNMENT
    # =================================================

    if choice == "1":

        print("\n========== ADD ASSIGNMENT ==========")


        subject = input(
            "Enter subject: "
        ).strip()

        if subject == "":

            print(
                "Subject cannot be empty."
            )

            continue


        assignment_name = input(
            "Enter assignment name: "
        ).strip()

        if assignment_name == "":

            print(
                "Assignment name cannot be empty."
            )

            continue


        deadline = input(
            "Enter deadline (YYYY-MM-DD): "
        ).strip()


        try:

            deadline_date = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            print(
                "\nInvalid date format."
            )

            print(
                "Please use YYYY-MM-DD."
            )

            continue


        today = datetime.now().date()


        if deadline_date < today:

            print(
                "\nWarning: This deadline "
                "is already past."
            )

            confirm = input(
                "Do you still want to add it? (y/n): "
            ).lower()


            if confirm != "y":

                print(
                    "Assignment not added."
                )

                continue


        difficulty = input(
            "Enter difficulty (1-3): "
        ).strip()


        if difficulty not in ["1", "2", "3"]:

            print(
                "\nInvalid difficulty."
            )

            print(
                "Enter 1, 2, or 3."
            )

            continue


        estimated_hours = input(
            "Enter estimated completion time (hours): "
        ).strip()


        try:

            estimated_hours = float(
                estimated_hours
            )

        except ValueError:

            print(
                "\nPlease enter a valid number."
            )

            continue


        if estimated_hours <= 0:

            print(
                "\nEstimated hours must be"
                " greater than 0."
            )

            continue


        assignment = {

            "subject": subject,

            "name": assignment_name,

            "deadline": deadline,

            "difficulty": int(difficulty),

            "hours": estimated_hours,

            "status": "Pending"

        }


        assignments.append(assignment)

        save_assignments(assignments)


        print(
            "\nAssignment added successfully!"
        )

        print(
            "Data saved successfully."
        )


    # =================================================
    # 2. VIEW ASSIGNMENTS
    # =================================================

    elif choice == "2":

        print(
            "\n========== YOUR ASSIGNMENTS =========="
        )


        if len(assignments) == 0:

            print(
                "No assignments found."
            )

            continue


        for i, assignment in enumerate(
            assignments,
            start=1
        ):

            days_remaining = (
                calculate_days_remaining(
                    assignment["deadline"]
                )
            )


            deadline_status = (
                get_deadline_status(
                    days_remaining
                )
            )


            print(
                f"\nAssignment {i}"
            )

            print(
                "-------------------------"
            )

            print(
                "Subject:",
                assignment["subject"]
            )

            print(
                "Name:",
                assignment["name"]
            )

            print(
                "Deadline:",
                assignment["deadline"]
            )

            print(
                "Days Remaining:",
                days_remaining
            )

            print(
                "Deadline Status:",
                deadline_status
            )

            print(
                "Difficulty:",
                assignment["difficulty"]
            )

            print(
                "Estimated Hours:",
                assignment["hours"]
            )

            print(
                "Status:",
                assignment["status"]
            )


    # =================================================
    # 3. SEARCH ASSIGNMENTS
    # =================================================

    elif choice == "3":

        print(
            "\n========== SEARCH ASSIGNMENTS =========="
        )


        if len(assignments) == 0:

            print(
                "No assignments available."
            )

            continue


        search_subject = input(
            "Enter subject to search: "
        ).strip()


        if search_subject == "":

            print(
                "Search subject cannot be empty."
            )

            continue


        found = False


        for assignment in assignments:

            if (
                assignment["subject"].lower()
                == search_subject.lower()
            ):

                days_remaining = (
                    calculate_days_remaining(
                        assignment["deadline"]
                    )
                )


                deadline_status = (
                    get_deadline_status(
                        days_remaining
                    )
                )


                print(
                    "\nAssignment Found"
                )

                print(
                    "-------------------------"
                )

                print(
                    "Subject:",
                    assignment["subject"]
                )

                print(
                    "Name:",
                    assignment["name"]
                )

                print(
                    "Deadline:",
                    assignment["deadline"]
                )

                print(
                    "Days Remaining:",
                    days_remaining
                )

                print(
                    "Deadline Status:",
                    deadline_status
                )

                print(
                    "Difficulty:",
                    assignment["difficulty"]
                )

                print(
                    "Estimated Hours:",
                    assignment["hours"]
                )

                print(
                    "Status:",
                    assignment["status"]
                )


                found = True


        if not found:

            print(
                "No assignment found"
                " for this subject."
            )


    # =================================================
    # 4. PRIORITY ANALYSIS
    # =================================================

    elif choice == "4":

        print(
            "\n========== PRIORITY ANALYSIS =========="
        )


        if len(assignments) == 0:

            print(
                "No assignments available."
            )

            continue


        priority_list = []


        for assignment in assignments:

            score = calculate_priority(
                assignment
            )

            level = get_priority_level(
                score
            )


            priority_list.append(
                (
                    score,
                    level,
                    assignment
                )
            )


        priority_list.sort(
            reverse=True,
            key=lambda x: x[0]
        )


        for i, item in enumerate(
            priority_list,
            start=1
        ):

            score = item[0]
            level = item[1]
            assignment = item[2]


            days_remaining = (
                calculate_days_remaining(
                    assignment["deadline"]
                )
            )


            deadline_status = (
                get_deadline_status(
                    days_remaining
                )
            )


            print(
                f"\n{i}. "
                f"{assignment['subject']} - "
                f"{assignment['name']}"
            )

            print(
                "   Priority Score:",
                score
            )

            print(
                "   Priority Level:",
                level
            )

            print(
                "   Deadline:",
                assignment["deadline"]
            )

            print(
                "   Deadline Status:",
                deadline_status
            )

            print(
                "   Difficulty:",
                assignment["difficulty"]
            )

            print(
                "   Estimated Hours:",
                assignment["hours"]
            )


    # =================================================
    # 5. WORKLOAD ANALYSIS
    # =================================================

    elif choice == "5":

        print(
            "\n========== WORKLOAD ANALYSIS =========="
        )


        if len(assignments) == 0:

            print(
                "No assignments available."
            )

            continue


        total_hours = 0
        hours_due_soon = 0

        high_priority = 0
        medium_priority = 0
        low_priority = 0

        overdue_count = 0


        for assignment in assignments:

            total_hours += assignment["hours"]


            score = calculate_priority(
                assignment
            )

            level = get_priority_level(
                score
            )


            if level == "HIGH":

                high_priority += 1

            elif level == "MEDIUM":

                medium_priority += 1

            else:

                low_priority += 1


            days_remaining = (
                calculate_days_remaining(
                    assignment["deadline"]
                )
            )


            if days_remaining < 0:

                overdue_count += 1


            if 0 <= days_remaining <= 7:

                hours_due_soon += (
                    assignment["hours"]
                )


        average_hours = (
            total_hours / len(assignments)
        )


        if total_hours >= 20:

            workload = "HEAVY"

        elif total_hours >= 10:

            workload = "MODERATE"

        else:

            workload = "LIGHT"


        print(
            "\nTotal Assignments:",
            len(assignments)
        )

        print(
            "Total Estimated Hours:",
            round(total_hours, 2)
        )

        print(
            "Average Hours per Assignment:",
            round(average_hours, 2)
        )

        print(
            "High Priority:",
            high_priority
        )

        print(
            "Medium Priority:",
            medium_priority
        )

        print(
            "Low Priority:",
            low_priority
        )

        print(
            "Overdue Assignments:",
            overdue_count
        )

        print(
            "Hours Due Within 7 Days:",
            round(hours_due_soon, 2)
        )

        print(
            "Overall Workload:",
            workload
        )


    # =================================================
    # 6. UPDATE ASSIGNMENT STATUS
    # =================================================

    elif choice == "6":

        print(
            "\n========== UPDATE ASSIGNMENT STATUS =========="
        )


        if len(assignments) == 0:

            print(
                "No assignments available."
            )

            continue


        for i, assignment in enumerate(
            assignments,
            start=1
        ):

            print(
                f"{i}. "
                f"{assignment['subject']} - "
                f"{assignment['name']} "
                f"[{assignment['status']}]"
            )


        try:

            assignment_number = int(
                input(
                    "\nEnter assignment number: "
                )
            )

        except ValueError:

            print(
                "Please enter a valid number."
            )

            continue


        if (
            assignment_number < 1
            or assignment_number > len(assignments)
        ):

            print(
                "Invalid assignment number."
            )

            continue


        selected_assignment = assignments[
            assignment_number - 1
        ]


        print(
            "\nSelect new status:"
        )

        print("1. Pending")
        print("2. In Progress")
        print("3. Completed")


        status_choice = input(
            "Enter your choice: "
        )


        if status_choice == "1":

            selected_assignment["status"] = (
                "Pending"
            )

        elif status_choice == "2":

            selected_assignment["status"] = (
                "In Progress"
            )

        elif status_choice == "3":

            selected_assignment["status"] = (
                "Completed"
            )

        else:

            print(
                "Invalid status choice."
            )

            continue


        save_assignments(assignments)


        print(
            "\nAssignment status updated successfully!"
        )

        print(
            "New Status:",
            selected_assignment["status"]
        )


    # =================================================
    # 7. STUDENT DASHBOARD
    # =================================================

    elif choice == "7":

        print(
            "\n========== STUDENT DASHBOARD =========="
        )


        if len(assignments) == 0:

            print(
                "No assignments available."
            )

            continue


        total_assignments = len(assignments)

        completed = 0
        in_progress = 0
        pending = 0

        overdue = 0
        due_soon = 0

        high_priority = 0
        medium_priority = 0
        low_priority = 0

        total_hours = 0


        for assignment in assignments:

            # STATUS COUNT

            if assignment["status"] == "Completed":

                completed += 1

            elif assignment["status"] == "In Progress":

                in_progress += 1

            else:

                pending += 1


            # DEADLINE INFORMATION

            days_remaining = (
                calculate_days_remaining(
                    assignment["deadline"]
                )
            )


            if days_remaining < 0:

                overdue += 1

            elif days_remaining <= 3:

                due_soon += 1


            # PRIORITY INFORMATION

            score = calculate_priority(
                assignment
            )

            level = get_priority_level(
                score
            )


            if level == "HIGH":

                high_priority += 1

            elif level == "MEDIUM":

                medium_priority += 1

            else:

                low_priority += 1


            # TOTAL HOURS

            total_hours += assignment["hours"]


        # DISPLAY DASHBOARD

        print(
            "\n----- Assignment Summary -----"
        )

        print(
            "Total Assignments:",
            total_assignments
        )

        print(
            "Completed:",
            completed
        )

        print(
            "In Progress:",
            in_progress
        )

        print(
            "Pending:",
            pending
        )


        print(
            "\n----- Deadline Summary -----"
        )

        print(
            "Overdue:",
            overdue
        )

        print(
            "Due Within 3 Days:",
            due_soon
        )


        print(
            "\n----- Priority Summary -----"
        )

        print(
            "High Priority:",
            high_priority
        )

        print(
            "Medium Priority:",
            medium_priority
        )

        print(
            "Low Priority:",
            low_priority
        )


        print(
            "\n----- Workload Summary -----"
        )

        print(
            "Total Estimated Hours:",
            round(total_hours, 2)
        )


        if total_hours >= 20:

            workload = "HEAVY"

        elif total_hours >= 10:

            workload = "MODERATE"

        else:

            workload = "LIGHT"


        print(
            "Overall Workload:",
            workload
        )


    # =================================================
    # 8. EXIT
    # =================================================

    elif choice == "8":

        save_assignments(assignments)

        print(
            "\nData saved successfully."
        )

        print(
            "Thank you for using the system!"
        )

        break


    # =================================================
    # INVALID MENU CHOICE
    # =================================================

    else:

        print(
            "\nInvalid choice."
            " Please enter a number from 1 to 8."
        )