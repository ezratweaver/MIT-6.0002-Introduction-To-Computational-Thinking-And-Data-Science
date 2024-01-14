"""This code was NOT written by me, it can be found here:
https://backtobackswe.com/platform/content/the-change-making-problem/solutions"""

"""Finger exercise: Use the tabular method to implement a dynamic
programming solution that meets the specification. (Page 329)"""


def make_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for j in range(0, len(coins)):
            if coins[j] <= i:
                dp[i] = min(dp[i], dp[i - coins[j]] + 1)
    return -1 if dp[amount] > amount else dp[amount]
