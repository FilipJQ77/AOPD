import math
import os
import statistics
import sys
from abc import ABC, abstractmethod
from time import perf_counter_ns as timer

import pycuda.autoinit
import matplotlib.pyplot as plt
import numpy as np
import pycuda.cumath as cumath
import pycuda.gpuarray as gpuarray


def linear_function(x):
    return x * 2


def polynomial_function_naive(x):
    return x ** 5 - 8 * x ** 4 + 3 * x ** 3 - 20 * x ** 2 - 1729 * x + math.sqrt(x) + 42069


def polynomial_function_accelerated(x):
    return x ** 5 - 8 * x ** 4 + 3 * x ** 3 - 20 * x ** 2 - 1729 * x + cumath.sqrt(x) + 42069


def trigonometric_function_naive(x: float) -> float:
    return math.sin(x) + math.cos(x) + 2 * math.tan(x)


def trigonometric_function_accelerated(x: gpuarray) -> gpuarray:
    return cumath.sin(x) + cumath.cos(x) + 2 * cumath.tan(x)


def exponential_function_naive(x: float) -> float:
    return math.exp(x) + math.pi ** (x / 2 - 10)


def exponential_function_accelerated(x: gpuarray) -> gpuarray:
    return cumath.exp(x) + math.pi ** (x / 2 - 10)


def logarithmic_function_naive(x: float) -> float:
    return math.log(x) - math.log10(x / 3)


def logarithmic_function_accelerated(x: gpuarray) -> gpuarray:
    return cumath.log(x) - cumath.log10(x / 3)


def composite_function_naive(x: float) -> float:
    return math.sin(math.log10(math.sqrt(x * 2 + 69)) + math.exp(x))


def composite_function_accelerated(x: gpuarray) -> gpuarray:
    return cumath.sin(cumath.log10(cumath.sqrt(x * 2 + 69)) + cumath.exp(x))


class Calculator(ABC):
    @abstractmethod
    def calculate(self, x_points, math_function, number_of_samples):
        pass


class NaiveCalculator(Calculator):
    def calculate(self, x_points, math_function, number_of_samples):
        y_points = np.zeros(number_of_samples, dtype=np.float64)
        for i in range(number_of_samples):
            y_points[i] = math_function(x_points[i])
        return y_points


class AcceleratedCalculator(Calculator):
    def calculate(self, x_points, math_function, number_of_samples):
        # CUDA magic
        y_points = np.zeros(number_of_samples, dtype=np.float64)
        x_array_gpu = gpuarray.to_gpu(x_points)
        math_function(x_array_gpu).get(y_points)
        return y_points


# optional: removing the highest and the lowest points if the plot is flat because of them
def calculate_quantiles(y_array):
    quantile_number = int(input("Quantile number (0 if no quantiles): "))
    if quantile_number >= 1:
        quantiles = statistics.quantiles(y_array, n=quantile_number)
        for i in range(len(y_array)):
            if y_array[i] < quantiles[0]:
                y_array[i] = math.inf
            if y_array[i] > quantiles[len(quantiles) - 1]:
                y_array[i] = math.inf
    return y_array


def main():
    # warning suppression https://stackoverflow.com/a/63598551
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    calculation_type = int(sys.argv[1])
    number_from = float(sys.argv[2])
    number_to = float(sys.argv[3])
    number_of_samples = int(sys.argv[4])
    function_type = int(sys.argv[5])
    repetitions = int(sys.argv[6])
    show_plot = int(sys.argv[7])
    filename = sys.argv[8]
    if show_plot != 0:
        show_plot = True
    else:
        show_plot = False

    math_function = linear_function  # default function
    function_str = "x * 2"

    if calculation_type == 1:
        calculator = NaiveCalculator()
        if function_type == 1:
            math_function = linear_function
            function_str = "x * 2"
        elif function_type == 2:
            math_function = polynomial_function_naive
            function_str = "x^5 - 8 * x^4 + 3 * x^3 - 20 * x^2 - 1729 * x + sqrt(x) + 42069"
        elif function_type == 3:
            math_function = trigonometric_function_naive
            function_str = "sin(x) + cos(x) + 2 * tan(x)"
        elif function_type == 4:
            math_function = exponential_function_naive
            function_str = "exp(x) + pi^(x / 2 - 10)"
        elif function_type == 5:
            math_function = logarithmic_function_naive
            function_str = "ln(x) - log10(x / 3)"
        elif function_type == 6:
            math_function = composite_function_naive
            function_str = "sin(log10(sqrt(x * 2 + 69))) + exp(x))"
    elif calculation_type == 2:
        calculator = AcceleratedCalculator()
        if function_type == 1:
            math_function = linear_function
            function_str = "x * 2"
        elif function_type == 2:
            math_function = polynomial_function_accelerated
            function_str = "x^5 - 8 * x^4 + 3 * x^3 - 20 * x^2 - 1729 * x + sqrt(x) + 42069"
        elif function_type == 3:
            math_function = trigonometric_function_accelerated
            function_str = "sin(x) + cos(x) + 2 * tan(x)"
        elif function_type == 4:
            math_function = exponential_function_accelerated
            function_str = "exp(x) + pi^(x / 2 - 10)"
        elif function_type == 5:
            math_function = logarithmic_function_accelerated
            function_str = "ln(x) - log10(x / 3)"
        elif function_type == 6:
            math_function = composite_function_accelerated
            function_str = "sin(log10(sqrt(x * 2 + 69))) + exp(x))"
    else:
        return

    for _ in range(repetitions):
        x_time_start = timer()
        x_array = np.linspace(number_from, number_to, number_of_samples)

        x_time_stop = timer()

        y_time_start = timer()
        y_array = calculator.calculate(x_array, math_function, number_of_samples)
        y_time_stop = timer()

        plot_time_start = timer()
        plt.title(function_str)
        plt.plot(x_array, y_array)
        plot_time_stop = timer()

        x_array_time = x_time_stop - x_time_start
        y_array_time = y_time_stop - y_time_start
        plot_time = plot_time_stop - plot_time_start

        if show_plot:
            plt.waitforbuttonpress()  # display plot

        # create header for new file
        with open(filename, 'a') as file:
            if os.stat(file.name).st_size == 0:
                file.write(
                    "Implementation;"
                    "Math function;"
                    "Number from;"
                    "Number to;"
                    "Number of samples;"
                    "Time - Creating x array;"
                    "Time - Calculating y array;"
                    "Time - Plotting results"
                    "\n")
            file.write(
                f"{'Naive      ' if calculation_type == 1 else 'Accelerated'};"
                f"{function_str};"
                f"{number_from};"
                f"{number_to};"
                f"{number_of_samples};"
                f"{x_array_time};"
                f"{y_array_time};"
                f"{plot_time}"
                f"\n")


if __name__ == '__main__':
    main()
