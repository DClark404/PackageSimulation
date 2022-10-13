import csv
from hashmap import *


# Parses package data within a csv file while adding other relevant tracking variables,
# then inserts all data into an instance of the hashmap data structure.
# Space-time complexity is O(N)
def package_import(package_data_file):
    with open(package_data_file) as open_package_data:
        read_csv_package = csv.reader(open_package_data, delimiter=",")

        package_hash = HashMap()
        for row in read_csv_package:
            key = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            special_notes = row[7]
            truck_number = 0
            delivery_time = 0.0
            time_loaded = 0.0
            delivery_timestamp = "at hub"

            data = [address, city, state, zip_code, deadline, weight,
                    special_notes, truck_number, delivery_time, time_loaded, delivery_timestamp]
            package_hash.insert_data(int(key), data)

        return package_hash


# Parses location name data within a csv file before inserting it into an instance of
# the hashmap data structure.
# Space-time complexity is O(N)
def distance_name_import(distance_name_file):
    with open(distance_name_file) as open_name_data:
        read_csv_name = csv.reader(open_name_data, delimiter=",")

        name_hash = HashMap()
        for row in read_csv_name:
            key = row[0]
            name = row[1]
            address = row[2]

            data = [name, address]
            name_hash.insert_data(int(key), data)

    return name_hash


# Retrieves the distance data from a csv file, storing each row of the data as a list within a list,
# effectively creating a matrix of the distance data for simple access to row/column values.
# Space-time complexity is O(N)
def distance_data_import(distance_data_file):
    with open(distance_data_file) as open_distance_data:
        read_csv_distance = csv.reader(open_distance_data, delimiter=",")

        distance_data_matrix = []
        for row in read_csv_distance:
            distance_data_matrix.append(row)

    return distance_data_matrix
