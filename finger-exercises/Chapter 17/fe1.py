"""Finger exercise: Modify the code in Figure 17-5 so that it produces
plots like those shown in Figure 17-7. (Page 377)"""
import matplotlib.pyplot as plt
import random


def flip_plot(min_exp, max_exp):
    ratios, diffs, xaxis = [], [], []
    for exp in range(min_exp, max_exp + 1):
        xaxis.append(2**exp)
    for num_flips in xaxis:
        num_heads = 0
        for n in range(num_flips):
            if random.choice(("H", "T")) == "H":
                num_heads += 1
        num_tails = num_flips - num_heads
        try:
            ratios.append(num_heads/num_tails)
            diffs.append(abs(num_heads - num_tails))
        except ZeroDivisionError:
            continue
    plt.title("Difference Between Heads and Tails")
    plt.xlabel("Number of Flips")
    plt.ylabel("Abs(#Heads - #Tails)")
    plt.xticks(rotation="vertical")
    plt.plot(xaxis, diffs, "ko")
    plt.figure()
    plt.title("Heads/Tails Ratios")
    plt.xlabel("Number of Flips")
    plt.ylabel("#Heads/#Tails")
    plt.xticks(rotation="vertical")
    plt.plot(xaxis, ratios, "ko")
    plt.show()


random.seed(0)
flip_plot(4, 20)
