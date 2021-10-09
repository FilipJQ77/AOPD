import math
from math import sin, cos
from numpy import linspace
import matplotlib.pyplot as plt
import statistics


def function(x):
    return (sin(x) + 2 * cos(x) ** 2 + x ** 7 - x) / x ** 2


def main():
    # todo number of samples and quantiles changeable as a slider
    number_of_samples = 100000
    quantiles_number = 100
    number_from = -5
    number_to = 5
    x_array = linspace(number_from, number_to, number_of_samples)
    y_array = [0] * number_of_samples
    for i in range(len(x_array)):
        y_array[i] = function(x_array[i])
    quantiles = statistics.quantiles(y_array, n=quantiles_number)
    for i in range(len(y_array)):
        if y_array[i] < quantiles[0]:
            y_array[i] = -math.inf
        if y_array[i] > quantiles[len(quantiles)-1]:
            y_array[i] = math.inf

    plt.plot(x_array, y_array)
    plt.waitforbuttonpress()


if __name__ == '__main__':
    main()
