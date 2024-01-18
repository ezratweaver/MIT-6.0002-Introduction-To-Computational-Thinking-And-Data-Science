"""Finger exercise: Write code to produce the plot in Figure 16-5."""
from matplotlib import pyplot as plt
import random


class Location:

    def __init__(self, x, y) -> None:
        self._x, self._y = x, y

    def move(self, delta_x, delta_y):
        return Location(self._x + delta_x, self._y + delta_y)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def dist_from(self, other):
        ox, oy = other.get_x(), other.get_y()
        x_dist, y_dist = self._x - ox, self._y - oy
        return (x_dist ** 2 + y_dist ** 2) ** 0.5

    def __str__(self):
        return f"<{self._x}, {self._y}>"


class Field:

    def __init__(self) -> None:
        self._drunks = {}

    def add_drunk(self, drunk, loc):
        if drunk in self._drunks:
            raise ValueError("Duplicate drunk")
        else:
            self._drunks[drunk] = loc

    def move_drunk(self, drunk):
        if drunk not in self._drunks:
            raise ValueError("Drunk not in field")
        x_dist, y_dist = drunk.take_step()
        current_location = self._drunks[drunk]
        self._drunks[drunk] = current_location.move(x_dist, y_dist)

    def get_loc(self, drunk):
        if drunk not in self._drunks:
            raise ValueError("Drunk not in field")
        return self._drunks[drunk]


class Drunk:

    def __init__(self, name=None):
        self._name = name

    def __str__(self):
        if self._name is not None:
            return self._name
        return "Anonymous"


class Usual_drunk(Drunk):

    def take_step(self):
        step_choices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(step_choices)


class Cold_drunk(Drunk):

    def take_step(self):
        step_choices = [(0.0, 1.0), (0.0, -2.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)


class EW_drunk(Drunk):

    def take_step(self):
        step_choices = [(1.0, 0.0), (-1.0, 0.0)]
        return random.choice(step_choices)


def walk(f, d, num_steps):
    start = f.get_loc(d)
    for s in range(num_steps):
        f.move_drunk(d)
    return start.dist_from(f.get_loc(d))


def sim_walks(num_steps, num_trials, d_class):
    homer = d_class()
    origin = Location(0, 0)
    distances = []
    for t in range(num_trials):
        f = Field()
        f.add_drunk(homer, origin)
        distances.append(round(walk(f, homer, num_steps)))
    return distances


def drunk_test(walk_lengths, num_trials, d_class):
    mean_dist = []
    steps = []
    for num_steps in walk_lengths:
        distances = sim_walks(num_steps, num_trials, d_class)
        mean_dist.append(sum(distances) / len(distances))
        steps.append(num_steps)
        print(d_class.__name__, "walk of", num_steps, "steps: Mean =",
              f"{sum(distances) / len(distances):.3f} Max = {max(distances)}, Min = {min(distances)}")
    return mean_dist, steps


def sim_all(drunk_kinds, walk_lengths, num_trials):
    for d_class in drunk_kinds:
        drunk_test(walk_lengths, num_trials, d_class)


def plot_test(mean_dist, steps):
    plt.title("Mean distance from Origin")
    plt.plot(mean_dist, steps, label="Usual Drunk")
    plt.ylabel("Distance from origin")
    plt.xlabel("Number of Steps")
    plt.legend()
    plt.show()


m, s = drunk_test((10, 100, 1000, 10000), 100, Usual_drunk)
plot_test(m, s)
# sim_all((Usual_drunk, Cold_drunk, EW_drunk), (100, 1000), 10)
