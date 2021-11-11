import sys
import numpy as np


def read_file(filename):
    function = 0
    y_data_naive = [[[], [], []], [[], [], []], [[], [], []],
                    [[], [], []], [[], [], []], [[], [], []]]
    y_data_accel = [[[], [], []], [[], [], []], [[], [], []],
                    [[], [], []], [[], [], []], [[], [], []]]
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]  # skip first line
        for line in lines:
            line = line.split(";")
            if line[1] == "x * 2":
                function = 0
            elif line[1] == "x^5 - 8 * x^4 + 3 * x^3 - 20 * x^2 - 1729 * x + sqrt(x) + 42069":
                function = 1
            elif line[1] == "sin(x) + cos(x) + 2 * tan(x)":
                function = 2
            elif line[1] == "exp(x) + pi^(x / 2 - 10)":
                function = 3
            elif line[1] == "ln(x) - log10(x / 3)":
                function = 4
            elif line[1] == "sin(log10(sqrt(x * 2 + 69))) + exp(x))":
                function = 5
            if line[0] == "Naive":
                y_data_naive[function][0].append(int(line[5]))
                y_data_naive[function][1].append(int(line[6]))
                y_data_naive[function][2].append(int(line[7]))
            else:
                y_data_accel[function][0].append(int(line[5]))
                y_data_accel[function][1].append(int(line[6]))
                y_data_accel[function][2].append(int(line[7]))

    return [y_data_naive, y_data_accel]


def calculate_mean(data):
    mean_results = []
    for function in range(0, 6):
        for implement in range(2):
            if function == 0:
                formula = "x * 2"
            elif function == 1:
                formula = "x^5 - 8 * x^4 + 3 * x^3 - 20 * x^2 - 1729 * x + sqrt(x) + 42069"
            elif function == 2:
                formula = "sin(x) + cos(x) + 2 * tan(x)"
            elif function == 3:
                formula = "exp(x) + pi^(x / 2 - 10)"
            elif function == 4:
                formula = "ln(x) - log10(x / 3)"
            elif function == 5:
                formula = "sin(log10(sqrt(x * 2 + 69))) + exp(x))"
            if implement == 0:
                implementation = "Naive"
            else:
                implementation = "Accelerated"
            mean_results.append([implementation, formula, 1, 10, 100000000, np.mean(
                data[implement][function][0]), np.mean(data[implement][function][1]), np.mean(data[implement][function][2])])
    return mean_results


def main(filename):
    data = read_file(filename)
    mean = calculate_mean(data)
    with open("values100mil.csv", "a") as file:
        for line in mean:
            file.write(
                f"{line[0]};{line[1]};{float(line[2])};{float(line[3])};{line[4]};{int(line[5])};{int(line[6])};{int(line[7])}\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\033[1;32m"
              "Usage: python.exe " + sys.argv[0] + " <filename>"
              "\033[1;m")
        sys.exit(0)
    filename = sys.argv[1]
    main(filename)
