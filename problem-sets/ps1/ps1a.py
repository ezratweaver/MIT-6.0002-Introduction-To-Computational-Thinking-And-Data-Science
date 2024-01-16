###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import timeit


# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_log = {}
    with open(filename) as file:
        for line in file:
            line = line.strip("\n").split(",")
            cow_log[line[0]] = int(line[1])
    return cow_log


# Problem 2
def greedy_cow_transport(cows, limit=10):
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
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_list = [(c, w) for c, w in cows.items()]
    sorted_cows = sorted(cow_list, key=lambda x: x[1], reverse=True)
    transport_list = []
    current_transport = []
    current_weight = 0
    while len(sorted_cows) != 0:
        for cow in sorted_cows:
            cow_weight = cow[1]
            if current_weight + min(sorted_cows, key=lambda x: x[1])[1] > limit: break
            if cow_weight + current_weight <= limit:
                current_transport.append(cow)
                current_weight += cow_weight
            else:
                continue
        for cow in current_transport:
            sorted_cows.remove(cow)
        transport_list.append(current_transport)
        current_weight = 0
        current_transport = []
    return transport_list


def is_set_valid(run, cow_dict, limit):
    for transport in run:
        weight = 0
        for cow in transport:
            weight += cow_dict[cow]
            if weight > limit:
                return False
    return True


def brute_force_cow_transport(cows, limit=10):
    """
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_list = list(cows.keys())
    minimum = None
    runs = []
    for x, run in enumerate(get_partitions(cow_list)):
        runs.append(run)
        if is_set_valid(run, cows, limit) is False:
            continue
        run_length = len(run)
        if minimum is None:
            minimum = run_length
            minimum_spot = x
        if run_length < minimum:
            minimum = run_length
            minimum_spot = x
    return runs[minimum_spot]


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
    cow_log = load_cows("ps1_cow_data.txt")
    start_greedy_time = timeit.default_timer()
    greedy_results = greedy_cow_transport(cow_log)
    greedy_time = round(timeit.default_timer() - start_greedy_time, 3)
    start_brute_time = timeit.default_timer()
    brute_results = brute_force_cow_transport(cow_log)
    brute_time = round(timeit.default_timer() - start_brute_time, 3)
    print(f"Greedy algorithm completed in {greedy_time} second(s) and "
          f"completed the task in {len(greedy_results)} trips")
    print(f"Brute force alogrithm completed in {brute_time} second(s) and "
          f"completed the task in {len(brute_results)} trips")


if __name__ == "__main__":
    compare_cow_transport_algorithms()
