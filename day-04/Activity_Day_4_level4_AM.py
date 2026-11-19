file = open("names.txt", "w")

file.write("Rofhiwa, Peter, John, Mary, David  \n")

file.close()

print("Five names saved successfully!")

print("\nLEARNER NAMES")

try:
    file = open("names.txt", "r")

    for line in file:
        name = line.strip()
        print(name.upper())

    file.close()

except FileNotFoundError:
    print("Error: File does not exist!")

file = open("names.txt", "a")

file.write("Williams\n")

file.close()

print("\nSixth name added successfully!")

try:
    file = open("names.txt", "r")

    lines = file.readlines()

    print("Total number of names:", len(lines))

    file.close()

except FileNotFoundError:
    print("Error: Cannot count names. File not found!")


