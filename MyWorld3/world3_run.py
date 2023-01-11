########################################################################################################################
# © Copyright French Civil Aviation Authority
# Author: Julien LEGAVRE (2022)

# julien.legavre@alumni.enac.fr

# This software is a computer program whose purpose is to produce the results
# of the World3 model described in "The Limits to Growth" and
# in "The Limits to Growth: The 30-Year Update".

# This software is governed by the GNU General Public License version 2.0.
# This software is also governed by the CeCILL license under French law and
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
# knowledge of the GNU General Public License version 2.0 or the CeCILL  
# license and that you accept its terms.
########################################################################################################################

# It is recommended to read the note named "MyWorld3: Equations and Explanations" before using/modifying this code.

import sys
import world3_system as w_sys
import world3_dynamic as sd
from world3_plot import *
import matplotlib.pyplot as plt

VERSION = 2003
INITIAL_TIME = 1900
FINAL_TIME = 2100
TIME_STEP = 0.5
N_SCENARIO = 1

if __name__ == "__main__":
    #########
    # Solve #
    #########
    nbarg = len(sys.argv)
    try:
        #version    = VERSION
        N_SCENARIO = N_SCENARIO if nbarg == 1 else int(sys.argv[1])
    except Exception as e:
        print(f"Usage:\npython world3_run.py <no_scenario=1..10>\n")
        raise e
    try:
        world3 = sd.World3(VERSION, N_SCENARIO, INITIAL_TIME, FINAL_TIME, TIME_STEP)
        w_sys.load(world3)
    except ValueError:
        print("VERSION must be an integer.")
        exit(0)

    try:
        INITIAL_TIME < 0
    except ValueError:
        print("INITIAL_TIME must be a positive integer.")

    try:
        FINAL_TIME < INITIAL_TIME
    except ValueError:
        print("FINAL_TIME must be a positive integer higher than INITIAL_TIME.")

    try:
        INITIAL_TIME < TIME_STEP < 0
    except ValueError:
        print("TIME_STEP must be a positive float lower than INITIAL_TIME.")

    try:
        N_SCENARIO < 0
    except ValueError:
        print("N_SCENARIO must be a positive integer.")

    world3.run()#INITIAL_TIME, FINAL_TIME, TIME_STEP)
    ######################
    # Plots of variables #
    ######################
    params = {'lines.linewidth': '3'}
    plt.rcParams.update(params)
    if VERSION == 1972:
        # Overview
        #classic_plot(world3.nodes["t"].hist,
        #             [world3.nodes["nrfr"].hist, world3.nodes["iopc.hist, world3.nodes["fpc.hist, world3.nodes["pop.hist, world3.nodes["ppolx.hist],
        classic_plot(world3.nodes["time"].hist,
                     [world3.nodes["nrfr"].hist, world3.nodes["iopc"].hist, world3.nodes["fpc"].hist, world3.nodes["pop"].hist, world3.nodes["ppolx"].hist],
                     ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
                     [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
                     #img_background="background/scenario{}-overview.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Overview".format(N_SCENARIO),
                     save=False)

        # Financial Sector
        classic_plot(world3.nodes["time"].hist,
                     [world3.nodes["fcaor"].hist, world3.nodes["io"].hist, world3.nodes["tai"].hist, world3.nodes["aiph"].hist, world3.nodes["fioaa"].hist],
                     ["FCAOR", "IO", "TAI", "AIPH", "FIOAA"],
                     [[0, 1], [0, 4e12], [0, 4e12], [0, 200], [0, 0.201]],
                     #img_background="background/scenario{}-financial.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Financial Sector".format(N_SCENARIO),
                     save=False)

        # Agriculture Sector
        classic_plot(world3.nodes["time"].hist,
                     [world3.nodes["ly"].hist, world3.nodes["al"].hist, world3.nodes["fpc"].hist, world3.nodes["lmf"].hist, world3.nodes["pop"].hist],
                     ["LY", "AL", "FPC", "LMF", "POP"],
                     [[0, 4e3], [0, 4e9], [0, 800], [0, 1.6], [0, 16e9]],
                     #img_background="background/scenario{}-agriculture.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Agricultural Sector".format(N_SCENARIO),
                     save=False)

    if VERSION == 2003:
        # State Of The World
        classic_plot(world3.nodes["time"].hist,
                     [world3.nodes["nr"].hist, world3.nodes["io"].hist, world3.nodes["f"].hist, world3.nodes["pop"].hist, world3.nodes["ppolx"].hist],
                     ["NR", "IO", "F", "POP", "PPOLX"],
                     [[0, 2e12], [0, 4e12], [0, 6e12], [0, 12e9], [0, 40]],
                     img_background="background/scenario{}-1.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} State Of The World".format(N_SCENARIO),
                     save=False)

        # Material Standard Of Living
        classic_plot(world3.nodes["time"].hist,
                     [world3.nodes["fpc"].hist, world3.nodes["le"].hist, world3.nodes["sopc"].hist, world3.nodes["ciopc"].hist],
                     ["FPC", "LE", "SOPC", "CIOPC"],
                     [[0, 1e3], [0, 90], [0, 1e3], [0, 250]],
                     img_background="background/scenario{}-2.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Material Standard Of Living".format(N_SCENARIO),
                     save=False)

        # Human Welfare And Footprint
        classic_plot(world3.nodes["time"].hist,
                     [world3.nodes["hwi"].hist, world3.nodes["hef"].hist],
                     ["HWI", "HEF"],
                     [[0, 1], [0, 4]],
                     img_background="background/scenario{}-3.png".format(N_SCENARIO),
                     grid=1,
                     title="World3 Scenario {} Human Welfare And Footprint".format(N_SCENARIO),
                     save=False)

    # To plot other variables on the same graph (here the life expectancy)
    # multiple_plot(world3.nodes["t"].hist,
    #               [world3.nodes["pop"].hist, world3.nodes["p1"].hist, world3.nodes["p2"].hist, world3.nodes["p3"].hist, world3.nodes["p4"].hist],
    #               "Time (years)", ["POP", "P1", "P2", "P3", "P4"])

    # To plot other variables on different graph (here the life expectancy)
    # single_plot(world3.nodes["t"].hist, [world3.nodes["le"].hist], "Time (years)", ["Life Expectancy"])
