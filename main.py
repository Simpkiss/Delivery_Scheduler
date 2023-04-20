# Aaron Simpkiss ID#001473307 C950 project



import datetime
import csv
from Truck import Truck
from HashTable import HashTable
from Package import Package


# Functions to switch between strings and date times, just for simplicity
def to_printable_time(datetime_input):
    return datetime_input.strftime('%I:%M %p')


def to_workable_time(stringtime):
    return datetime.datetime.strptime(stringtime, '%I:%M %p')


# Function that formats the package info nicely and prints it
def nice_output(id_num, input_time):
    delivery_time = pack_hash.search(id_num).delivery_time
    if input_time > delivery_time:
        status_string = " was successfully delivered at "
    elif input_time > pack_hash.search(id_num).leave_time:
        status_string = " is out for delivery and is scheduled to arrive at "
    else:
        status_string = " is not yet out for delivery, but is scheduled to be delivered at "

    print("At ", to_printable_time(input_time), " package #", id_num, ", weighing ", pack_hash.search(id_num).weight,
          " kilos, destined for ", pack_hash.search(id_num).address, ", ", pack_hash.search(id_num).city, " ",
          pack_hash.search(id_num).state, ", ", pack_hash.search(id_num).zip_code, " by ",
          pack_hash.search(id_num).deadline, ",", status_string, to_printable_time(delivery_time), sep='')


# Create hash table
pack_hash = HashTable()

# Load and hash packages
file = open("CSV/Package File.csv", "r")
packages = csv.reader(file, delimiter=",")
for package in packages:
    ID = int(package[0])
    address = package[1]
    city = package[2]
    state = package[3]
    zipcode = package[4]
    deadline = package[5]
    weight = package[6]
    note = package[7]
    status = "At Hub"
    hash_package = Package(ID, address, city, state, zipcode, deadline, weight, note, status)
    pack_hash.insert(ID, hash_package)

# Load distances
file = open("CSV/Distance Table.csv", "r")
distances = list(csv.reader(file, delimiter=","))

# Load addresses
file = open("CSV/Addresses.csv", "r")
addresses = list(csv.reader(file, delimiter=","))
file.close()  # Closes files


# Finds the index of a named address on the address list
def address_index(address_string):
    for row in addresses:
        if address_string in row[1]:
            return int(row[0]) - 1


# Sorts and delivers packages, weights distances to prioritize deadline packages.
# Records package leave and delivery times, calculates truck mileage with return trip and return time.
def deliver(truck):
    distance = 1000.0
    start = 0
    next_package = 0
    traveled = 0.0
    while len(truck.packages) > 0:
        for pack_ID in truck.packages:
            actual_distance = float(distances[start][address_index(pack_hash.search(pack_ID).address)])
            weighted_distance = actual_distance
            if pack_hash.search(pack_ID).deadline == "EOD":
                weighted_distance = actual_distance * 5
            if weighted_distance < distance:
                distance = weighted_distance
                travel_distance = actual_distance
                next_package = pack_ID
        # print("Next stop is ", distance, " miles away, now delivering package number ", next_package)
        traveled = traveled + travel_distance
        pack_hash.search(next_package).leave_time = truck.depart_time
        pack_hash.search(next_package).delivery_time = truck.depart_time + datetime.timedelta(minutes=(traveled / 0.3))
        truck.packages.remove(next_package)
        start = address_index(pack_hash.search(next_package).address)
        distance = 1000.0
    truck.mileage = traveled + float(distances[start][0])
    truck.return_time = (truck.depart_time + datetime.timedelta(minutes=(truck.mileage / 0.3)))


# Manually load the 3 trucks and set their departure times. Truck 3 held until package 9's address is updated
truck1 = Truck([15, 14, 19, 16, 13, 20, 34, 21, 39, 27, 35, 29, 7, 1, 40, 30], to_workable_time('8:00 AM'))
truck2 = Truck([18, 36, 3, 38, 37, 5, 10, 8, 25, 26, 32, 31, 17, 6, 28, 22], to_workable_time('9:05 AM'))
truck3 = Truck([9, 2, 33, 11, 12, 4, 23, 24], to_workable_time('10:30 AM'))

# Deliver the trucks
deliver(truck1)
deliver(truck2)
deliver(truck3)

# Header information
print("All packages delivered and trucks returned at ", to_printable_time(truck3.return_time), ", with a total of ",
      truck1.mileage + truck2.mileage + truck3.mileage, " miles.")

# Input prompt
entered_value = input("Input a time to check package status (hh:mm am/pm) or type 'quit' to exit. ")
while entered_value.lower() != "quit":
    if entered_value.lower() == "eod":
        entered_value = to_printable_time(truck3.return_time)
    try:
        entered_time = to_workable_time(entered_value)     # Input converted to functional date time
        # Selection prompt
        select_mode = input("Enter a package ID number or 'all' to see information for those packages. ")
        if select_mode.lower() == 'all':                    # Print all method
            for x in pack_hash.list():
                nice_output(x, entered_time)
        elif int(select_mode) in pack_hash.list():  # Print select method
            nice_output(int(select_mode), entered_time)
        else:                                       # Bad selection error
             print("There doesn't seem to be a package with that ID number. ")

    except ValueError:
        print("That wasn't what I was expecting, try it again.")
    entered_value = input("Input a time to check package status (hh:mm am/pm) or type 'quit' to exit.")