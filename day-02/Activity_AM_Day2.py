
def amount_due(facility_code, hours):

    if facility_code == "squa":
        rate = 13.00

    elif facility_code == "swim":
        rate = 12.00

    elif facility_code == "gym":
        rate = 11.00

    elif facility_code == "wei":
        rate = 8.00

    amount = rate * hours

    return amount



def final_amount_due(amount):

    final_amount = amount * 1.14

    return final_amount


def display(name, final_amount):

    print("\n----- PAYMENT DETAILS -----")
    print("Customer name:", name)
    print(f"Amount payable: R{final_amount:.2f}")


# Function 4: Process payment
def process_payment():

    name = input("Enter customer name: ")

    facility_code = input("Enter facility code: ").lower()

    hours = float(input("Enter number of hours: "))

    amount = amount_due(facility_code, hours)

    total = final_amount_due(amount)

    display(name, total)


# Start the program
process_payment()
