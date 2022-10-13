# David Clark, Student ID: 000953486
from distances import *

# This section of the program runs the simulation of the trucks delivering their packages.
# The first two trucks are initialized with a pre-sorted package list, then their routes are processed.
# The third truck is then initialized with the remaining packages and leaves when the second truck returns,
# receiving the second trucks mileage as an argument for the purpose of keeping time.
# Space-time complexity is O(N^3)
first_truck = WGUPSTruck([14, 16, 20, 15, 13, 19, 29, 30, 31, 34, 40, 7, 8, 21, 39, 1], 1)
second_truck = WGUPSTruck([3, 18, 36, 38, 37, 35, 27, 26], 2)
first_truck.greedy_driver(0)
second_truck.greedy_driver(0)

# At 10:20 AM, the incorrect address on package #9 is corrected.
correct_address(9, ["410 S State St", "Salt Lake City", "UT", "84111"])

third_truck = WGUPSTruck([25, 28, 32, 6, 9, 5, 33, 2, 23, 11, 22, 4, 10, 12, 17, 24], 3, second_truck.miles_travelled)
third_truck.greedy_driver(0)


# This function simply prints miles travelled of individual truck objects, then the sum.
# total miles is the sum of the first and third truck, as the mileage of the second truck is
# passed as an argument during declaration of the third truck.
# Space-time complexity is O(1)
def report_total_mileage():
    total_miles = int(first_truck.miles_travelled + third_truck.miles_travelled)
    print(" ")
    print("Truck #1 has travelled " + str(int(first_truck.miles_travelled)) + " Miles.")
    print("Truck #2 has travelled " + str(int(second_truck.miles_travelled)) + " Miles.")
    print("Truck #3 has travelled " + str(int(third_truck.miles_travelled) - int(second_truck.miles_travelled)) +
          " Miles.")
    print("All packages delivered within " + str(total_miles) + " Miles.")


# function that prints the data and final delivery time of every package.
# Space-time complexity is O(N^2)
def print_final_package_status():
    for i in range(1, (package_data.return_size() + 1)):
        package_list = package_data.lookup_data(i)
        print("[" + str(i) + "] " + str(package_list[0:6]) + " " + str(package_list[10]) + ".")


# Function that prints a list of all stored package data at a given time, along
# with their delivery status.
# Space-time complexity is O(N^2)
def list_all_package_status(time):
    print(" ")
    print("Status of all packages at " + str(time) + ":")
    for i in range(1, (package_data.return_size() + 1)):
        list_single_package_status(time, i)


# Function that prints the delivery status of a single package at a given time.
# Space-time complexity is O(N)
def list_single_package_status(time, package_id):
    format_correct = time
    if len(format_correct) == 7:
        format_correct = str("0" + format_correct)
    time_search = return_minutes_from_timestamp(format_correct)
    package = package_data.lookup_data(package_id)
    if time_search > package[8]:
        print("[" + str(package_id) + "] " + str(package[0:6]) + " " + str(package[10]) + ".")
    elif time_search < package[9]:
        print("[" + str(package_id) + "] " + str(package[0:6]) + " Status: At Hub.")
    else:
        print("[" + str(package_id) + "] " + str(package[0:6]) + " Status: En route, on truck #"
              + str(package[7]) + ".")


# Space-time complexity is O(1)
def print_menu_options():
    print("Select from the following:")
    print("    1 = List final delivery status of all packages.")
    print("    2 = Show status of a single package at any time.")
    print("    3 = List status of all packages at any time.")
    print("    4 = Reports total miles travelled.")
    print("    5 = Exits the program.")


# This is the user interface section, where the user can view the status and info of any package
# at any time, and total mileage travelled by all trucks.
# Space-time complexity is O(N^3)
print(" ")
print("Welcome to the WGU package tracking system!")
ui_start = None

while ui_start != '5':
    print(" ")
    print_menu_options()
    ui_start = input("Enter your choice: ")

    if ui_start == '1':
        print(" ")
        print("Listing final delivery status of all packages:")
        print_final_package_status()

    elif ui_start == '2':
        package_to_search = input("Enter package ID number: ")
        print("Note: Time must be in format 'HH:MM AM' or 'HH:MM PM'.")
        print("This includes the space, leading zeros are not necessary.")
        time_to_search = input("    Enter time: ")
        print(" ")
        print("Returning status of Package #" + package_to_search + " at " + time_to_search + ":")
        list_single_package_status(time_to_search, int(package_to_search))

    elif ui_start == '3':
        print("Note: Time must be in format 'HH:MM AM' or 'HH:MM PM'.")
        print("This includes the space, leading zeros are not necessary.")
        time_to_search = input("    Enter time: ")
        list_all_package_status(time_to_search)

    elif ui_start == '4':
        report_total_mileage()
