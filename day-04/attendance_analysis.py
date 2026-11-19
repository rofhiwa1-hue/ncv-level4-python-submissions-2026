# ============================================================
# STUDENT ATTENDANCE ANALYSIS SYSTEM
# Analyse 250 student attendance records from attendance.json
# ============================================================

import json

INPUT_FILE = "attendance.json"
REPORT_FILE = "attendance_report.txt"
ERROR_FILE = "invalid_records.log"

# RISK RULES (ASSUMPTIONS: change if your lecturer gives other limits)
CRITICAL_ATTENDANCE = 60       # Below 60% = CRITICAL
SUPPORT_ATTENDANCE = 75        # Below 75% = SUPPORT
CRITICAL_LATE_SUBMISSIONS = 5  # 5 or more = CRITICAL
SUPPORT_LATE_SUBMISSIONS = 3   # 3 or more = SUPPORT

students = []
invalid_records = []


# ------------------------------------------------------------
# SECTION 1: LOAD JSON FILE (STEP 1)
# ------------------------------------------------------------
def load_json_file():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        print("JSON file loaded successfully.")
        return data

    except FileNotFoundError:
        print("ERROR: attendance.json was not found.")
    except json.JSONDecodeError as error:
        print("ERROR: Invalid JSON format:", error)
    except OSError as error:
        print("ERROR reading file:", error)

    return None


# ------------------------------------------------------------
# SECTION 2: READ STUDENT RECORDS (STEP 2)
# Accepts either:
#   {"students": [ ... ]}
# or a direct JSON list: [ ... ]
# ------------------------------------------------------------
def get_student_records(data):
    if isinstance(data, list):
        return data

    if isinstance(data, dict) and isinstance(data.get("students"), list):
        return data["students"]

    raise ValueError(
        'JSON must be a list of students or an object with a "students" list.'
    )


# ------------------------------------------------------------
# SECTION 3: VALIDATE RECORDS (STEP 3)
# Supports flat fields or nested sessions:
# Flat: sessions_total, sessions_attended
# Nested: "sessions": {"total": 20, "attended": 17}
# ------------------------------------------------------------
def validate_records(records):
    seen_ids = set()

    for record_number, record in enumerate(records, start=1):
        reasons = []

        if not isinstance(record, dict):
            invalid_records.append(
                "Record " + str(record_number) + " | Record is not an object"
            )
            continue

        student_id = record.get("ID", record.get("id"))
        name = record.get("name")
        late = record.get("late_submissions")

        sessions = record.get("sessions", {})
        if isinstance(sessions, dict):
            total = record.get("sessions_total", sessions.get("total"))
            attended = record.get(
                "sessions_attended", sessions.get("attended")
            )
        else:
            total = record.get("sessions_total")
            attended = record.get("sessions_attended")

        # Check required text fields
        if student_id is None or str(student_id).strip() == "":
            reasons.append("Missing student ID")

        if name is None or str(name).strip() == "":
            reasons.append("Missing student name")

        # Check duplicate ID
        clean_id = str(student_id).strip() if student_id is not None else ""
        if clean_id != "" and clean_id in seen_ids:
            reasons.append("Duplicate student ID")
        elif clean_id != "":
            seen_ids.add(clean_id)

        # Validate total sessions
        try:
            total = int(total)
            if total <= 0:
                reasons.append("Total sessions must be greater than zero")
        except (ValueError, TypeError):
            total = 0
            reasons.append("Total sessions must be a whole number")

        # Validate attended sessions
        try:
            attended = int(attended)
            if attended < 0:
                reasons.append("Attended sessions cannot be negative")
        except (ValueError, TypeError):
            attended = 0
            reasons.append("Attended sessions must be a whole number")

        if total > 0 and attended > total:
            reasons.append("Attended sessions cannot exceed total sessions")

        # Validate late submissions
        try:
            late = int(late)
            if late < 0:
                reasons.append("Late submissions cannot be negative")
        except (ValueError, TypeError):
            late = 0
            reasons.append("Late submissions must be a whole number")

        if reasons:
            invalid_records.append(
                "Record " + str(record_number) +
                " | " + "; ".join(reasons) +
                " | " + str(record)
            )
        else:
            students.append({
                "id": clean_id,
                "name": str(name).strip(),
                "sessions_total": total,
                "sessions_attended": attended,
                "late_submissions": late
            })


# ------------------------------------------------------------
# SECTION 4: CALCULATE ATTENDANCE PERCENTAGE (STEP 4)
# ------------------------------------------------------------
def calculate_attendance():
    for student in students:
        percentage = (
            student["sessions_attended"] /
            student["sessions_total"]
        ) * 100

        student["attendance_percentage"] = percentage


# ------------------------------------------------------------
# SECTION 5: APPLY RISK RULES (STEP 5)
# CRITICAL: attendance below 60% OR late submissions >= 5
# SUPPORT: attendance below 75% OR late submissions >= 3
# Otherwise: SATISFACTORY
# ------------------------------------------------------------
def apply_risk_rules():
    for student in students:
        attendance = student["attendance_percentage"]
        late = student["late_submissions"]

        if (attendance < CRITICAL_ATTENDANCE or
                late >= CRITICAL_LATE_SUBMISSIONS):
            risk = "CRITICAL"

        elif (attendance < SUPPORT_ATTENDANCE or
              late >= SUPPORT_LATE_SUBMISSIONS):
            risk = "SUPPORT"

        else:
            risk = "SATISFACTORY"

        student["risk"] = risk


# ------------------------------------------------------------
# SECTION 6: COUNT RISK GROUPS (STEP 6)
# ------------------------------------------------------------
def count_risk_groups():
    counts = {
        "CRITICAL": 0,
        "SUPPORT": 0,
        "SATISFACTORY": 0
    }

    for student in students:
        risk = student["risk"]
        counts[risk] = counts[risk] + 1

    return counts


# ------------------------------------------------------------
# SECTION 7: SAVE ATTENDANCE REPORT (STEP 7)
# ------------------------------------------------------------
def create_attendance_report(counts):
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("STUDENT ATTENDANCE ANALYSIS REPORT\n")
        file.write("=" * 55 + "\n\n")

        file.write("VALID STUDENT RECORDS\n")
        file.write("-" * 55 + "\n")
        file.write(
            "ID | Name | Attended/Total | Attendance | Late | Risk\n"
        )

        for student in students:
            file.write(
                student["id"] + " | " +
                student["name"] + " | " +
                str(student["sessions_attended"]) + "/" +
                str(student["sessions_total"]) + " | " +
                format(student["attendance_percentage"], ".2f") +
                "% | " + str(student["late_submissions"]) +
                " | " + student["risk"] + "\n"
            )

        file.write("\nRISK GROUP SUMMARY\n")
        file.write("-" * 55 + "\n")
        file.write("Critical: " + str(counts["CRITICAL"]) + "\n")
        file.write("Requires support: " + str(counts["SUPPORT"]) + "\n")
        file.write("Satisfactory: " + str(counts["SATISFACTORY"]) + "\n")
        file.write("Accepted records: " + str(len(students)) + "\n")
        file.write("Rejected records: " + str(len(invalid_records)) + "\n")

        file.write("\nSTUDENTS REQUIRING SUPPORT\n")
        file.write("-" * 55 + "\n")
        for student in students:
            if student["risk"] == "CRITICAL" or student["risk"] == "SUPPORT":
                file.write(
                    student["id"] + " | " + student["name"] +
                    " | " + format(student["attendance_percentage"], ".2f") +
                    "% | " + student["risk"] + "\n"
                )

    print("Attendance report created:", REPORT_FILE)


# ------------------------------------------------------------
# SECTION 8: SAVE INVALID-RECORD LOG
# ------------------------------------------------------------
def create_error_log():
    with open(ERROR_FILE, "w", encoding="utf-8") as file:
        file.write("INVALID STUDENT ATTENDANCE RECORDS\n")
        file.write("=" * 55 + "\n\n")

        for error in invalid_records:
            file.write(error + "\n")

        file.write("\nTotal invalid records: " + str(len(invalid_records)))

    print("Invalid-record log created:", ERROR_FILE)


# ------------------------------------------------------------
# SECTION 9: DISPLAY SUMMARY
# ------------------------------------------------------------
def display_summary(counts):
    print("\nSTUDENT ATTENDANCE ANALYSIS")
    print("=" * 40)
    print("Accepted records:", len(students))
    print("Rejected records:", len(invalid_records))
    print("Critical risk:", counts["CRITICAL"])
    print("Requires support:", counts["SUPPORT"])
    print("Satisfactory:", counts["SATISFACTORY"])
    print("Report:", REPORT_FILE)
    print("Invalid log:", ERROR_FILE)


# ------------------------------------------------------------
# SECTION 10: MAIN PROGRAM
# ------------------------------------------------------------
def main():
    print("Starting Student Attendance Analysis System...")

    data = load_json_file()
    if data is None:
        return

    try:
        records = get_student_records(data)
        validate_records(records)
        calculate_attendance()
        apply_risk_rules()
        counts = count_risk_groups()
        create_attendance_report(counts)
        create_error_log()
        display_summary(counts)
        print("\nProgram completed successfully.")

    except ValueError as error:
        print("DATA FORMAT ERROR:", error)


# START PROGRAM
if __name__ == "__main__":
    main()
