###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise
"""Since I used this code for my last dynamic coding problem, and this problem is
essentially the same, I thought id leav this think here as well.
https://backtobackswe.com/platform/content/the-change-making-problem/solutions"""


def dp_make_weight(egg_weight_list, target_weight):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always an egg of value 1.
    
    Parameters: egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1
    < d2 < ... < dk) target_weight - int, amount of weight we want to find eggs to fit memo - dictionary,
    OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    egg_arr = [target_weight + 1] * (target_weight + 1)
    egg_arr[0] = 0
    for i in range(1, target_weight + 1):
        for j in range(0, len(egg_weight_list)):
            if egg_weight_list[j] <= i:
                x = egg_arr[i - egg_weight_list[j]] + 1
                egg_arr[i] = min(egg_arr[i], egg_arr[i - egg_weight_list[j]] + 1)
    return -1 if egg_arr[target_weight] > target_weight else egg_arr[target_weight]


if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
