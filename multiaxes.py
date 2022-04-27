from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.pyplot as plt

def affiche(x, y, xmin, xmax, ymin, ymax, labelX, labelY,tx):
    host = host_subplot(111, axes_class=axisartist.Axes)
    plt.subplots_adjust(right=tx)

    n = len(y)
    par = [host.twinx() for _ in range(n-1)]
    par.insert(0, host)

    for i in range(1, n):
        par[i].axis["right"] = par[i].new_fixed_axis(loc="right", offset=(40*i, 0))
        par[i].axis["right"].toggle(all=True)

    p = [None] * n
    for i in range(n):
        p[i], = par[i].plot(x[i], y[i], label=labelY[i])

    par[0].set_xlim(xmin, xmax)
    for i in range(n):
        par[i].set_ylim(ymin[i], ymax[i])

    par[0].set_xlabel(labelX)
    par[0].set_ylabel(labelY[0])
    for i in range(1, n):
        par[i].set_ylabel(labelY[i])

    par[0].legend()

    par[0].axis["left"].label.set_color(p[0].get_color())
    for i in range(1, n):
        par[i].axis["right"].label.set_color(p[i].get_color())

    plt.show()


def affiche2(time, y, ymin, ymax, labelX, labelY, n, window_title="World3 Results"):
    fig = plt.figure(figsize=(20.48, 10.24))
    plots = [(time[i], labelY[i], y[i], ymin[i], ymax[i]) for i in range(n)]
    ax = fig.add_subplot(4, 3, 1, xlabel=labelX[0], ylabel='Population')
    for i, (time, title, data, ymin, ymax) in enumerate(plots):
        if i in range(0, 4):
            ax.plot(time, data, label=title)
            ax.legend()
        else:
            ax = fig.add_subplot(4, 3, i-2, xlabel=labelX, ylabel=title)
            ax.set_ylim(ymin, ymax)
            ax.plot(time, data)
    fig.suptitle(window_title)
    plt.show()


if __name__ == "__main__":
    n = 4
    x = [[0, 1, 2] for _ in range(n)]
    y = [[0, 1, 2], [0, 3, 2], [50, 30, 15], [10, 20, 5]]
    ymin = [0, 0, 0, 0]
    ymax = [5, 6, 80, 25]
    xmin, xmax = 0, 2
    tx =0.5
    labelX = "labelX"
    labelY = ["Density", "Temperature", "Velocity", "bbbba"]
    affiche(x, y, xmin, xmax, ymin, ymax, labelX, labelY, tx)
