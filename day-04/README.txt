STUDENT ATTENDANCE ANALYSIS ASSIGNMENT

Files in this starter folder:
- attendance_analysis.py: commented Python solution
- README.txt: instructions and assumptions
- Screenshots/: add your Thonny screenshots here

BEFORE SUBMISSION:
1. Put the supplied attendance.json file in this same folder.
2. Run attendance_analysis.py in Thonny.
3. The program creates attendance_report.txt and invalid_records.log.
4. Add those generated files to this folder.
5. Add screenshots showing successful execution and tests to Screenshots/.
6. Re-create the ZIP with all required files.

SUPPORTED JSON STRUCTURES

Option A - list of student records:
[
  {
    "ID": "ST001",
    "name": "Example Student",
    "sessions": {"total": 20, "attended": 17},
    "late_submissions": 1
  }
]

Option B - an object containing a students list:
{
  "students": [
    {
      "ID": "ST001",
      "name": "Example Student",
      "sessions_total": 20,
      "sessions_attended": 17,
      "late_submissions": 1
    }
  ]
}

RISK RULES USED (ASSUMPTIONS - confirm with lecturer):
- CRITICAL: attendance below 60% OR late submissions 5 or more.
- SUPPORT: attendance below 75% OR late submissions 3 or more.
- SATISFACTORY: all other valid students.

The assignment screenshot does not state the numerical risk thresholds or
the exact JSON structure. The program makes these assumptions explicit.
Change the constants near the top of the Python file if your lecturer
provides different thresholds.

The actual attendance.json was not supplied with the screenshot. Therefore,
the final report, error log, real 250-record totals and screenshots must be
generated after adding the supplied dataset and running the program.
