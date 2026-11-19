
# Race Qualifiers Program

athletes = []
times = []
qualifiers = 0

print("===== 5 KM RACE QUALIFIERS =====")

while True:

    name = input("\nEnter athlete name (x to stop): ")

    if name.lower() == "x":
        break

    time = input("Enter race time (mm:ss): ")

    # Validate the time
    parts = time.split(":")

    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        print("Invalid time! Enter time in mm:ss format.")
        continue

    minutes = int(parts[0])
    seconds = int(parts[1])

    if seconds < 0 or seconds > 59:
        print("Invalid time! Seconds must be between 00 and 59.")
        continue

    # Convert time into seconds
    total_seconds = minutes * 60 + seconds

    # Store athlete details
    athletes.append(name)
    times.append(total_seconds)

    # Check if athlete qualified
    if total_seconds <= 25 * 60:
        qualifiers = qualifiers + 1


# Find the winner
if len(athletes) == 0:

    print("\nNo athletes were entered.")

else:

    lowest_time = times[0]
    winner = athletes[0]

    for i in range(len(times)):

        if times[i] < lowest_time:

            lowest_time = times[i]
            winner = athletes[i]

    # Convert winner's time back to minutes and seconds
    win_minutes = lowest_time // 60
    win_seconds = lowest_time % 60

    print("\n========== RACE RESULTS ==========")

    print("Winner:", winner,
          "({}:{:02d})".format(win_minutes, win_seconds))

    print("Qualified:", qualifiers, "of", len(athletes))
