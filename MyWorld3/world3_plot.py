from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from matplotlib.image import imread

#########################
# Different way to plot #
#########################
def single_plot(time, y, labelX, labelY, window_title="World3 Results"):
    plots = [(labelY[i], y[i]) for i in range(len(y))]
    for i, (title, data) in enumerate(plots):
        plt.figure(figsize=(20.48, 10.24))
        plt.plot(time, data, label=title)
        plt.xlabel(labelX, fontsize=16)
        plt.legend(fontsize=16)
        plt.suptitle(window_title)
        plt.show()

def classic_plot(time, var_data, var_names, var_lims,
                         img_background=None,
                         title=None,
                         figsize=None,
                         dist_spines=0.09,
                         grid=False,
                         save=False):

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    var_number = len(var_data)

    fig, host = plt.subplots(figsize=figsize)
    axs = [host, ]
    for i in range(var_number-1):
        axs.append(host.twinx())

    fig.subplots_adjust(left=dist_spines*2)
    for i, ax in enumerate(axs[1:]):
        ax.spines["left"].set_position(("axes", -(i + 1)*dist_spines))
        ax.spines["left"].set_visible(True)
        ax.yaxis.set_label_position('left')
        ax.yaxis.set_ticks_position('left')

    if img_background is not None:
        im = imread(img_background)
        axs[0].imshow(im, aspect="auto",
                      extent=[time[0], time[-1],
                              var_lims[0][0], var_lims[0][1]], cmap="gray")

    ps = []
    for ax, label, ydata, color in zip(axs, var_names, var_data, colors):
        ps.append(ax.plot(time, ydata, label=label, color=color)[0])
    axs[0].grid(grid)
    axs[0].set_xlim(time[0], time[-1])

    for ax, lim in zip(axs, var_lims):
        ax.set_ylim(lim[0], lim[1])

    for ax_ in axs:
        formatter_ = EngFormatter(places=1, sep="\N{THIN SPACE}")
        ax_.tick_params(axis='y', rotation=90)
        ax_.yaxis.set_major_locator(plt.MaxNLocator(4))
        ax_.yaxis.set_major_formatter(formatter_)

    tkw = dict(size=4, width=1.5)
    axs[0].set_xlabel("time [years]")
    axs[0].tick_params(axis='x', **tkw)
    for i, (ax, p) in enumerate(zip(axs, ps)):
        ax.set_ylabel(p.get_label(), rotation="horizontal")
        ax.yaxis.label.set_color(p.get_color())
        ax.tick_params(axis='y', colors=p.get_color(), **tkw)
        ax.yaxis.set_label_coords(-i*dist_spines, 1.01)

    if title is not None:
        fig.suptitle(title, x=0.95, ha="right", fontsize=10)

    plt.tight_layout()
    plt.show()
    if save:
        plt.savefig("img/{}".format(title))
