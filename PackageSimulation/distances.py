from csv_reader import *

# Runs the data import functions contained within the "csv_reader.py" script.
# Space-time complexity is O(N)
distance_data = distance_data_import("data/distance_data.csv")
distance_names = distance_name_import("data/distance_names.csv")
package_data = package_import("data/package_data.csv")


# Fetches the distance between two locations from the distance_data matrix.
# Space-time complexity is O(1)
def return_distance(row, col):
    distance = distance_data[row][col]
    if distance == 'E':
        distance = distance_data[col][row]
    return float(distance)


# Math function to return the time spent travelling in minutes from miles travelled,
# assuming the trucks travel at an average of 18 miles per hour.
# Space-time complexity is O(1)
def return_minutes(miles):
    minutes = (miles/18) * 60
    return minutes


# Function that translates an amount of minutes into
# a timestamp string of format "HH:MM AM" or "HH:MM PM."
# Space-time complexity is O(1)
def return_timestamp(minutes):
    afternoon = " AM"
    if minutes > 720:
        afternoon = " PM"
    hours, minutes = divmod(minutes, 60)
    timestamp = "%02d:%02d" % (hours, minutes) + afternoon
    return timestamp


# Function that parses a timestamp string of format "HH:MM AM" or "HH:MM PM"
# to return an amount of minutes for calculation purposes.
# Space-time complexity is O(1)
def return_minutes_from_timestamp(timestamp):
    afternoon = str(timestamp[6]) + str(timestamp[7])
    if int(timestamp[0]) == 0:
        hours = int(timestamp[1])
        if int(timestamp[3]) == 0:
            minutes = int(timestamp[4])
        else:
            minutes = (int(timestamp[3]) * 10) + int(timestamp[4])
    else:
        hours = (int(timestamp[0]) * 10) + int(timestamp[1])
        if int(timestamp[3]) == 0:
            minutes = int(timestamp[4])
        else:
            minutes = (int(timestamp[3]) * 10) + int(timestamp[4])
    return_total = float((hours * 60) + minutes)
    if afternoon == "PM":
        return_total = return_total + 720.0
    return float(return_total)


# Function that updates the package_data hashmap with correct address information,
# in the case of error.
# Space-time complexity is O(N)
def correct_address(package_id, correction):
    package = package_data.lookup_data(package_id)
    for i in range(0, 3):
        package[i] = correction[i]
    package[6] = str(package[6]) + ": Corrected."
    package_data.insert_data(package_id, package)


# This class represents the delivery trucks, and contains the core algorithm and various related functions.
# Space-time complexity is O(N^3) due to return_address_index.
class WGUPSTruck:
    def __init__(self, packages, truck_number, miles=0.0):
        self.miles_travelled = miles
        self.loaded_packages = packages
        self.address_indexes = []
        self.package_dict = {}
        self.truck_number = truck_number
        self.return_address_index(packages)

    # This function adds an amount of distance to the truck objects current miles travelled.
    # Space-time complexity is O(1)
    def add_distance(self, distance):
        self.miles_travelled = float(self.miles_travelled) + float(distance)

    # This function returns the time that a package is delivered, by adding the current miles
    # travelled in minutes to the amount of minutes at the start of the day (480 minutes for 8:00 AM).
    # Space-time complexity is O(1)
    def delivery_time(self):
        current_time = 480.0 + return_minutes(self.miles_travelled)
        return current_time

    # This function takes a list of loaded package IDs and returns a list of location indexes
    # the truck needs to visit while populating an internal dictionary that links the two.
    # Runs once per instantiation of WGUPSTruck object.
    # Space-time complexity is O(N^3)
    def return_address_index(self, package_list):
        address_index_list = []

        for i in package_list:
            for row in range(0, len(distance_data)):
                names_hash_entry = distance_names.lookup_data(int(row))
                package_data_entry = package_data.lookup_data(int(i))
                if names_hash_entry[1] == package_data_entry[0]:
                    address_index_list.append(int(row))
                    self.package_dict[int(i)] = int(row)
            package_update = package_data.lookup_data(int(i))
            package_update[9] = self.delivery_time()
            package_update[7] = self.truck_number
        self.address_indexes = address_index_list

    # This function retrieves the IDs of any packages that need to be delivered at the current location
    # from an internal dictionary, then updates the package_data hashmap with the time of delivery for
    # those packages. The current location is then removed from the internal list of addresses to visit.
    # Space-time complexity is O(N^2)
    def deliver_package(self, current_location):
        key_list = [key for (key, value) in self.package_dict.items() if value == current_location]
        for value in key_list:
            package_update = package_data.lookup_data(int(value))
            package_timestamp = str(return_timestamp(self.delivery_time()))
            package_update[8] = self.delivery_time()
            package_update[10] = "Delivered at: " + str(package_timestamp) + " by Truck #" + str(package_update[7])
            package_data.insert_data(int(value), package_update)
            self.address_indexes.remove(int(current_location))

    # This is the core "greedy" algorithm of the program that searches for the shortest distance between the current
    # location and all locations the truck needs to visit. The algorithm runs "while" the list of locations to visit
    # is not empty, initializing tracker variables to record the shortest distance and its location. After cycling
    # through all locations in the address list and finding the shortest path, the distance of that path is added to
    # the trucks current miles travelled. The deliver_package function is then run on that location to update the
    # package data and the address list. When all locations are visited and all packages are delivered the truck makes
    # a return trip to the hub, adding the miles travelled before the algorithm ends.
    # Space-time complexity is O(N^3)
    def greedy_driver(self, starting_location):
        current_location = int(starting_location)

        while len(self.address_indexes) != 0:
            shortest_distance = 50.0
            new_location = 0

            for element in self.address_indexes:
                if return_distance(current_location, element) < shortest_distance:
                    shortest_distance = return_distance(current_location, element)
                    new_location = element

            current_location = new_location
            self.add_distance(float(shortest_distance))
            self.deliver_package(new_location)

        return_trip = return_distance(current_location, starting_location)
        self.add_distance(float(return_trip))
