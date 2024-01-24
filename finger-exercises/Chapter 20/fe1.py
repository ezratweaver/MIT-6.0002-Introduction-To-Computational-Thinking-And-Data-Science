import numpy as np
import matplotlib.pyplot as plt
import math


def get_data(input_file):
    with open(input_file, 'r') as data_file:
        distances = []
        masses = []
        data_file.readline() #ignore header
        for line in data_file:
            d, m = line.split(',')
            distances.append(float(d))
            masses.append(float(m))
    return (masses, distances)


def plot_data(input_file):
    masses, distances = get_data(input_file)
    distances = np.array(distances) 
    masses = np.array(masses)
    forces = masses*9.81
    plt.plot(forces, distances, 'bo',
               label = 'Measured displacements')
    plt.title('Measured Displacement of Spring')
    plt.xlabel('|Force| (Newtons)')
    plt.ylabel('Distance (meters)')


def fit_data(input_file):
    masses, distances = get_data(input_file)
    distances = np.array(distances)
    forces = np.array(masses) * 9.81

    plt.plot(forces, distances, 'ko', label='Measured displacements')
    plt.title('Measured Displacement of Spring')
    plt.xlabel('|Force| (Newtons)')
    plt.ylabel('Distance (meters)')

    # Linear fit
    a, b = np.polyfit(forces, distances, 1)
    k_linear = 1.0 / a
    extended_forces_linear = np.linspace(min(forces), max(forces) * 1.5, 100)
    predicted_distances_linear = a * extended_forces_linear + b
    plt.plot(extended_forces_linear, predicted_distances_linear, label=f'Linear fit, k = {round(k_linear, 5)}')

    # Cubic fit
    fit_cubic = np.polyfit(forces, distances, 3)
    extended_forces_cubic = np.linspace(min(forces), max(forces) * 1.5, 100)
    predicted_distances_cubic = np.polyval(fit_cubic, extended_forces_cubic)
    plt.plot(extended_forces_cubic, predicted_distances_cubic, 'k:', label='Cubic fit')

    plt.legend(loc='best')
    plt.show() 


fit_data("springData.csv")

