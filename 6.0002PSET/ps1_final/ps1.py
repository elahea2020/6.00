###########################
# 6.0002 Problem Set 1: Space Cows
# Name: Elaheh Ahmadi
# Collaborators: TAs :-?
# Time: +10h
# Difficult sections / topics: Dynamic programming!

from ps1_partition import get_partitions
import time
import copy

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow weight, name pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename : the name of the data file as a string

    Returns:
    a dictionary containing cow names (string) as keys, and the corresponding
    weight (int) as the value
    for ex: {'Matt': 3, 'Kaitlin': 3, 'Katy': 5}
    """
    # Open the file
    data_file = open(filename)
    # Read the file and put whatever that is in the file in data string
    data_string = data_file.read()
    # putting each line in an element of an array
    data_array = data_string.split('\n')
    # Creating an empty dictionary
    cows_dict = {}
    # Iterating over the lines in data
    for line in data_array:
        cow_data = line.split(',')
        if len(cow_data) > 1:
            cows_dict[cow_data[1]] = int(cow_data[0])
    return cows_dict


# Problem 2
def sort_cows(cows):
    """
    Sorts the input dictionary based on the values from high to low.
    Assumes input is a dictionary
    Parameters:
    cows : a dictionary of names (string), weights (int)
    Returns:
    sorted_cow_list : a list of name of the cows sorted based on their weight
    """
    sorted_cow_list = []
    # Iterates over the cows and creates a sorted list that is name of the cows sorted by their weight from high to low
    for cow in cows.keys():
        if len(sorted_cow_list) == 0:
            sorted_cow_list.append(cow)
        else:
            i = len(sorted_cow_list)-1
            cow_weight = int(cows[cow])
            while cow_weight > int(cows[sorted_cow_list[i]]) and i >= 0:
                i -= 1
            sorted_cow_list.insert(i+1, cow)
    return sorted_cow_list


def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows : a dictionary of names (string), weights (int)
    limit : weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Sorting the cows based on their weight from high to low
    sorted_cow_list = sort_cows(cows)
    trips = []
    # As long as there is cow to be moved this while works
    while len(sorted_cow_list) > 0:
        trip = []
        trip_limit = limit
        # Iterates over the remaining cows and add them to the spaceship if possible
        temp_cow_list = sorted_cow_list[:]
        for cow in temp_cow_list:
            cow_weight = int(cows[cow])
            if trip_limit - cow_weight >= 0:
                trip.append(cow)
                trip_limit -= cow_weight
                sorted_cow_list.remove(cow)
            if trip_limit == 0:
                break
        # Add the trip to the trips array
        trips.append(trip)
    return trips



# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows : a dictionary of names (string), and weights (int)
    limit : weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    valid_trips = []
    # Finding valid trips by iterating over each partition and check if this partition is consist of valid trips.
    for partition in get_partitions(cows.keys()):
        trip_flag = True
        for trip in partition:
            trip_weights = 0
            for cow in trip:
                cow_weight = int(cows[cow])
                trip_weights += cow_weight
            if trip_weights > limit:
                trip_flag = False
                break
        if trip_flag:
            valid_trips.append(partition)
    # Finding best trip series.
    min_num_of_trips = len(valid_trips[0])
    best_trip = valid_trips[0]
    # Iterate over the valid trips and finds the trip series with the least number of trips in total.
    for trips in valid_trips:
        if len(trips) < min_num_of_trips:
            min_num_of_trips = len(trips)
            best_trip = trips
    return best_trip

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    limit = 10
    # Load the data
    cow_weights = load_cows('ps1_cow_data.txt')
    # put the start time of the greedy function in start_greedy
    start_greedy = time.time()
    # Runs the greedy function
    greedy_trip = greedy_cow_transport(cow_weights,limit)
    # Puts the end time of the greedy function in end_greedy
    end_greedy = time.time()
    # Finds the total time it took the greedy function to run
    greedy_time = end_greedy - start_greedy
    # Puts the start time of the brute force algorithm in start_brute
    start_brute = time.time()
    # Runs the brute force function
    brute_trip = brute_force_cow_transport(cow_weights, limit)
    # Puts the end time of the brute force algorithm in end_brute
    end_brute = time.time()
    # Finds the total time it took the brute force algorithm to run
    brute_time = end_brute - start_brute
    print("The greedy algorithm took %f (s) and found a solution with %d trips."%(greedy_time, len(greedy_trip)))
    print("The brute force algorithm took %f (s) and found a solution with %d trips." % (brute_time, len(brute_trip)))


# Problem 5
def dp_make_weight(cow_weights, target_weight, memo = None):
    """
    Find largest number of cows that can be brought back. Assumes there is
    an infinite supply of cows of each weight in cow_weights.

    Parameters:
    cow_weights   : tuple of ints, available cow weights sorted from smallest to
                    largest value (d1 < d2 < ... < dk)
    target_weight : int, amount of weight the spaceship can carry
    memo          : dictionary, (remaining cows, remaining weights in spaceship)(you may not
                    need to use this parameter depending on your implementation,
                    dont delete though!)

    Returns:
    int, largest number of cows that can be brought back whose weight
    equals target_weight.
    None, if no combinations of weights equal target_weight
    """
    # Checks if the target weight has been calculated before and if does it will just return the saved value
    if target_weight in memo:
        return memo[target_weight]
    # Base code, it checks if the target weight is less than the lightest cow
    elif target_weight < cow_weights[0]:
        # If the target weight is zero it will save the zero in the memo and return zero
        if target_weight == 0:
            memo[target_weight] = 0
            return 0
        # If the target weight is not zero then it will return None. Because, in this case we cannot fill the spaceship.
        else:
            memo[target_weight] = None
            return None
    # Main part of code begins here
    else:
        max_number = 0
        # Iterate over all of the cow weights
        for cow in cow_weights:
            # Checks if it can add it to the spaceship
            if cow <= target_weight:
                try:
                    temp = 1 + dp_make_weight(cow_weights, target_weight-cow, memo)
                except TypeError:
                    temp = None
                # Checks if temp is higer than out temp value that we found
                if temp != None and temp > max_number:
                    # print('In changing max, target_weight = %d'%target_weight)
                    max_number = temp
                # Adds temp to memo
                memo[target_weight] = temp
        # Checks if the spaceship is filled or not ( filled : sum of cows in spaceship = target_weight)
        if 0 not in memo:
            return None
        return max_number

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':

# Problem 1
#     cow_weights = load_cows('ps1_cow_data.txt')
#     print(cow_weights)
#     sorted_cows_name = sort_cows(cow_weights)
#     print(sorted_cows_name)

# Problem 2
#     cows = {
#                 'John' : 85,
#                 'Ana' : 75,
#                 'Carlos' : 10,
#                 'Katy' : 15,
#                 'Aasavari' : 50,
#                 'Matt' : 65,
#                 'Bethany' : 45,
#                 'Laura' : 5,
#                 'Orhan' : 60,
#                 'Kaitlin' : 20
#             }
#     sorted_cows_name = sort_cows(cows)
#     print(sorted_cows_name)
#     print(greedy_cow_transport(cows, 100))
#     x = get_partitions(sorted_cows_name)
#     print(list(x))
# Problem 3
#     print(greedy_cow_transport(cow_weights))
#     print(brute_force_cow_transport(cow_weights))
# # Problem 4
#     compare_cow_transport_algorithms()
# Problem 5
#     cow_weights = (3, 5, 8, 9)
#     n = 64
#     memo = {}
#     max_number = 0
#     print(dp_find_weight(cow_weights, n, memo))


    cow_weights = (3,5)
    n = 7
    # print("Cow weights = (3, 5, 8, 9)")
    # print("n = 64")
    # print("Expected ouput: 20 (3 * 18 + 2 * 5 = 64)")
    memo = {}
    print("Actual output:", dp_make_weight(cow_weights, n, memo))
    print()
    pass
