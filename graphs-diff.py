import os
import sys
import matplotlib.pyplot as plt


def read_file(filename):

    x_data_naive = []
    y_data_naive = [[], [], []]
    x_data_accel = []
    y_data_accel = [[], [], []]
    with open(filename, 'r') as file:
        lines = file.readlines()[1:]  # skip first line
        for line in lines:
            line = line.split(";")
            if line[0] == "Naive":
                x_data_naive.append(str(float(line[3])*2))
                y_data_naive[0].append(int(line[5])/10**6)
                y_data_naive[1].append(int(line[6])/10**6)
                y_data_naive[2].append(int(line[7])/10**6)
            else:
                x_data_accel.append(str(float(line[3])*2))
                y_data_accel[0].append(int(line[5])/10**6)
                y_data_accel[1].append(int(line[6])/10**6)
                y_data_accel[2].append(int(line[7])/10**6)

    return [[x_data_naive, y_data_naive], [x_data_accel, y_data_accel]]


def draw_graph(data, graph_name):

    plt.rcParams.update({'font.size': 20})
    plt.figure(num=None, figsize=(20, 8), dpi=400,
               facecolor='w', edgecolor='k')

    plt.plot(data[0], data[1][0], marker='o', linestyle='-', color="limegreen",
             linewidth=2, markersize=10, label="Stworzenie tablicy X")
    plt.plot(data[0], data[1][1], marker='o', linestyle='-', color="blue",
             linewidth=2, markersize=10, label="Obliczenie tablicy Y")
    plt.plot(data[0], data[1][2], marker='o', linestyle='-', color="orange",
             linewidth=2, markersize=10, label="Wyświetlenie wyników")

    plt.margins(x=None, y=None, tight=True)
    plt.legend(loc="best")
    plt.title(graph_name)
    plt.ylabel("Czas [ms]")
    plt.xlabel("Szerokość przedziału")
    plt.grid(True, color="lightgrey", alpha=0.5)
    os.makedirs("./pictures", exist_ok=True)
    save_path = "./pictures/" + graph_name + ".png"
    plt.savefig(save_path)  # save plot to file
    # plt.show()  # show plots in IDE


def main(filename):
    data = read_file(filename)
    print("Naive")
    for i in range(len(data[0][0])):
        print(str(data[0][0][i])+";"+str(data[0][1][0][i]) +
              ";"+str(data[0][1][1][i])+";"+str(data[0][1][2][i]))
    print("Accelerated")
    for i in range(len(data[1][0])):
        print(str(data[1][0][i])+";"+str(data[1][1][0][i]) +
              ";"+str(data[1][1][1][i])+";"+str(data[1][1][2][i]))

    draw_graph(data[0], "Różne przedziały - Implementacja Naiwna")
    draw_graph(data[1], "Różne przedziały - Implementacja Akcelerowana")


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
