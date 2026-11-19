
# ============================================================
# COMMUNITY WATER CONSUMPTION AND BILLING MANAGEMENT SYSTEM
# Python Practical Assignment - 100 Marks
# ============================================================

# ============================================================
# SECTION 1: VARIABLES AND DATA STRUCTURES
# ============================================================

INPUT_FILE = "water_readings.txt"
REPORT_FILE = "billing_report.txt"
ERROR_FILE = "errors.log"

# Dictionary to store valid household records
households = {}

# Lists to store rejected records and error messages
rejected_records = []
error_messages = []


# ============================================================
# SECTION 2: READ THE INPUT FILE (Q1)
# ============================================================

def read_file():

    try:
        file = open(INPUT_FILE, "r")

        lines = file.readlines()

        file.close()

        print("Input file successfully opened.")
        return lines

    except FileNotFoundError:

        print("ERROR: water_readings.txt was not found.")
        return None


# ============================================================
# SECTION 3: VALIDATE AND STORE RECORDS (Q2 AND Q3)
# ============================================================

def validate_records(lines):

    seen_meters = set()

    line_number = 0

    for line in lines:

        line_number = line_number + 1

        # Ignore completely blank lines
        if line.strip() == "":
            continue

        fields = line.strip().split(",")

        reason = ""

        # Check number of fields
        if len(fields) != 5:

            reason = "Incorrect number of fields"

        else:

            meter = fields[0].strip()
            name = fields[1].strip()
            previous = fields[2].strip()
            current = fields[3].strip()
            area = fields[4].strip()

            # Check missing fields
            if (meter == "" or name == "" or
                previous == "" or current == "" or
                area == ""):

                reason = "Missing field"

            # Check duplicate meter numbers
            elif meter in seen_meters:

                reason = "Duplicate meter number"

            else:

                seen_meters.add(meter)

                # Check numeric readings
                try:

                    previous = float(previous)
                    current = float(current)

                    # Check negative readings
                    if previous < 0 or current < 0:

                        reason = "Negative meter reading"

                    # Check reversed readings
                    elif current < previous:

                        reason = "Current reading is below previous reading"

                except ValueError:

                    reason = "Non-numeric meter reading"

        # Store rejected record and reason
        if reason != "":

            rejected_records.append(line.strip())

            error_messages.append(
                "Line " + str(line_number) +
                " | " + reason +
                " | " + line.strip()
            )

        else:

            # Store valid records in dictionary
            households[meter] = {
                "name": name,
                "previous": previous,
                "current": current,
                "area": area
            }


# ============================================================
# SECTION 4: CALCULATE MONTHLY CONSUMPTION (Q4)
# ============================================================

def calculate_consumption():

    for meter in households:

        previous = households[meter]["previous"]
        current = households[meter]["current"]

        consumption = current - previous

        households[meter]["consumption"] = consumption


# ============================================================
# SECTION 5: CALCULATE PROGRESSIVE WATER BILL (Q5)
# ============================================================

def calculate_bill(consumption):

    bill = 0

    # First 6 kL are free
    if consumption <= 6:

        bill = 0

    # Consumption above 6 and up to 20 kL
    elif consumption <= 20:

        bill = (consumption - 6) * 8.50

    # Consumption above 20 kL
    else:

        bill = (14 * 8.50) + ((consumption - 20) * 12.00)

    return bill


def process_bills():

    for meter in households:

        consumption = households[meter]["consumption"]

        bill = calculate_bill(consumption)

        households[meter]["bill"] = bill


# ============================================================
# SECTION 6: CLASSIFY HOUSEHOLDS (Q6)
# ============================================================

def classify_households():

    for meter in households:

        consumption = households[meter]["consumption"]

        if consumption <= 20:

            category = "LOW"

        elif consumption <= 50:

            category = "MODERATE"

        else:

            category = "HIGH"

        households[meter]["category"] = category


# ============================================================
# SECTION 7: MANUAL TOP FIVE RANKING (Q7)
# DO NOT USE sorted(), max() OR min()
# ============================================================

def find_top_five():

    # Copy records into a list
    remaining = []

    for meter in households:

        record = {
            "meter": meter,
            "name": households[meter]["name"],
            "consumption": households[meter]["consumption"],
            "bill": households[meter]["bill"],
            "area": households[meter]["area"]
        }

        remaining.append(record)

    top_five = []

    # Manually find the five highest consumers
    for position in range(5):

        if len(remaining) == 0:
            break

        highest_index = 0

        # Compare consumption using a loop
        for index in range(1, len(remaining)):

            if (remaining[index]["consumption"] >
                remaining[highest_index]["consumption"]):

                highest_index = index

        # Move highest record to top five
        highest_record = remaining.pop(highest_index)

        top_five.append(highest_record)

    return top_five


# ============================================================
# SECTION 8: GENERATE BILLING REPORT (Q8)
# ============================================================

def create_billing_report(top_five):

    report = open(REPORT_FILE, "w")

    report.write("============================================\n")
    report.write(" COMMUNITY WATER BILLING MANAGEMENT SYSTEM\n")
    report.write("============================================\n\n")

    report.write("VALID HOUSEHOLD BILLING RECORDS\n")
    report.write("--------------------------------------------\n")

    report.write(
        "Meter | Household | Area | Usage | Category | Bill\n"
    )

    report.write("--------------------------------------------\n")

    total_consumption = 0
    total_billing = 0
    low_count = 0
    moderate_count = 0
    high_count = 0

    for meter in households:

        record = households[meter]

        usage = record["consumption"]
        bill = record["bill"]
        category = record["category"]

        report.write(
            meter + " | " +
            record["name"] + " | " +
            record["area"] + " | " +
            str(round(usage, 2)) + " kL | " +
            category + " | R" +
            format(bill, ".2f") + "\n"
        )

        total_consumption = total_consumption + usage
        total_billing = total_billing + bill

        if category == "LOW":

            low_count = low_count + 1

        elif category == "MODERATE":

            moderate_count = moderate_count + 1

        else:

            high_count = high_count + 1

    # Top five consumers
    report.write("\n\nTOP FIVE HIGHEST-CONSUMING HOUSEHOLDS\n")
    report.write("--------------------------------------------\n")

    rank = 1

    for record in top_five:

        report.write(
            str(rank) + ". " +
            record["name"] +
            " | Meter: " + record["meter"] +
            " | Area: " + record["area"] +
            " | Consumption: " +
            str(round(record["consumption"], 2)) +
            " kL | Bill: R" +
            format(record["bill"], ".2f") + "\n"
        )

        rank = rank + 1

    # Summary
    report.write("\n\nMONTHLY SUMMARY\n")
    report.write("--------------------------------------------\n")

    report.write(
        "Accepted households: " +
        str(len(households)) + "\n"
    )

    report.write(
        "Rejected records: " +
        str(len(rejected_records)) + "\n"
    )

    report.write(
        "Total consumption: " +
        str(round(total_consumption, 2)) + " kL\n"
    )

    report.write(
        "Total billing amount: R" +
        format(total_billing, ".2f") + "\n"
    )

    report.write("LOW households: " + str(low_count) + "\n")
    report.write("MODERATE households: " + str(moderate_count) + "\n")
    report.write("HIGH households: " + str(high_count) + "\n")

    report.close()

    print("Billing report created successfully.")


# ============================================================
# SECTION 9: CREATE ERROR LOG (Q8)
# ============================================================

def create_error_log():

    error_file = open(ERROR_FILE, "w")

    error_file.write("WATER BILLING SYSTEM - ERROR LOG\n")
    error_file.write("============================================\n\n")

    for error in error_messages:

        error_file.write(error + "\n")

    error_file.write("\n============================================\n")

    error_file.write(
        "Total rejected records: " +
        str(len(rejected_records)) + "\n"
    )

    error_file.close()

    print("Error log created successfully.")


# ============================================================
# SECTION 10: DISPLAY RESULTS
# ============================================================

def display_results(top_five):

    print("\n===================================")
    print(" WATER BILLING SYSTEM")
    print("===================================")

    print("Accepted records:", len(households))
    print("Rejected records:", len(rejected_records))

    print("\nTOP FIVE HIGHEST CONSUMERS")

    rank = 1

    for record in top_five:

        print(
            rank, record["name"],
            "-", record["consumption"], "kL",
            "- R", format(record["bill"], ".2f")
        )

        rank = rank + 1

    print("\nBilling report:", REPORT_FILE)
    print("Error log:", ERROR_FILE)


# ============================================================
# SECTION 11: MAIN PROGRAM
# ============================================================

def main():

    print("Starting Water Billing Management System...")

    # Read input file
    lines = read_file()

    if lines is None:

        return

    # Validate records
    validate_records(lines)

    # Calculate consumption
    calculate_consumption()

    # Calculate bills
    process_bills()

    # Classify households
    classify_households()

    # Find top five consumers
    top_five = find_top_five()

    # Generate reports
    create_billing_report(top_five)

    create_error_log()

    # Display results
    display_results(top_five)

    print("\nProgram completed successfully.")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()
