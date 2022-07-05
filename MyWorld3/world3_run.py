import world3_graph as w3
from world3_plot import *
import matplotlib.pyplot as plt

INITIAL_TIME = 1900
FINAL_TIME = 2100
VERSION = 2003
N_SCENARIO = 5

if __name__ == "__main__":
    #########
    # Solve #
    #########
    w3.h.set_rank()
    w3.h.run(w3.NB_STEP, w3.TS.val)

    ######################
    # Plots of variables #
    ######################
    params = {'lines.linewidth': '3'}
    plt.rcParams.update(params)
    if VERSION == 1972:
        #Overview
        classic_plot(w3.t.hist,
                    [w3.nrfr.hist, w3.iopc.hist, w3.fpc.hist, w3.pop.hist, w3.ppolx.hist,
                     w3.cbr.hist, w3.cdr.hist, w3.sopc.hist],
                    ["NRFR", "IOPC", "FPC", "POP", "PPOLX", "CBR", "CDR", "SOPC"],
                    [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32], [0, 50], [0, 50], [0, 1e3]],
                    img_background="background/scenario{}-overview.png".format(N_SCENARIO),
                    grid=1,
                    title="World3 Scenario {} Overview".format(N_SCENARIO),
                    save=True)

        #Financial Sector
        classic_plot(w3.t.hist,
                    [w3.fcaor.hist, w3.io.hist, w3.tai.hist, w3.aiph.hist, w3.fioaa.hist],
                    ["FCAOR", "IO", "TAI", "AIPH", "FIOAA"],
                    [[0, 1], [0, 4e12], [0, 4e12], [0, 200], [0, 0.201]],
                    img_background="background/scenario{}-financial.png".format(N_SCENARIO),
                    grid=1,
                    title="World3 Scenario {} Financial Sector".format(N_SCENARIO),
                    save=True)

        #Agriculture Sector
        classic_plot(w3.t.hist,
                    [w3.ly.hist, w3.al.hist, w3.fpc.hist, w3.lmf.hist, w3.pop.hist],
                    ["LY", "AL", "FPC", "LMF", "POP"],
                    [[0, 4e3], [0, 4e9], [0, 800], [0, 1.6], [0, 16e9]],
                    img_background="background/scenario{}-agriculture.png".format(N_SCENARIO),
                    grid=1,
                    title="World3 Scenario {} Agricultural Sector".format(N_SCENARIO),
                    save=True)

    if VERSION == 2003:
        #State Of The World
        classic_plot(w3.t.hist,
                  [w3.nr.hist, w3.io.hist, w3.f.hist, w3.pop.hist, w3.ppolx.hist],
                  ["NR", "IO", "F", "POP", "PPOLX"],
                  [[0, 2e12], [0, 4e12], [0, 6e12], [0, 12e9], [0, 40]],
                  img_background="background/scenario{}-1.png".format(N_SCENARIO),
                  grid=False,
                  title="World3 Scenario {} State Of The World".format(N_SCENARIO),
                  save=False)

        #Material Standard Of Living
        classic_plot(w3.t.hist,
                  [w3.fpc.hist, w3.le.hist, w3.sopc.hist, w3.ciopc.hist],
                  ["FPC", "LE", "SOPC", "CIOPC"],
                  [[0, 1e3], [0, 90], [0, 1e3], [0, 250]],
                  img_background="background/scenario{}-2.png".format(N_SCENARIO),
                  grid=False,
                  title="World3 Scenario {} Material Standard Of Living".format(N_SCENARIO),
                  save=False)

        #Human Welfare And Footprint
        classic_plot(w3.t.hist,
                  [w3.hwi.hist, w3.hef.hist],
                  ["HWI", "HEF"],
                  [[0, 1], [0, 4]],
                  img_background="background/scenario{}-3.png".format(N_SCENARIO),
                  grid=False,
                  title="World3 Scenario {} Human Welfare And Footprint".format(N_SCENARIO),
                  save=False)

    #To plot other variables (here the life expectancy)
    #single_plot(w3.t.hist, [w3.le.hist], "Time (years)", ["Life Expectancy"])
