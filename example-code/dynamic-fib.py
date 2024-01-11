def fib_memo(n, memo=None):
    """Assumes n is an int >= 0. memo used only
    by recursive calls Returns Fibonaccci of n"""
    if memo is None:
        memo = {}
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]
    except KeyError:
        result = fib_memo(n-1, memo) + fib_memo(n-2, memo)
        memo[n] = result
        return result


def fib_tab(n):
    """Assumes n is an int >= 0
        Returns Fibonacci of n"""
    tab = [1]*(n+1)
    for i in range(2, n + 1):
        tab[i] = tab[i-1] + tab[i-2]
    return tab[n]


print(fib_tab(11230))
