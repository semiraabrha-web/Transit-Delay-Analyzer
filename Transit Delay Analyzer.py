# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 23:39:05 2025

@author: semir
"""

"""
Transit Delay Analyzer

I made this program to check if buses or trains arrive on time. 
It can use built-in trips, read trips from a file, or let the user type trips manually. 
The program calculates how many minutes each trip is early or late, then tells 
if it’s Early, On-time, Minor Delay, or Major Delay. 

This project also helped me practice basic Python skills like,
using loops and if statements,writing functions, working with lists
and tuples, reading from and writing to files, converting times 
from HH:MM to minutes
"""

import os  # For saving output report to a file in the same folder

# -----------------------------
# Decide if a trip is early, on time, or late
# -----------------------------
def classify_delay(minutes_diff):
    """
    Decide the status of a trip based on the difference in minutes.
    """
    if minutes_diff < -2:           # If more than 2 minutes early
        return "Early"
    elif -2 <= minutes_diff <= 2:   # Within ±2 minutes considered on-time
        return "On-time"
    elif minutes_diff <= 9:         # Delayed 3–9 minutes
        return "Minor Delay"
    else:                           # Delayed 10 minutes or more
        return "Major Delay"

# -----------------------------
# Convert HH:MM string to total minutes
# -----------------------------
def time_to_minutes(time_str):
    """
    Convert time string "HH:MM" to total minutes since midnight.
    """
    hours, minutes = map(int, time_str.split(":"))  # Split hours and minutes and convert to int
    total_minutes = hours * 60 + minutes           # Total minutes = hours * 60 + minutes
    return total_minutes                            # Return the total minutes

# -----------------------------
# Display trips and their delay status and save to file
# -----------------------------
def display_delays(trip_list, filename="transit_report.txt"):
    """
    Print and save a table showing scheduled time, actual time, delay, and status.
    trip_list: list of tuples (scheduled, actual)
    filename: name of file to save output
    """
    # Full path for saving file in same folder as script
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    # Open file for writing (overwrite each run)
    with open(file_path, "w") as f:
        # Header for the report
        header = "\n--- Bus Arrival Status Report ---"
        f.write(header + "\n")
        f.write(f"{'Scheduled':>10} {'Actual':>10} {'Delay(min)':>12} {'Status':>14}\n")
        f.write("=" * 50 + "\n")

        # Print header to console as well
        print(header)
        print(f"{'Scheduled':>10} {'Actual':>10} {'Delay(min)':>12} {'Status':>14}")
        print("=" * 50)

        # Loop through all trips
        for scheduled, actual in trip_list:
            diff = time_to_minutes(actual) - time_to_minutes(scheduled)  # Calculate delay in minutes
            status = classify_delay(diff)                                # Get status based on delay
            line = f"{scheduled:>10} {actual:>10} {diff:>12} {status:>14}"
            print(line)      # Print each row to console
            f.write(line + "\n")  # Write each row to file

        # End of table
        print("=" * 50 + "\n")
        f.write("=" * 50 + "\n")

    print(f"Report saved to {file_path}\n")  # Notify user where file is saved

# -----------------------------
# Create a sample file if it doesn't exist
# -----------------------------
def create_sample_file():
    """
    Create 'schedules.txt' with example trips if it doesn't exist.
    """
    sample_data = """07:59 07:54
08:05 08:09
08:14 08:16
08:40 08:40
08:50 09:05"""
    try:
        with open("schedules.txt", "x") as f:  # 'x' mode creates file only if it doesn't exist
            f.write(sample_data)
        print("Sample file 'schedules.txt' created!\n")
    except FileExistsError:
        pass  # File already exists, do nothing
        
# This function counts how many trips are on time in a route
# I use it to compare different bus routes later
def ontime_count(trip_list):
    count = 0

    for sched, actual in trip_list:
        diff = time_to_minutes(actual) - time_to_minutes(sched)

        # check if trip is on time
        if classify_delay(diff) == "On-time":
            count += 1

    return count

# -----------------------------
# Main program loop
# -----------------------------
def main():
    print("Welcome to the Transit Arrival Analyzer!\n")
    create_sample_file()  # Ensure sample file exists

    # Default built-in trips
    default_trips = [("08:00", "07:58"), ("08:15", "08:16"),
                     ("08:30", "08:37"), ("08:45", "08:45"),
                     ("09:00", "09:12")]


    # different bus routes to compare which one is better

    route_A = [("08:00", "08:01"), ("08:15", "08:14"), ("08:30", "08:32")]
    route_B = [("08:00", "08:10"), ("08:15", "08:20"), ("08:30", "08:40")]
    route_C = [("08:00", "07:59"), ("08:15", "08:16"), ("08:30", "08:29")]

    # putting all routes together so I can loop through them easily
    built_in_routes = {
        "Route A": route_A,
        "Route B": route_B,
        "Route C": route_C
    }
    user_routes={}
    
    while True:
        # Menu for user
        choice = input(
            "Pick an option:\n"
            "  'list'  - see default trips\n"
            "  'file'  - load trips from a file\n"
            "  'input' - type your own trips\n"
            "  'route' - find best bus route\n"
            "  'quit'  - exit program\n"
            "Your choice: "
        ).strip().lower()

        if choice == "quit":  # Exit program
            break
        elif choice == "list":
            display_delays(default_trips)  # Show built-in trips
        elif choice == "file":  # Load trips from a file
            filename = input("Enter filename (like schedules.txt): ").strip()
            if not filename.endswith(".txt"):  # Ensure .txt extension
                filename += ".txt"
            try:
                trips_from_file = []
                with open(filename, "r") as f:
                    for line in f:
                        times = line.strip().split()  # Split scheduled and actual times
                        if len(times) == 2:
                            trips_from_file.append((times[0], times[1]))
                display_delays(trips_from_file)
            except FileNotFoundError:
                print("Oops! File not found.\n")
                
        elif choice == "input":  # Manual input (one or many trips)
        # Allow user to enter one or multiple trips in a single line
            print("\nEnter trips (you can enter 1 trip or many trips)")
            print("Format: 08:00 08:05, 08:10 08:15")

            line = input("Trips: ")

            user_trips = []

            trips = line.split(",") # Split multiple trips

            for t in trips:
                times = t.strip().split() # Split each trip into scheduled and actual time

                if len(times) != 2:
                    print("Wrong format:", t)
                    continue

                sched = times[0]
                actual = times[1]

                try: # Calculate difference in minutes between scheduled and actual time
                    diff = time_to_minutes(actual) - time_to_minutes(sched)
                    print("Delay:", diff, "minutes ->", classify_delay(diff))

                    user_trips.append((sched, actual))

                except ValueError:
                    print("Invalid time format (use HH:MM):", t)
                    # Handles invalid time format like wrong HH:MM input
                    
            # If at least one valid trip exists, display full report
            if user_trips:
                display_delays(user_trips)
                
        # this part compares all routes and finds which one is best
        # based on how many trips are on time

        elif choice == "route":

            print("\nChecking which bus route is best...\n")

            # ask the user if they want to add their own route
            add_route = input("Do you want to add your own route? (yes/no): ").strip().lower()

            # if user says yes, let them type multiple routes
            if add_route == "yes":

                print("\nEnter your routes one by one")
                print("Format: RouteA 08:00 08:05, 08:10 08:15")
                print("Type STOP when you are done\n")
                
                while True:
                    
                    line = input("Route: ").strip()
                    
                    # stop condition
                    if line.upper() == "STOP":
                        break

                    # split route name and trips
                    parts = line.split(" ", 1)

                    
                    # check if input format is correct
                    if len(parts) != 2:
                        print("Wrong format. Use: RouteName 08:00 08:05, 08:10 08:15")
                        continue
                    
                    route_name = " ".join(parts[0].replace("Route", "Route ").split())
                    trips_part = parts[1]

                    user_route = []

                    # split trips by commas
                    trips = trips_part.split(",")

                    # go through each trip
                    for t in trips:

                        # split scheduled and actual time
                        times = t.strip().split()
                        
                        if len(times) != 2:
                            print("Wrong format:", t)
                            continue

                        sched = times[0]
                        actual = times[1]

                        try:

                            # calculate delay difference
                            diff = time_to_minutes(actual) - time_to_minutes(sched)
                            # add trip into user's route
                            user_route.append((sched, actual))
                        
                            
                            print("Trip:", sched, actual, "->", classify_delay(diff))
                       

                        except ValueError:
                            # handles wrong time input
                            print("Invalid time format:", t)

                    # store route into dictionary
                    user_routes[route_name] = user_route
            
            #keep track of best route
            best_route = ""
            best_count = -1

            print("\n--- Route Results ---")

            # loop through every route
            for name, trips in {**built_in_routes, **user_routes}.items():

                # count how many trips are on time
                count = ontime_count(trips)

                print(name, "on-time trips:", count)

                # update best route if this route is better
                if count > best_count:

                    best_count = count
                    best_route = name

            # print final best route
            print("\nBest route today is:", best_route)
            print("It had", best_count, "on-time trips\n")
        else:
            # Handles wrong menu input
            print("Invalid input. Please choose: list, file, input, route, or quit.\n")

    print("Thanks for using the Transit Arrival Analyzer. Bye!\n")  # Exit message

# Run the program automatically
main()
