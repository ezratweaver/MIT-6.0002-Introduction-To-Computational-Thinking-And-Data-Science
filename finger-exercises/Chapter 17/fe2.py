"""Finger exercise: In Figure 17-19, why are the bins near the middle
of the histogram taller than the bins near the sides? (Page 388)"""
import matplotlib.pyplot as plt
import random


def rand_hist_gen():
    random.seed(0)
    vals = []
    for _ in range(1000):
        num1 = random.choice(range(0, 101))
        num2 = random.choice(range(0, 101))
        vals.append(num1 + num2)
    plt.hist(vals, bins=10, ec="k")
    plt.xlabel("Sum")
    plt.ylabel("Number of Occurrences")
    plt.show()


rand_hist_gen()

"""Answer: The probability of num1 and num2 being numbers that add to equal a number between 75 and 150
is much higher then the probability of them adding to equal a extreme low, or extreme high number.
Example. more paris withh be (150, 10), (50, 75) etc then (2, 15), (175 + 6)"""
