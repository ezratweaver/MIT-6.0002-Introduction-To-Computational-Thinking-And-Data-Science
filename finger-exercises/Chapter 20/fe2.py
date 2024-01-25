"""Finger exercise: In a vacuum, the speed of a falling object is
defined by the equation v = v0 + gt, where v0 is the initial velocity of
the object, t is the number of seconds the object has been falling, and
g is the gravitational constant, roughly 9.8 m/sec2 on the surface of
the Earth and 3.711 m/ sec2 on Mars. A scientist measures the
velocity of a falling object on an unknown planet. She does this by
measuring the downward velocity of an object at different points in
time. At time 0, the object has an unknown velocity of v0. Implement
a function that fits a model to the time and velocity data and
estimates g for that planet and v0 for the experiment. It should
return its estimates for g and v0, and also r-squared for the model."""
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def falling_object_model(t, v0, g):
    return v0 + g * t


def fit_model_to_data(time_data, velocity_data):
    initial_guess = (velocity_data[0], 9.8)
    params, covariance = curve_fit(falling_object_model, time_data, velocity_data, p0=initial_guess)
    v0, g = params
    predicted_velocity = falling_object_model(time_data, v0, g)
    r_squared = r2_score(velocity_data, predicted_velocity)
    return v0, g, r_squared


time_data = np.array([0, 1, 2, 3, 4])
velocity_data = np.array([10.0, 20.1, 30.2, 40.3, 50.4])

estimated_v0, estimated_g, r_squared_value = fit_model_to_data(time_data, velocity_data)

print(f"Estimated initial velocity (v0): {estimated_v0}")
print(f"Estimated gravitational constant (g): {estimated_g}")
print(f"R-squared value: {r_squared_value}")
