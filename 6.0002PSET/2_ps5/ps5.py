# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Elaheh Ahmadi
# Collaborators (discussion): Raveen Nzilani
# Time: +20h

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from sklearn.metrics import r2_score
import re

params = {'legend.fontsize': 'medium',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'medium',
         'axes.titlesize':'medium',
         'xtick.labelsize':'medium',
         'ytick.labelsize':'medium'}
pylab.rcParams.update(params)
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE', 
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

TRAINING_INTERVAL = range(1961, 2011)
TESTING_INTERVAL = range(2011, 2017)

"""
Begin helper code
"""
class Temperature(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Temperature instance, which stores the temperature records
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
            a 1-d numpy array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

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
        assert year in self.rawdata[city], "provided year {} is not available".format(year)
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
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by a linear
            regression model
        model: a numpy array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: a 1-d numpy array of length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array of length N, representing the y-coordinates of
            the N sample points
        degs: a list of integers that correspond to the degree of each polynomial 
            model that will be fit to the data

    Returns:
        a list of numpy arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    # Iterates over the degrees
    for deg in degs:
        # Fits a polynomial with order deg
        model = np.polyfit(x,y,deg)
        models.append(model)
    return models


def evaluate_models_on_training(x, y, models, plt_name = None):
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
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # Iterates over the models
    for model in models:
        # Creates the polynomial function
        p = np.poly1d(model)
        # Calculates the predicted ys
        y_pred = p(x)
        # Calculates the regression
        r_2 = r2_score(y, y_pred)
        # Calculates the SE/slope
        se_slope = se_over_slope(x, y, y_pred, model)
        fig = plt.figure()
        plt.plot(x, y, 'bo')
        plt.plot(x, y_pred, 'r-')
        if len(model) == 1:
            plt.title('This is the plot of model with degree %d, and regression = %f and standard error of the fitted '
                      'curve = --' %(len(model)-1, r_2))
        else:
            plt.title('This is the plot of model with degree %d, and regression = %f and standard error of the fitted '
                      'curve = %f' %(len(model)-1, r_2, se_slope), )
        plt.xlabel('Years')
        plt.ylabel('Temperature (Celsius)')
        if plt_name:
            fig.savefig(plt_name)
        plt.show()



def gen_cities_avg(temp, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        temp: instance of Temperature
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a numpy 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    sumtemp = np.zeros(len(years))
    for city in multi_cities:
        for i in range(len(years)):
            city_temps = np.average(temp.get_yearly_temp(city, years[i]))
            sumtemp[i] += city_temps
    avg_temp = sumtemp/len(multi_cities)
    return avg_temp


def find_interval(x, y, length, has_positive_slope):
    """
    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        length: the length of the interval
        has_positive_slope: a boolean whose value specifies whether to look for
            an interval with the most extreme positive slope (True) or the most
            extreme negative slope (False)

    Returns:
        a tuple of the form (i, j) such that the application of linear (deg=1)
        regression to the data in x[i:j], y[i:j] produces the most extreme
        slope and j-i = length.

        In the case of a tie, it returns the most recent interval. For example,
        if the intervals (2,5) and (8,11) both have the same slope, (8,11) should
        be returned.

        If such an interval does not exist, returns None
    """
    extreme_slope = 0
    extreme_interval = None
    # Determines the slope sign
    slope_sign = 1 if has_positive_slope else -1
    # Iterates over the possible ranges calculates the slope and finds the most extreme slope.
    for i in range(len(x)-length+1):
        model = generate_models(x[i:i+length],y[i:i+length],[1])[0]
        if slope_sign*(model[0] - extreme_slope) >= 0 or abs(model[0]-extreme_slope) <= 1e-8:
            extreme_slope = model[0]
            extreme_interval = (i, i+length)
    return extreme_interval

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d numpy array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    sum_sqr = 0
    for i in range(len(y)):
        # Finds the square sum
        sum_sqr += (y[i] - estimated[i])**2
    # Returns the RMSE
    return (sum_sqr/len(y))**.5

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model's estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: a 1-d numpy array with length N, representing the x-coordinates of
            the N sample points
        y: a 1-d numpy array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a numpy array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        # Creates the polynomial function
        p = np.poly1d(model)
        # Calculates the predicted ys
        y_pred = p(x)
        RMSE =rmse(y, y_pred)
        plt.plot(x, y, 'bo')
        plt.plot(x, y_pred, 'r-')
        plt.title('This is the plot of predicted value of the test set with the model of degree %d and RMSE = %f'%
                      (len(model) - 1, RMSE))
        plt.xlabel('Years')
        plt.ylabel('Temperature (Celsius)')
        plt.show()



if __name__ == '__main__':
    print(generate_models(np.array([1961, 1962, 1963]),
                          np.array([-4.4, -5.5, -6.6]), [1, 2]))
    # Problem 3A
    # Gets the data
    data = Temperature('data.csv')
    years = range(1961, 2017)
    years = np.asarray(years)
    daily_data = np.zeros(len(years))
    # Puts the daily input into the daily_data numpy array
    for i in range(len(years)):
        daily_data[i] = data.get_daily_temp('BOSTON', 2, 14, years[i])
    # Generates the model
    models_neg = generate_models(years, daily_data, [1])
    # Evaluate the model by plotting the data
    # evaluate_models_on_training(years, daily_data, models)

    # Problem 3B
    avg_data = gen_cities_avg(data, ['BOSTON'], years)
    # Generates the model
    models_neg = generate_models(years, avg_data, [1])
    # Evaluate the model by plotting the data
    # evaluate_models_on_training(years, avg_data, models)

    # Problem 4B
    SD_data = gen_cities_avg(data, ['SAN DIEGO'], years)
    # Finding the best increasing interval
    result_pos = find_interval(years, SD_data, 30, True)
    models_pos = generate_models(years[result_pos[0]:result_pos[1]], SD_data[result_pos[0]:result_pos[1]], [1])
    print(result_pos)
    print(models_pos)
    # evaluate_models_on_training(years[result_pos[0]:result_pos[1]], SD_data[result_pos[0]:result_pos[1]], models_pos)
    # Finding the best decreasing interval
    result_neg = find_interval(years, SD_data, 30, False)
    models_neg = generate_models(years[result_neg[0]:result_neg[1]], SD_data[result_neg[0]:result_neg[1]], [1])
    print(result_neg)
    print(models_neg)
    # evaluate_models_on_training(years[result_neg[0]:result_neg[1]], SD_data[result_neg[0]:result_neg[1]], models_neg)

    # Finding the best decreasing window for national average annual temperature.
    national_avg_data = gen_cities_avg(data, CITIES, years)
    latest_found = None
    for window in range(2, len(years)):
        national_result_neg = find_interval(years, national_avg_data, window, False)
        if national_result_neg:
            i = national_result_neg[0]
            j = national_result_neg[1]
            national_model = generate_models(years[i:j], national_avg_data[i:j], [1])
            if national_model[0][0] < 0:
                latest_found = (national_result_neg, national_model)
                i = latest_found[0][0]
                j = latest_found[0][1]
                fig_name = 'model_wind' + str(window)+'.png'
                evaluate_models_on_training(years[i:j], national_avg_data[i:j], latest_found[1], fig_name)
    # evaluate_models_on_training(years, national_avg_data, generate_models(years, national_avg_data, [1]))

    # Problem 5B
    # Generating training set
    national_avg_data = gen_cities_avg(data, CITIES, years)
    trainig_set = national_avg_data[:len(TRAINING_INTERVAL)]
    # Generating the test set
    test_set = national_avg_data[len(TRAINING_INTERVAL):]
    models = generate_models(np.asarray(TRAINING_INTERVAL), trainig_set, [1,2,20])
    evaluate_models_on_training(np.asarray(TRAINING_INTERVAL), trainig_set, models)
    evaluate_models_on_testing(np.asarray(TESTING_INTERVAL), test_set, models)


