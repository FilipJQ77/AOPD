import statistics
from abc import ABC, abstractmethod
from math import sin, cos, inf
from time import perf_counter_ns as timer

import matplotlib.pyplot as plt
import pycuda.cumath as cumath
import pycuda.gpuarray as gpuarray
from numpy import linspace

# import pycuda.driver as cuda
# import pycuda.autoinit
# from pycuda.compiler import SourceModule

function = "sin(x) + 2 * cos(x) ** 2 - x"  # variable with function for .csv file


def math_function(x: float) -> float:
    return sin(x) + 2 * cos(x) ** 2 - x


class Calculator(ABC):
    @abstractmethod
    def calculate(self, x_points, number_of_samples):
        pass


class NaiveCalculator(Calculator):
    def calculate(self, x_points, number_of_samples):
        y_points = [0] * number_of_samples
        for i in range(number_of_samples):
            self.function = math_function(x_points[i])
            y_points[i] = self.function
        return y_points


class AcceleratedCalculator(Calculator):
    def calculate(self, x_points, number_of_samples):
        # y_points = [0] * number_of_samples
        # function_gpu = cuda.mem_alloc_like(number_of_samples)
        # cuda.memcpy_htod(function_gpu, number_of_samples)
        # module = SourceModule(
        #     """
        #         __global__ void calculate(double *x_points, double *y_points, int number_of_samples)
        #         {
        #             // __device__ double sin ( double  x)
        #
        #             int idx = threadIdx.x + threadIdx.y*4;
        #             y_point[idx] = sin(x) + 2 * cos(x) ** 2 - x;
        #         }
        #     """
        # )
        # result = module.get_function("calculate")
        # result(function_gpu)

        # CUDA magic
        x_array_gpu = gpuarray.to_gpu(x_points)
        y_points = (cumath.sin(x_array_gpu) + 2 * cumath.cos(x_array_gpu) ** 2 - x_array_gpu).get()
        return y_points


#  ##  Additional  ##
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
    x_array = linspace(number_from, number_to, number_of_samples)
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

    # plt.waitforbuttonpress()  # display plot
    with open("results.csv", 'a') as file:
        file.write(
            f"{'Naive' if calculation_type == 1 else 'Accelerated'};\t"
            f"{function};\t"
            f"{number_from};\t"
            f"{number_to};\t"
            f"{number_of_samples};\t"
            f"{x_array_time};\t"
            f"{y_array_time};\t"
            f"{plot_time};\t"
            f"\n")

        # create header for new file
        # file.write(f"math_function;number_from;number_to;number_of_samples;x_array_time;y_array_time;plot_time")


if __name__ == '__main__':
    main()
