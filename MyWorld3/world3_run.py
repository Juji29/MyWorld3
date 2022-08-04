########################################################################################################################
# © Copyright French Civil Aviation Authority
# Contributor: Julien LEGAVRE (2022)

# julienleg29@gmail.com

# This software is a computer program whose purpose is to produce the results
# of the World3 model described in "The Limits to Growth" and
# in "The Limits to Growth".

# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
########################################################################################################################

# It is recommended to read the note named "MyWorld3: Equations and Explanations" before using/modifying this code.

import world3_system as wsys
from world3_plot import *
import matplotlib.pyplot as plt

VERSION = 1972
INITIAL_TIME = 1900
FINAL_TIME = 2100
TIME_STEP = 0.5
N_SCENARIO = 1

if __name__ == "__main__":
    #########
    # Solve #
    #########
    wsys.world3.run(INITIAL_TIME, FINAL_TIME, TIME_STEP)

    ######################
    # Plots of variables #
    ######################
    params = {'lines.linewidth': '3'}
    plt.rcParams.update(params)
    if VERSION == 1972:
        # Overview
        classic_plot(wsys.t.hist,
                     [wsys.nrfr.hist, wsys.iopc.hist, wsys.fpc.hist, wsys.pop.hist, wsys.ppolx.hist],
                     ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                     [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                     img_background="background/scenario{}-overview.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Overview".format(N_SCENARIO),
                     save=False)

        # Financial Sector
        classic_plot(wsys.t.hist,
                     [wsys.fcaor.hist, wsys.io.hist, wsys.tai.hist, wsys.aiph.hist, wsys.fioaa.hist],
                     ["FCAOR", "IO", "TAI", "AIPH", "FIOAA"],
                     [[0, 1], [0, 4e12], [0, 4e12], [0, 200], [0, 0.201]],
                     img_background="background/scenario{}-financial.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Financial Sector".format(N_SCENARIO),
                     save=False)

        # Agriculture Sector
        classic_plot(wsys.t.hist,
                     [wsys.ly.hist, wsys.al.hist, wsys.fpc.hist, wsys.lmf.hist, wsys.pop.hist],
                     ["LY", "AL", "FPC", "LMF", "POP"],
                     [[0, 4e3], [0, 4e9], [0, 800], [0, 1.6], [0, 16e9]],
                     img_background="background/scenario{}-agriculture.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Agricultural Sector".format(N_SCENARIO),
                     save=False)

    if VERSION == 2003:
        # State Of The World
        classic_plot(wsys.t.hist,
                     [wsys.nr.hist, wsys.io.hist, wsys.f.hist, wsys.pop.hist, wsys.ppolx.hist],
                     ["NR", "IO", "F", "POP", "PPOLX"],
                     [[0, 2e12], [0, 4e12], [0, 6e12], [0, 12e9], [0, 40]],
                     img_background="background/scenario{}-1.png".format(N_SCENARIO),
                     grid=False,
                     title="World3 Scenario {} State Of The World".format(N_SCENARIO),
                     save=False)

        # Material Standard Of Living
        classic_plot(wsys.t.hist,
                     [wsys.fpc.hist, wsys.le.hist, wsys.sopc.hist, wsys.ciopc.hist],
                     ["FPC", "LE", "SOPC", "CIOPC"],
                     [[0, 1e3], [0, 90], [0, 1e3], [0, 250]],
                     img_background="background/scenario{}-2.png".format(N_SCENARIO),
                     grid=False,
                     title="World3 Scenario {} Material Standard Of Living".format(N_SCENARIO),
                     save=False)

        # Human Welfare And Footprint
        classic_plot(wsys.t.hist,
                     [wsys.hwi.hist, wsys.hef.hist],
                     ["HWI", "HEF"],
                     [[0, 1], [0, 4]],
                     img_background="background/scenario{}-3.png".format(N_SCENARIO),
                     grid=False,
                     title="World3 Scenario {} Human Welfare And Footprint".format(N_SCENARIO),
                     save=False)

    # To plot other variables (here the life expectancy)
    #single_plot(wsys.t.hist, [wsys.le.hist], "Time (years)", ["Life Expectancy"])
