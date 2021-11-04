import statistics
from abc import ABC, abstractmethod
from math import sin, cos, inf
from time import perf_counter_ns as timer

import matplotlib.pyplot as plt
import numpy as np
import pycuda.cumath as cumath
import pycuda.gpuarray as gpuarray

# import pycuda.driver as cuda
# import pycuda.autoinit
# from pycuda.compiler import SourceModule

function = "sin(x) + 2 * cos(x) ** 2 - x"  # variable with function for .csv file


def math_function_naive(x: float) -> float:
    return sin(x) + 2 * cos(x) ** 2 - x  # todo is cumath possible here? if yes, then we can use one function for both


def math_function_accelerated(x: gpuarray) -> gpuarray:
    return cumath.sin(x) + 2 * cumath.cos(x) ** 2 - x


class Calculator(ABC):
    @abstractmethod
    def calculate(self, x_points, number_of_samples):
        pass


class NaiveCalculator(Calculator):
    def calculate(self, x_points, number_of_samples):
        y_points = np.zeros(number_of_samples, dtype=np.float64)
        for i in range(number_of_samples):
            y_points[i] = math_function_naive(x_points[i])
        return y_points


class AcceleratedCalculator(Calculator):
    def calculate(self, x_points, number_of_samples):
        # CUDA magic
        y_points = np.zeros(number_of_samples, dtype=np.float64)
        x_array_gpu = gpuarray.to_gpu(x_points)
        math_function_accelerated(x_array_gpu).get(y_points)  # todo check if works, if not then use line below
        # y_points = math_function_accelerated(x_array_gpu).get()
        return y_points


# optional: removing the highest and the lowest points if the plot is flat because of them
def calculate_quantiles(y_array):
    quantile_number = int(input("Quantile number (0 if no quantiles): "))
    if quantile_number >= 1:
        quantiles = statistics.quantiles(y_array, n=quantile_number)
        for i in range(len(y_array)):
            if y_array[i] < quantiles[0]:
                y_array[i] = inf
            if y_array[i] > quantiles[len(quantiles) - 1]:
                y_array[i] = inf
    return y_array


def main():
    calculation_type = int(input("1. Naive\n2. Accelerated\n"))
    if calculation_type == 1:
        calculator = NaiveCalculator()
    elif calculation_type == 2:
        calculator = AcceleratedCalculator()
    else:
        return

    number_from = float(input("Number from: "))
    number_to = float(input("Number to: "))
    number_of_samples = int(input("Number of samples: "))

    x_time_start = timer()
    x_array = np.linspace(number_from, number_to, number_of_samples)
    x_time_stop = timer()

    y_time_start = timer()
    y_array = calculator.calculate(x_array, number_of_samples)
    y_time_stop = timer()

    plot_time_start = timer()
    plt.plot(x_array, y_array)
    plot_time_stop = timer()

    x_array_time = x_time_stop - x_time_start
    y_array_time = y_time_stop - y_time_start
    plot_time = plot_time_stop - plot_time_start

    plt.waitforbuttonpress()  # display plot

    # create header for new file
    with open("results.csv", 'a') as file:
        # file.write(
        #     "Implementation;"
        #     "Math function;"
        #     "Number from;"
        #     "Number to;"
        #     "Number of samples;"
        #     "Time - Creating x array;"
        #     "Time - Calculating y array;"
        #     "Time - Plotting results"
        #     "\n")
        file.write(
            f"{'Naive' if calculation_type == 1 else 'Accelerated'};"
            f"{function};"
            f"{number_from};"
            f"{number_to};"
            f"{number_of_samples};"
            f"{x_array_time};"
            f"{y_array_time};"
            f"{plot_time}"
            f"\n")


if __name__ == '__main__':
    main()
