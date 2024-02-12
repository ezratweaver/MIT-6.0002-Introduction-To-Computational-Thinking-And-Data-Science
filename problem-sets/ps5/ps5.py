# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:
import numpy as np
import pylab
import matplotlib.pyplot as plt
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    fits_list = []

    for p in degs:
        fit = pylab.array(np.polyfit(x, y, p))
        fits_list.append(fit)

    return fits_list


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    error = ((estimated - y)**2).sum()
    mean_error = error/len(y)
    return 1 - (mean_error/np.var(y))


def evaluate_models_on_training(x, y, models,
                        degrees=None, figname="Figure1", title="Title"):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    if degrees is None:
        degrees = ["N\\A" for _ in range(len(models))]
    line_styles = ['r-', '--', '-.', ':', 'steps', '-.', '--',
                   '-|', '-', ':', '-.', '--', '-|', '-']

    plt.plot(x, y, "bo", label="Tempatures of time") 
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Tempature (Celsius)")

    for z, model in enumerate(models):
        predicted_y = np.polyval(model, x)

        label_add = ""
        if degrees[z] == 1:
            label_add = f"S\\E={round(se_over_slope(x, y, predicted_y, model), 3)}"

        rsquare = round(r_squared(y, predicted_y), 3)
        plt.plot(x, predicted_y, line_styles[z], 
                label=f"Degree={degrees[z]}, R^2={rsquare} " + label_add)


    plt.legend()
    plt.savefig(f"plots/{figname}.png")
    plt.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    yearly_averages = []
    for year in years:
        city_averages = []
        for city in multi_cities:
            temps = climate.get_yearly_temp(city, year) 
            city_averages.append(temps.sum()/len(temps))
        yearly_averages.append(sum(city_averages)/len(city_averages))
    return np.array(yearly_averages)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    avr = []
    for x in range(1, window_length):
        val = 0
        for z in range(x):
            val += y[z]
        avr.append(val/x)

    for i in range(len(y)):
        if i + window_length > len(y):
            break
        val = 0
        for x in range(window_length):
            val += y[i + x]
        avr.append(val/window_length)

    return np.array(avr)


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    error = 0.0
    for i in range(len(y)):
        error += (y[i] - estimated[i])**2
    return (error/len(y))**0.5
 

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    pass

def evaluate_models_on_testing(x, y, models, 
                    degrees=None, figname="FigureX", title="Title"):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    if degrees is None:
        degrees = ["N\\A" for _ in range(len(models))]
    line_styles = ['r-', '--', '-.', ':', 'steps', '-.', '--',
                   '-|', '-', ':', '-.', '--', '-|', '-']

    plt.plot(x, y, "bo", label="Tempatures of time") 
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Tempature (Celsius)")

    for z, model in enumerate(models):
        predicted_y = np.polyval(model, x)
        rsme = round(rsme(y, predicted_y), 3)
        plt.plot(x, predicted_y, line_styles[z], 
                label=f"Degree={degrees[z]}, rsme={rsme} ")


    plt.legend()
    plt.savefig(f"plots/{figname}.png")
    plt.show()


def codeT():
    test_x = np.array([1, 2, 3, 4, 5])
    test_y = np.array([2, 1, 4, 3, 5])
    fitlist = [1, 2, 4]

    models = generate_models(test_x, test_y, fitlist) 
    evaluate_models_on_training(test_x, test_y, models, fitlist)


def codeA1(climate):
    test_x = []
    test_y = []
    for x in range(1961, 2010):
        test_x.append(x)
        test_y.append(climate.get_daily_temp("NEW YORK", 1, 10, x))
       
    test_x = np.array(test_x)
    test_y = np.array(test_y)

    fitlist = [1]
    models = generate_models(test_x, test_y, fitlist)
    evaluate_models_on_training(test_x, test_y, models,
                fitlist, "Figure1", "Tempatures on January 10th (New York)")


def codeA4(climate):
    test_x = []
    test_y = []
    for year in range(1961, 2010):
        test_x.append(year)
        temps = climate.get_yearly_temp("NEW YORK", year)
        test_y.append(temps.sum()/len(temps))
    
    test_x = np.array(test_x)
    test_y = np.array(test_y)

    fitlist = [1]
    models = generate_models(test_x, test_y, fitlist)
    evaluate_models_on_training(test_x, test_y, models,
                    fitlist, "Figure2", "Average Yearly Tempature (New York)")


def codeB(climate):
    test_x = [year for year in range(1961, 2010)]
    test_y = gen_cities_avg(climate, CITIES, test_x)

    test_x = np.array(test_x)
    
    fitlist = [1]
    models = generate_models(test_x, test_y, fitlist)
    evaluate_models_on_training(test_x, test_y, models, fitlist,
                    "Figure3", "Average Yearly Tempature (21 Major US Cities)")


def codeC(climate):
    test_x = [year for year in range(1961, 2010)]
    test_y = gen_cities_avg(climate, CITIES, test_x)

    test_x = np.array(test_x)

    test_y = moving_average(test_y, 5)

    fitlist = [1]
    models = generate_models(test_x, test_y, fitlist)
    evaluate_models_on_training(test_x, test_y, models, fitlist, "Figure4",
                    "Moving Average of Yearly Tempature (21 Major US Cities)")


def codeD1(climate):
    test_x = [year for year in range(1961, 2010)]
    test_y = gen_cities_avg(climate, CITIES, test_x)

    test_x = np.array(test_x)

    test_y = moving_average(test_y, 5)

    fitlist = [1, 2, 20]
    models = generate_models(test_x, test_y, fitlist)
    evaluate_models_on_training(test_x, test_y, models, fitlist, "Figure5",
                    "Moving Average of Yearly Tempature (21 Major US Cities)")


def codeD2(climate):
    test_x = np.array([year for year in range(1961, 2010)])
    test_y = gen_cities_avg(climate, CITIES, test_x)

    test_y = moving_average(test_y, 5)

    fitlist = [1, 2, 20]
    models = generate_models(test_x, test_y, fitlist)

    test_x = np.array([year for year in range(2010, 2016)])
    test_y = gen_cities_avg(climate, CITIES, test_x)

    test_y = moving_average(test_y, 5)
    
    evaluate_models_on_training(test_x, test_y, models, fitlist, "Figure6",
        "Predicted Moving Average of Yearly Tempature (21 Major US Cities)")


if __name__ == '__main__':
    climate_data = Climate("data.csv")

    # codeA4(climate_data)
    # codeA1(climate_data)
    # codeB(climate_data)
    # codeC(climate_data)
    # codeD1(climate_data)

    codeD2(climate_data)

    # Part D.2
    # TODO: replace this line with your code

    # Part E
    # TODO: replace this line with your code
