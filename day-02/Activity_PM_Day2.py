
import random


# 1. Generate random machine usage time
def generate_minutes():
    minutes = random.randint(30, 180)
    return minutes


# 2. Calculate amount before VAT
def calc_amount(machine_type, minutes):

    hours = minutes / 60

    if machine_type == "A":
        initial_cost = 50.00
        hourly_rate = 30.00

    elif machine_type == "B":
        initial_cost = 62.50
        hourly_rate = 36.25

    elif machine_type == "C":
        initial_cost = 74.87
        hourly_rate = 40.50

    amount = initial_cost + (hourly_rate * hours)

    return amount


# 3. Calculate VAT and total payable
def calc_total_amount(amount):

    vat = amount * 0.14
    total = amount + vat

    return vat, total


# 4. Display daily summary
def display_summary(payments):

    number_customers = len(payments)

    total_payments = sum(payments)

    average_payment = total_payments / number_customers

    highest_payment = max(payments)

    lowest_payment = min(payments)

    print("\n========== DAILY SUMMARY ==========")

    print("Number of customers:", number_customers)

    print("Combined payments: R{:.2f}".format(total_payments))

    print("Average payment: R{:.2f}".format(average_payment))

    print("Highest payment: R{:.2f}".format(highest_payment))

    print("Lowest payment: R{:.2f}".format(lowest_payment))


# 5. Process customer payments
def process_payments():

    payments = []

    customers = int(input("Enter number of customers: "))

    for count in range(customers):

        print("\nCustomer", count + 1)

        name = input("Enter customer name: ")

        machine_type = input("Enter machine type (A, B or C): ").upper()

        minutes = generate_minutes()

        amount = calc_amount(machine_type, minutes)

        vat, total = calc_total_amount(amount)

        payments.append(total)

        print("\n========== CUSTOMER INVOICE ==========")

        print("Customer name:", name)

        print("Machine type:", machine_type)

        print("Minutes used:", minutes)

        print("Amount before VAT: R{:.2f}".format(amount))

        print("VAT amount: R{:.2f}".format(vat))

        print("Total payable: R{:.2f}".format(total))

    display_summary(payments)


# Start the program
process_payments()
