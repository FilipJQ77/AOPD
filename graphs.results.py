import os
import sys
import matplotlib.pyplot as plt


def read_file(filename):
    function = 0
    x_data_naive = [[], [], [], [], [], []]
    y_data_naive = [[[], [], []], [[], [], []], [[], [], []],
                    [[], [], []], [[], [], []], [[], [], []]]
    x_data_accel = [[], [], [], [], [], []]
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
                x_data_naive[function].append(line[4])
                y_data_naive[function][0].append(int(line[5])/10**6)
                y_data_naive[function][1].append(int(line[6])/10**6)
                y_data_naive[function][2].append(int(line[7])/10**6)
            else:
                x_data_accel[function].append(line[4])
                y_data_accel[function][0].append(int(line[5])/10**6)
                y_data_accel[function][1].append(int(line[6])/10**6)
                y_data_accel[function][2].append(int(line[7])/10**6)

    return [[x_data_naive, y_data_naive], [x_data_accel, y_data_accel]]


def draw_graph(data, function, version):
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

    plt.rcParams.update({'font.size': 20})
    plt.figure(num=None, figsize=(20, 8), dpi=400,
               facecolor='w', edgecolor='k')
    with open("values.csv", "a") as file:

        file.write(f"{formula} - {version}\n")
        for i in range(len(data[0][function])):
            file.write(str(data[0][function][i]) + ";" + str(data[1][function][0][i]) + ";" + str(
                data[1][function][1][i]) + ";" + str(data[1][function][2][i]) + "\n")
        file.write("\n")

    plt.plot(data[0][function], data[1][function][0], marker='o', linestyle='-', color="limegreen",
             linewidth=2, markersize=10, label="Stworzenie tablicy X")
    plt.plot(data[0][function], data[1][function][1], marker='o', linestyle='-', color="blue",
             linewidth=2, markersize=10, label="Obliczenie tablicy Y")
    plt.plot(data[0][function], data[1][function][2], marker='o', linestyle='-', color="orange",
             linewidth=2, markersize=10, label="Wyświetlenie wyników")

    plt.margins(x=None, y=None, tight=True)
    plt.legend(loc="best")
    plt.title(f"{formula} - Wersja {version}")
    plt.ylabel("Czas [ms]")
    plt.xlabel("Liczba próbek")
    plt.grid(True, color="lightgrey", alpha=0.5)
    os.makedirs("./pictures", exist_ok=True)
    save_path = "./pictures/" + str(version) + "-" + str(function) + ".png"
    plt.savefig(save_path)  # save plot to file
    # plt.show()  # show plots in IDE


def main(filename):
    data = read_file(filename)
    generate_graphs(data)
    # * < data[naive(0)/accelerated(1)][x(0)/y(1)][function(1,2,3,4,5,6)][{x_array(0)/y_array(1)/display(2)}]


def generate_graphs(data):
    for function in range(0, 6):
        draw_graph(data[0], function, "Naiwna")  # naive
        draw_graph(data[1], function, "Akcelerowana")  # accelerated


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


if __name__ == '__main__':
    suppress_qt_warnings()
    if len(sys.argv) < 2:
        print("\033[1;32m"
              "Usage: python.exe " + sys.argv[0] + " <filename>"
              "\033[1;m")
        sys.exit(0)
    filename = sys.argv[1]
    main(filename)
