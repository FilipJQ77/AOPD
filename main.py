from abc import ABC, abstractmethod
from math import sin, cos, inf
from numpy import linspace
import matplotlib.pyplot as plt
import statistics


class Calculator(ABC):
    @abstractmethod
    def calculate(self, x_points, math_function, number_of_samples):
        pass


class NaiveCalculator(Calculator):
    def calculate(self, x_points, math_function, number_of_samples):
        y_points = [0] * number_of_samples
        for i in range(len(x_points)):
            y_points[i] = math_function(x_points[i])
        return y_points


class AcceleratedCalculator(Calculator):
    def calculate(self, x_points, math_function, number_of_samples):
        y_points = [0] * number_of_samples
        # todo CUDA magic
        return y_points


def main():
    while True:
        calculation_type = int(input("1. Naive\n2. Accelerated\n"))
        if calculation_type == 1:
            calculator = NaiveCalculator()
        elif calculation_type == 2:
            calculator = AcceleratedCalculator()
        else:
            return

        def math_function(x: float) -> float:
            return sin(x) + 2 * cos(x) ** 2 - x

        number_from = float(input("Number from: "))
        number_to = float(input("Number to: "))
        number_of_samples = int(input("Number of samples: "))
        quantile_number = int(input("Quantile number (0 if no quantiles): "))

        x_array = linspace(number_from, number_to, number_of_samples)
        y_array = calculator.calculate(x_array, math_function, number_of_samples)
        if quantile_number >= 1:
            quantiles = statistics.quantiles(y_array, n=quantile_number)
            for i in range(len(y_array)):
                if y_array[i] < quantiles[0]:
                    y_array[i] = inf
                if y_array[i] > quantiles[len(quantiles) - 1]:
                    y_array[i] = inf

        plt.plot(x_array, y_array)
        plt.waitforbuttonpress()


if __name__ == '__main__':
    main()
