########################################################################################################################
# © Copyright French Civil Aviation Authority
# Author: Julien LEGAVRE (2022)

# julien.legavre@alumni.enac.fr

# This software is a computer program whose purpose is to produce the results
# of the World3 model described in "The Limits to Growth" and
# in "The Limits to Growth".

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

from world3_dynamic import *
from world3_run import VERSION, INITIAL_TIME, FINAL_TIME, TIME_STEP, N_SCENARIO
from math import log

try:
    world3 = World3(VERSION)
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

# Convention: NodeConstant are written in UPPER letters as global constants
#             when NodeFlow, NodeStock and NodeDelay3 are written in lower letters.

# From line 75 to line 1175, it is created the different nodes defined in World3 model.
# From line 1175 to the end, it is defined equations which link these nodes.

######################
# Initial conditions #
######################
TS = NodeConstant("TS", C, val=TIME_STEP, hg=world3)
t = NodeStock("time", val=INITIAL_TIME, hg=world3)
world3.add_equation(lambda x: 1, t, [TS])


#########
# Units #
#########
OY = NodeConstant("OY", C, val=1, hg=world3)
UAGI = NodeConstant("UAGI", C, val=1, hg=world3)
UP = NodeConstant("UP", C, val=1, hg=world3)
GDPU = NodeConstant("GDPU", C, val=1, hg=world3)


######################################
# Variables close to population #
######################################
P1I = NodeConstant("P1I", C, val=6.50e8, hg=world3)
P2I = NodeConstant("P2I", C, val=7.00e8, hg=world3)
P3I = NodeConstant("P3I", C, val=1.90e8, hg=world3)
P4I = NodeConstant("P4I", C, val=6.00e7, hg=world3)

M1 = NodeConstant("M1", CT, val=([20, 0.0567],
                                 [30, 0.0366],
                                 [40, 0.0243],
                                 [50, 0.0155],
                                 [60, 0.0082],
                                 [70, 0.0023],
                                 [80, 0.001]), hg=world3)
M2 = NodeConstant("M2", CT, val=([20, 0.0266],
                                 [30, 0.0171],
                                 [40, 0.011],
                                 [50, 0.0065],
                                 [60, 0.004],
                                 [70, 0.0016],
                                 [80, 0.0008]), hg=world3)
M3 = NodeConstant("M3", CT, val=([20, 0.0562],
                                 [30, 0.0373],
                                 [40, 0.0252],
                                 [50, 0.0171],
                                 [60, 0.0118],
                                 [70, 0.0083],
                                 [80, 0.006]), hg=world3)
M4 = NodeConstant("M4", CT, val=([20, 0.13],
                                 [30, 0.11],
                                 [40, 0.09],
                                 [50, 0.07],
                                 [60, 0.06],
                                 [70, 0.05],
                                 [80, 0.04]), hg=world3)

pop = NodeFlow("pop", hg=world3)

p1 = NodeStock("p1", val=P1I.val, hg=world3)
p2 = NodeStock("p2", val=P2I.val, hg=world3)
p3 = NodeStock("p3", val=P3I.val, hg=world3)
p4 = NodeStock("p4", val=P4I.val, hg=world3)

m1 = NodeFlow("m1", hg=world3)
m2 = NodeFlow("m2", hg=world3)
m3 = NodeFlow("m3", hg=world3)
m4 = NodeFlow("m4", hg=world3)

d1 = NodeFlow("d1", hg=world3)
d2 = NodeFlow("d2", hg=world3)
d3 = NodeFlow("d3", hg=world3)
d4 = NodeFlow("d4", hg=world3)

mat1 = NodeFlow("mat1", hg=world3)
mat2 = NodeFlow("mat2", hg=world3)
mat3 = NodeFlow("mat3", hg=world3)

# Related to death
LEN = NodeConstant("LEN", C, val=28, hg=world3)
HSID = NodeConstant("HSID", C, val=20, hg=world3)
EHSPCI = NodeConstant("EHSPCI", C, val=0, hg=world3)

# LMF values depend on the version used
if world3.version == 1972:
    LMF = NodeConstant("LMF", CT, val=([0, 0],
                                       [1, 1],
                                       [2, 1.2],
                                       [3, 1.3],
                                       [4, 1.35],
                                       [5, 1.4]), hg=world3)
if world3.version == 2003:
    LMF = NodeConstant("LMF", CT, val=([0, 0],
                                       [1, 1],
                                       [2, 1.43],
                                       [3, 1.5],
                                       [4, 1.5],
                                       [5, 1.5]), hg=world3)

HSAPC = NodeConstant("HSAPC", CT, val=([0, 0],
                                       [250, 20],
                                       [500, 50],
                                       [750, 95],
                                       [1000, 140],
                                       [1250, 175],
                                       [1500, 200],
                                       [1750, 220],
                                       [2000, 230]), hg=world3)
LMHS1 = NodeConstant("LMHS1", CT, val=([0, 1],
                                       [20, 1.1],
                                       [40, 1.4],
                                       [60, 1.6],
                                       [80, 1.7],
                                       [100, 1.8]), hg=world3)

# LMHS2 values depend on the version used
if world3.version == 1972:
    LMHS2 = NodeConstant("LMHS2", CT, val=([0, 1],
                                           [20, 1.4],
                                           [40, 1.6],
                                           [60, 1.8],
                                           [80, 1.95],
                                           [100, 2]), hg=world3)
if world3.version == 2003:
    LMHS2 = NodeConstant("LMHS2", CT, val=([0, 1],
                                           [20, 1.5],
                                           [40, 1.9],
                                           [60, 2],
                                           [80, 2],
                                           [100, 2]), hg=world3)

FPU = NodeConstant("FPU", CT, val=([0, 0],
                                   [2e9, 0.2],
                                   [4e9, 0.4],
                                   [6e9, 0.5],
                                   [8e9, 0.58],
                                   [1e10, 0.65],
                                   [1.2e10, 0.72],
                                   [1.4e10, 0.78],
                                   [1.6e10, 0.8]), hg=world3)
CMI = NodeConstant("CMI", CT, val=([0, 0.5],
                                   [200, 0.05],
                                   [400, -0.1],
                                   [600, -0.08],
                                   [800, -0.02],
                                   [1000, 0.05],
                                   [1200, 0.1],
                                   [1400, 0.15],
                                   [1600, 0.2]), hg=world3)
LMP = NodeConstant("LMP", CT, val=([0, 1],
                                   [10, 0.99],
                                   [20, 0.97],
                                   [30, 0.95],
                                   [40, 0.9],
                                   [50, 0.85],
                                   [60, 0.75],
                                   [70, 0.65],
                                   [80, 0.55],
                                   [90, 0.4],
                                   [100, 0.2]), hg=world3)

lmf = NodeFlow("lmf", hg=world3)
hsapc = NodeFlow("hsapc", hg=world3)
lmhs1 = NodeFlow("lmhs1", hg=world3)
lmhs2 = NodeFlow("lmhs2", hg=world3)
fpu = NodeFlow("fpu", hg=world3)
cmi = NodeFlow("cmi", hg=world3)
lmp = NodeFlow("lmp", hg=world3)

d = NodeFlow("d", hg=world3)
cdr = NodeFlow("cdr", hg=world3)
lmhs = NodeFlow("lmhs", hg=world3)
ehspc = NodeStock("ehspc", val=EHSPCI.val, hg=world3)
lmc = NodeFlow("lmc", hg=world3)
le = NodeFlow("le", hg=world3)

# Related to birth
RLT = NodeConstant("RLT", C, val=30, hg=world3)
PET = NodeConstant("PET", C, val=4000, hg=world3)
MTFN = NodeConstant("MTFN", C, val=12, hg=world3)
LPD = NodeConstant("LPD", C, val=20, hg=world3)
AIOPCI = NodeConstant("AIOPCI", C, val=43.3, hg=world3)

# ZPGT values depend on scenario chosen
if 1 <= N_SCENARIO <= 6:
    ZPGT = NodeConstant("ZPGT", C, val=4000, hg=world3)
if 7 <= N_SCENARIO <= 9:
    ZPGT = NodeConstant("ZPGT", C, val=2002, hg=world3)
if N_SCENARIO == 10:
    ZPGT = NodeConstant("ZPGT", C, val=1982, hg=world3)
if N_SCENARIO == 11:
    ZPGT = NodeConstant("ZPGT", C, val=2012, hg=world3)

# DCFSN values depend on the version used
if world3.version == 1972:
    DCFSN = NodeConstant("DCFSN", C, val=4, hg=world3)
if world3.version == 2003:
    DCFSN = NodeConstant("DCFSN", C, val=3.8, hg=world3)

SAD = NodeConstant("SAD", C, val=20, hg=world3)
IEAT = NodeConstant("IEAT", C, val=3, hg=world3)

# FCEST values depend on scenario used
if 1 <= N_SCENARIO <= 6:
    FCEST = NodeConstant("FCEST", C, val=4000, hg=world3)
if 7 <= N_SCENARIO <= 9:
    FCEST = NodeConstant("FCEST", C, val=2002, hg=world3)
if N_SCENARIO == 10:
    FCEST = NodeConstant("FCEST", C, val=1982, hg=world3)
if N_SCENARIO == 11:
    FCEST = NodeConstant("FCEST", C, val=2012, hg=world3)

# FM values depend on the version used
if world3.version == 1972:
    FM = NodeConstant("FM", CT, val=([0, 0],
                                     [10, 0.2],
                                     [20, 0.4],
                                     [30, 0.6],
                                     [40, 0.8],
                                     [50, 0.9],
                                     [60, 1],
                                     [70, 1.05],
                                     [80, 1.1]), hg=world3)
if world3.version == 2003:
    FM = NodeConstant("FM", CT, val=([0, 0],
                                     [10, 0.2],
                                     [20, 0.4],
                                     [30, 0.6],
                                     [40, 0.7],
                                     [50, 0.75],
                                     [60, 0.79],
                                     [70, 0.84],
                                     [80, 0.87]), hg=world3)

CMPLE = NodeConstant("CMPLE", CT, val=([0, 3],
                                       [10, 2.1],
                                       [20, 1.6],
                                       [30, 1.4],
                                       [40, 1.3],
                                       [50, 1.2],
                                       [60, 1.1],
                                       [70, 1.05],
                                       [80, 1]), hg=world3)

# SFSN values depend on the version used
if world3.version == 1972:
    SFSN = NodeConstant("SFSN", CT, val=([0, 1.25],
                                         [200, 1],
                                         [400, 0.9],
                                         [600, 0.8],
                                         [800, 0.75]), hg=world3)
if world3.version == 2003:
    SFSN = NodeConstant("SFSN", CT, val=([0, 1.25],
                                         [200, 0.94],
                                         [400, 0.715],
                                         [600, 0.59],
                                         [800, 0.5]), hg=world3)

FRSN = NodeConstant("FRSN", CT, val=([-0.2, 0.5],
                                     [-0.1, 0.6],
                                     [0, 0.7],
                                     [0.1, 0.85],
                                     [0.2, 1]), hg=world3)
FCE = NodeConstant("FCE", CT, val=([0, 0.75],
                                   [0.5, 0.85],
                                   [1, 0.9],
                                   [1.5, 0.95],
                                   [2, 0.98],
                                   [2.5, 0.99],
                                   [3, 1]), hg=world3)
FSAFC = NodeConstant("FSAFC", CT, val=([0, 0],
                                       [2, 0.005],
                                       [4, 0.015],
                                       [6, 0.025],
                                       [8, 0.03],
                                       [10, 0.035]), hg=world3)
fm = NodeFlow("fm", hg=world3)
fce = NodeFlow("fce", hg=world3)
frsn = NodeFlow("frsn", hg=world3)
sfsn = NodeFlow("sfsn", hg=world3)
cmple = NodeFlow("cmple", hg=world3)
fsafc = NodeFlow("fsafc", hg=world3)

b = NodeFlow("b", hg=world3)
cbr = NodeFlow("cbr", hg=world3)
tf = NodeFlow("tf", hg=world3)
mtf = NodeFlow("mtf", hg=world3)
dtf = NodeFlow("dtf", hg=world3)
ple = NodeDelay3("ple", hg=world3)
dcfs = NodeFlow("dcfs", hg=world3)
diopc = NodeDelay3("diopc", hg=world3)
fie = NodeFlow("fie", hg=world3)
aiopc = NodeStock("aiopc", val=AIOPCI.val, hg=world3)
nfc = NodeFlow("nfc", hg=world3)
fcfpc = NodeDelay3("fcfpc", hg=world3)
fcapc = NodeFlow("fcapc", hg=world3)


################################
# Variables close to capital #
################################
# Related to industry
ICOR1 = NodeConstant("ICOR1", C, val=3, hg=world3)

# ICOR2 values depend on the version used (is a NodeFlow if version is 2003)
if world3.version == 1972:
    ICOR2 = NodeConstant("ICOR2", C, val=3, hg=world3)

ICI = NodeConstant("ICI", C, val=2.1e11, hg=world3)
ALIC1 = NodeConstant("ALIC1", C, val=14, hg=world3)

# ALIC2 values depend on scenario chosen
if 1 <= N_SCENARIO <= 7:
    ALIC2 = NodeConstant("ALIC2", C, val=14, hg=world3)
if 8 <= N_SCENARIO <= 11:
    ALIC2 = NodeConstant("ALIC2", C, val=18, hg=world3)

# IET values depend on scenario chosen
if 1 <= N_SCENARIO <= 7:
    IET = NodeConstant("IET", C, val=4000, hg=world3)
if 8 <= N_SCENARIO <= 9:
    IET = NodeConstant("IET", C, val=2002, hg=world3)
if N_SCENARIO == 10:
    IET = NodeConstant("IET", C, val=1982, hg=world3)
if N_SCENARIO == 11:
    IET = NodeConstant("IET", C, val=2012, hg=world3)

FIOAC1 = NodeConstant("FIOAC1", C, val=0.43, hg=world3)
FIOAC2 = NodeConstant("FIOAC2", C, val=0.43, hg=world3)

# IOPCD values depend on scenario chosen
if 1 <= N_SCENARIO <= 7:
    IOPCD = NodeConstant("IOPCD", C, val=400, hg=world3)
if 8 <= N_SCENARIO <= 11:
    IOPCD = NodeConstant("IOPCD", C, val=350, hg=world3)

# PYEAR values depend on the version used and on scenario chosen
if world3.version == 1972:
    PYEAR = NodeConstant("PYEAR", C, val=1975, hg=world3)
if world3.version == 2003:
    if 1 <= N_SCENARIO <= 2 or N_SCENARIO == 7:
        PYEAR = NodeConstant("PYEAR", C, val=4000, hg=world3)
    if 3 <= N_SCENARIO <= 6 or 8 <= N_SCENARIO <= 9:
        PYEAR = NodeConstant("PYEAR", C, val=2002, hg=world3)
    if N_SCENARIO == 10:
        PYEAR = NodeConstant("PYEAR", C, val=1982, hg=world3)
    if N_SCENARIO == 11:
        PYEAR = NodeConstant("PYEAR", C, val=2012, hg=world3)

FIOACV = NodeConstant("FIOACV", CT, val=([0, 0.3],
                                         [0.2, 0.32],
                                         [0.4, 0.34],
                                         [0.6, 0.36],
                                         [0.8, 0.38],
                                         [1, 0.43],
                                         [1.2, 0.73],
                                         [1.4, 0.77],
                                         [1.6, 0.81],
                                         [1.8, 0.82],
                                         [2, 0.83]), hg=world3)
fioacv = NodeFlow("fioacv", hg=world3)

iopc = NodeFlow("iopc", hg=world3)
io = NodeFlow("io", hg=world3)
icor = NodeFlow("icor", hg=world3)

# ICOR2 values depend on the version used (is a NodeConstant if version is 1972)
if world3.version == 2003:
    icor2 = NodeFlow("icor2", hg=world3)

ic = NodeStock("ic", val=ICI.val, hg=world3)
icdr = NodeFlow("icdr", hg=world3)
alic = NodeFlow("alic", hg=world3)
icir = NodeFlow("icir", hg=world3)
fioai = NodeFlow("fioai", hg=world3)
fioac = NodeFlow("fioac", hg=world3)
fioacc = NodeFlow("fioacc", hg=world3)

# Related to services
SCI = NodeConstant("SCI", C, val=1.44e11, hg=world3)
ALSC1 = NodeConstant("ALSC1", C, val=20, hg=world3)

# ALSC2 values depend on scenario chosen
if 1 <= N_SCENARIO <= 7:
    ALSC2 = NodeConstant("ALSC2", C, val=20, hg=world3)
if 8 <= N_SCENARIO <= 11:
    ALSC2 = NodeConstant("ALSC2", C, val=25, hg=world3)

SCOR1 = NodeConstant("SCOR1", C, val=1, hg=world3)
SCOR2 = NodeConstant("SCOR2", C, val=1, hg=world3)

ISOPC1 = NodeConstant("ISOPC1", CT, val=([0, 40],
                                         [200, 300],
                                         [400, 640],
                                         [600, 1000],
                                         [800, 1220],
                                         [1000, 1450],
                                         [1200, 1650],
                                         [1400, 1800],
                                         [1600, 2000]), hg=world3)
ISOPC2 = NodeConstant("ISOPC2", CT, val=([0, 40],
                                         [200, 300],
                                         [400, 640],
                                         [600, 1000],
                                         [800, 1220],
                                         [1000, 1450],
                                         [1200, 1650],
                                         [1400, 1800],
                                         [1600, 2000]), hg=world3)
FIOAS1 = NodeConstant("FIOAS1", CT, val=([0, 0.3],
                                         [0.5, 0.2],
                                         [1, 0.1],
                                         [1.5, 0.05],
                                         [2, 0]), hg=world3)
FIOAS2 = NodeConstant("FIOAS2", CT, val=([0, 0.3],
                                         [0.5, 0.2],
                                         [1, 0.1],
                                         [1.5, 0.05],
                                         [2, 0]), hg=world3)
isopc1 = NodeFlow("isopc1", hg=world3)
isopc2 = NodeFlow("isopc2", hg=world3)
fioas1 = NodeFlow("fioas1", hg=world3)
fioas2 = NodeFlow("fioas2", hg=world3)

isopc = NodeFlow("isopc", hg=world3)
fioas = NodeFlow("fioas", hg=world3)
scir = NodeFlow("scir", hg=world3)
sc = NodeStock("sc", val=SCI.val, hg=world3)
scdr = NodeFlow("scdr", hg=world3)
alsc = NodeFlow("alsc", hg=world3)
so = NodeFlow("so", hg=world3)
sopc = NodeFlow("sopc", hg=world3)
scor = NodeFlow("scor", hg=world3)

# Related to jobs
LFPF = NodeConstant("LFPF", C, val=0.75, hg=world3)
LUFDT = NodeConstant("LUFDT", C, val=2, hg=world3)
LUFDI = NodeConstant("LUFDI", C, val=1, hg=world3)

JPICU = NodeConstant("JPICU", CT, val=([50, 3.7e-4],
                                       [200, 1.8e-4],
                                       [350, 1.2e-4],
                                       [500, 9e-5],
                                       [650, 7e-5],
                                       [800, 6e-5]), hg=world3)
JPSCU = NodeConstant("JPSCU", CT, val=([50, 1.1e-3],
                                       [200, 6e-4],
                                       [350, 3.5e-4],
                                       [500, 2e-4],
                                       [650, 1.5e-4],
                                       [800, 1.5e-4]), hg=world3)
JPH = NodeConstant("JPH", CT, val=([2, 2],
                                   [6, 0.5],
                                   [10, 0.4],
                                   [14, 0.3],
                                   [18, 0.27],
                                   [22, 0.24],
                                   [26, 0.2],
                                   [30, 0.2]), hg=world3)
CUF = NodeConstant("CUF", CT, val=([1, 1],
                                   [3, 0.9],
                                   [5, 0.7],
                                   [7, 0.3],
                                   [9, 0.1],
                                   [11, 0.1]), hg=world3)
jpicu = NodeFlow("jpicu", hg=world3)
jpscu = NodeFlow("jpscu", hg=world3)
jph = NodeFlow("jph", hg=world3)
cuf = NodeFlow("cuf", hg=world3)

j = NodeFlow("j", hg=world3)
pjis = NodeFlow("pjis", hg=world3)
pjss = NodeFlow("pjss", hg=world3)
pjas = NodeFlow("pjas", hg=world3)
lf = NodeFlow("lf", hg=world3)
luf = NodeFlow("luf", hg=world3)
lufd = NodeStock("lufd", val=LUFDI.val, hg=world3)


##################################
# Variables close to agriculture #
##################################
# Loop 1
PALT = NodeConstant("PALT", C, val=3.2e9, hg=world3)
ALI = NodeConstant("ALI", C, val=0.9e9, hg=world3)
PALI = NodeConstant("PALI", C, val=2.3e9, hg=world3)
LFH = NodeConstant("LFH", C, val=0.7, hg=world3)
PL = NodeConstant("PL", C, val=0.1, hg=world3)

IFPC1 = NodeConstant("IFPC1", CT, val=([0, 230],
                                       [200, 480],
                                       [400, 690],
                                       [600, 850],
                                       [800, 970],
                                       [1000, 1070],
                                       [1200, 1150],
                                       [1400, 1210],
                                       [1600, 1250]), hg=world3)
IFPC2 = NodeConstant("IFPC2", CT, val=([0, 230],
                                       [200, 480],
                                       [400, 690],
                                       [600, 850],
                                       [800, 970],
                                       [1000, 1070],
                                       [1200, 1150],
                                       [1400, 1210],
                                       [1600, 1250]), hg=world3)
FIOAA1 = NodeConstant("FIOAA1", CT, val=([0, 0.4],
                                         [0.5, 0.2],
                                         [1, 0.1],
                                         [1.5, 0.025],
                                         [2, 0],
                                         [2.5, 0]), hg=world3)
FIOAA2 = NodeConstant("FIOAA2", CT, val=([0, 0.4],
                                         [0.5, 0.2],
                                         [1, 0.1],
                                         [1.5, 0.025],
                                         [2, 0],
                                         [2.5, 0]), hg=world3)
DCPH = NodeConstant("DCPH", CT, val=([0, 100000],
                                     [0.1, 7400],
                                     [0.2, 5200],
                                     [0.3, 3500],
                                     [0.4, 2400],
                                     [0.5, 1500],
                                     [0.6, 750],
                                     [0.7, 300],
                                     [0.8, 150],
                                     [0.9, 75],
                                     [1, 50]), hg=world3)
ifpc1 = NodeFlow("ifpc1", hg=world3)
ifpc2 = NodeFlow("ifpc2", hg=world3)
fioaa1 = NodeFlow("fioaa1", hg=world3)
fioaa2 = NodeFlow("fioaa2", hg=world3)
dcph = NodeFlow("dcph", hg=world3)

lfc = NodeFlow("lfc", hg=world3)
al = NodeStock("al", val=ALI.val, hg=world3)
pal = NodeStock("pal", val=PALI.val, hg=world3)
f = NodeFlow("f", hg=world3)
fpc = NodeFlow("fpc", hg=world3)
ifpc = NodeFlow("ifpc", hg=world3)
tai = NodeFlow("tai", hg=world3)
fioaa = NodeFlow("fioaa", hg=world3)
ldr = NodeFlow("ldr", hg=world3)

# Loop 2
ALAI1 = NodeConstant("ALAI1", C, val=2, hg=world3)

# ALAI2 values depend on scenario chosen
if 1 <= N_SCENARIO <= 7:
    ALAI2 = NodeConstant("ALAI2", C, val=2, hg=world3)
if 8 <= N_SCENARIO <= 11:
    ALAI2 = NodeConstant("ALAI2", C, val=2.5, hg=world3)

AII = NodeConstant("AII", C, val=5e9, hg=world3)
LYF1 = NodeConstant("LYF1", C, val=1, hg=world3)

# LYF2 values depend on the version used (is a NodeDelay3 if version is 2003)
if world3.version == 1972:
    LYF2 = NodeConstant("LYF2", C, val=1, hg=world3)

IO70 = NodeConstant("IO70", C, val=7.9e11, hg=world3)
SD = NodeConstant("SD", C, val=0.07, hg=world3)

# TDD values depend on the version used (not used in 1972)
if world3.version == 2003:
    TDD = NodeConstant("TDD", C, val=20, hg=world3)

# LYMC values depend on the version used
if world3.version == 1972:
    LYMC = NodeConstant("LYMC", CT, val=([0, 1],
                                         [40, 3],
                                         [80, 3.8],
                                         [120, 4.4],
                                         [160, 4.9],
                                         [200, 5.4],
                                         [240, 5.7],
                                         [280, 6],
                                         [320, 6.3],
                                         [360, 6.6],
                                         [400, 6.9],
                                         [440, 7.2],
                                         [480, 7.4],
                                         [520, 7.6],
                                         [560, 7.8],
                                         [600, 8],
                                         [640, 8.2],
                                         [680, 8.4],
                                         [720, 8.6],
                                         [760, 8.8],
                                         [800, 9],
                                         [840, 9.2],
                                         [880, 9.4],
                                         [920, 9.6],
                                         [960, 9.8],
                                         [1000, 10]), hg=world3)
if world3.version == 2003:
    LYMC = NodeConstant("LYMC", CT, val=([0, 1],
                                         [40, 3],
                                         [80, 4.5],
                                         [120, 5],
                                         [160, 5.3],
                                         [200, 5.6],
                                         [240, 5.9],
                                         [280, 6.1],
                                         [320, 6.35],
                                         [360, 6.6],
                                         [400, 6.9],
                                         [440, 7.2],
                                         [480, 7.4],
                                         [520, 7.6],
                                         [560, 7.8],
                                         [600, 8],
                                         [640, 8.2],
                                         [680, 8.4],
                                         [720, 8.6],
                                         [760, 8.8],
                                         [800, 9],
                                         [840, 9.2],
                                         [880, 9.4],
                                         [920, 9.6],
                                         [960, 9.8],
                                         [1000, 10]), hg=world3)

LYMAP1 = NodeConstant("LYMAP1", CT, val=([0, 1],
                                         [10, 1],
                                         [20, 0.7],
                                         [30, 0.4]), hg=world3)

# LYMAP2 values depend on the version used
if world3.version == 1972:
    LYMAP2 = NodeConstant("LYMAP2", CT, val=([0, 1],
                                             [10, 1],
                                             [20, 0.7],
                                             [30, 0.4]), hg=world3)
if world3.version == 2003:
    LYMAP2 = NodeConstant("LYMAP2", CT, val=([0, 1],
                                             [10, 1],
                                             [20, 0.98],
                                             [30, 0.95]), hg=world3)

FIALD = NodeConstant("FIALD", CT, val=([0, 0],
                                       [0.25, 0.05],
                                       [0.5, 0.15],
                                       [0.75, 0.3],
                                       [1, 0.5],
                                       [1.25, 0.7],
                                       [1.5, 0.85],
                                       [1.75, 0.95],
                                       [2, 1]), hg=world3)
MLYMC = NodeConstant("MLYMC", CT, val=([0, 0.075],
                                       [40, 0.03],
                                       [80, 0.015],
                                       [120, 0.011],
                                       [160, 0.009],
                                       [200, 0.008],
                                       [240, 0.007],
                                       [280, 0.006],
                                       [320, 0.005],
                                       [360, 0.005],
                                       [400, 0.005],
                                       [440, 0.005],
                                       [480, 0.005],
                                       [520, 0.005],
                                       [560, 0.005],
                                       [600, 0.005]), hg=world3)
lymc = NodeFlow("lymc", hg=world3)
lymap = NodeFlow("lymap", hg=world3)
lymap1 = NodeFlow("lymap1", hg=world3)
lymap2 = NodeFlow("lymap2", hg=world3)
fiald = NodeFlow("fiald", hg=world3)
mlymc = NodeFlow("mlymc", hg=world3)

cai = NodeFlow("cai", hg=world3)
ai = NodeStock("ai", val=AII.val, hg=world3)
alai = NodeFlow("alai", hg=world3)
aiph = NodeFlow("aiph", hg=world3)
ly = NodeFlow("ly", hg=world3)
lyf = NodeFlow("lyf", hg=world3)

# lyf2 values depend on the version used (is a NodeConstant if version is 1972)
if world3.version == 2003:
    lyf2 = NodeDelay3("lyf2", hg=world3)

mpld = NodeFlow("mpld", hg=world3)
mpai = NodeFlow("mpai", hg=world3)

# Loop 3
# ALLN values depend on the version used
if world3.version == 1972:
    ALLN = NodeConstant("ALLN", C, val=6000, hg=world3)
if world3.version == 2003:
    ALLN = NodeConstant("ALLN", C, val=1000, hg=world3)

UILDT = NodeConstant("UILDT", C, val=10, hg=world3)
UILI = NodeConstant("UILI", C, val=8.2e6, hg=world3)

# LLMYTM values depend on scenario chosen
if 1 <= N_SCENARIO <= 4 or 7 <= N_SCENARIO <= 8:
    LLMYTM = NodeConstant("LLMYTM", C, val=4000, hg=world3)
if 5 <= N_SCENARIO <= 6 or N_SCENARIO == 9:
    LLMYTM = NodeConstant("LLMYTM", C, val=2002, hg=world3)
if N_SCENARIO == 10:
    LLMYTM = NodeConstant("LLMYTM", C, val=1982, hg=world3)
if N_SCENARIO == 11:
    LLMYTM = NodeConstant("LLMYTM", C, val=2012, hg=world3)

LLMY1 = NodeConstant("LLMY1", CT, val=([0, 1.2],
                                       [1, 1],
                                       [2, 0.63],
                                       [3, 0.36],
                                       [4, 0.16],
                                       [5, 0.055],
                                       [6, 0.04],
                                       [7, 0.025],
                                       [8, 0.015],
                                       [9, 0.01]), hg=world3)

# LLMY2 values depend on the version used
if world3.version == 1972:
    LLMY2 = NodeConstant("LLMY2", CT, val=([0, 1.2],
                                           [1, 1],
                                           [2, 0.63],
                                           [3, 0.36],
                                           [4, 0.16],
                                           [5, 0.055],
                                           [6, 0.04],
                                           [7, 0.025],
                                           [8, 0.015],
                                           [9, 0.01]), hg=world3)
if world3.version == 2003:
    LLMY2 = NodeConstant("LLMY2", CT, val=([0, 1.2],
                                           [1, 1],
                                           [2, 0.63],
                                           [3, 0.36],
                                           [4, 0.29],
                                           [5, 0.26],
                                           [6, 0.24],
                                           [7, 0.22],
                                           [8, 0.21],
                                           [9, 0.2]), hg=world3)

UILPC = NodeConstant("UILPC", CT, val=([0, 0.005],
                                       [200, 0.008],
                                       [400, 0.015],
                                       [600, 0.025],
                                       [800, 0.04],
                                       [1000, 0.055],
                                       [1200, 0.07],
                                       [1400, 0.08],
                                       [1600, 0.09]), hg=world3)
llmy = NodeFlow("llmy", hg=world3)
llmy1 = NodeFlow("llmy1", hg=world3)
llmy2 = NodeFlow("llmy2", hg=world3)
uilpc = NodeFlow("uilpc", hg=world3)

all = NodeFlow("all", hg=world3)
ler = NodeFlow("ler", hg=world3)
uilr = NodeFlow("uilr", hg=world3)
lrui = NodeFlow("lrui", hg=world3)
uil = NodeStock("uil", val=UILI.val, hg=world3)

# Loop 4
LFERTI = NodeConstant("LFERTI", C, val=600, hg=world3)

LFDR = NodeConstant("LFDR", CT, val=([0, 0],
                                     [10, 0.1],
                                     [20, 0.3],
                                     [30, 0.5]), hg=world3)
lfdr = NodeFlow("lfdr", hg=world3)

lfert = NodeStock("lfert", val=LFERTI.val, hg=world3)
lfd = NodeFlow("lfd", hg=world3)

# Loop 5
ILF = NodeConstant("ILF", C, val=600, hg=world3)
SFPC = NodeConstant("SFPC", C, val=230, hg=world3)
FSPD = NodeConstant("FSPD", C, val=2, hg=world3)
PFRI = NodeConstant("PFRI", C, val=1, hg=world3)

# DFR values depend on the version used (not used in 1972)
if world3.version == 2003:
    DFR = NodeConstant("DFR", C, val=2, hg=world3)

LFRT = NodeConstant("LFRT", CT, val=([0, 20],
                                     [0.02, 13],
                                     [0.04, 8],
                                     [0.06, 4],
                                     [0.08, 2],
                                     [0.1, 2]), hg=world3)
FALM = NodeConstant("FALM", CT, val=([0, 0],
                                     [1, 0.04],
                                     [2, 0.07],
                                     [3, 0.09],
                                     [4, 0.1]), hg=world3)

# LYCM values depend on the version used and on scenario chosen (not used in 1972)
# COYM values depend on the version used (not used in 1972)
if world3.version == 2003:
    if 1 <= N_SCENARIO <= 3 or 7 <= N_SCENARIO <= 8:
        LYCM = NodeConstant("LYCM", CT, val=([0, 0],
                                             [1, 0]), hg=world3)
    if 4 <= N_SCENARIO <= 6 or 9 <= N_SCENARIO <= 11:
        LYCM = NodeConstant("LYCM", CT, val=([0, 0],
                                             [1, 0.04]), hg=world3)
    COYM = NodeConstant("COYM", CT, val=([1, 1],
                                         [1.2, 1.05],
                                         [1.4, 1.12],
                                         [1.6, 1.25],
                                         [1.8, 1.35],
                                         [2, 1.5]), hg=world3)

    lycm = NodeFlow("lycm", hg=world3)
    coym = NodeFlow("coym", hg=world3)

lfrt = NodeFlow("lfrt", hg=world3)
falm = NodeFlow("falm", hg=world3)

lfr = NodeFlow("lfr", hg=world3)
fr = NodeFlow("fr", hg=world3)
pfr = NodeStock("pfr", val=PFRI.val, hg=world3)

# lytd and lytdr values depend on the version used (not used in 1972)
if world3.version == 2003:
    lytd = NodeStock("lytd", val=LYF1.val, hg=world3)
    lytdr = NodeFlow("lytdr", hg=world3)

################################
# Variables close to resources #
################################
# NRI values depend on scenario chosen
if N_SCENARIO == 1:
    NRI = NodeConstant("NRI", C, val=1e12, hg=world3)
if N_SCENARIO > 1:
    NRI = NodeConstant("NRI", C, val=2e12, hg=world3)

NRUF1 = NodeConstant("NRUFI", C, val=1, hg=world3)

# NRUF2 values depend on the version used (is a NodeDelay3 if version is 2003)
if world3.version == 1972:
    NRUF2 = NodeConstant("NRUF2", C, val=1, hg=world3)

# FCAORTM values depend on scenario chosen
if N_SCENARIO == 1:
    FCAORTM = NodeConstant("FCAORTM", C, val=4000, hg=world3)
if 2 <= N_SCENARIO <= 9:
    FCAORTM = NodeConstant("FCAORTM", C, val=2002, hg=world3)
if N_SCENARIO == 10:
    FCAORTM = NodeConstant("FCAORTM", C, val=1982, hg=world3)
if N_SCENARIO == 11:
    FCAORTM = NodeConstant("FCAORTM", C, val=2012, hg=world3)

# DNRUR values depend on the version used (not used in 1972)
if world3.version == 2003:
    DNRUR = NodeConstant("DNRUR", C, val=4.8e9, hg=world3)

# PCRUM values depend on the version used
if world3.version == 1972:
    PCRUM = NodeConstant("PCRUM", CT, val=([0, 0],
                                           [200, 0.85],
                                           [400, 2.6],
                                           [600, 4.4],
                                           [800, 5.4],
                                           [1000, 6.2],
                                           [1200, 6.8],
                                           [1400, 7],
                                           [1600, 7]), hg=world3)
if world3.version == 2003:
    PCRUM = NodeConstant("PCRUM", CT, val=([0, 0],
                                           [200, 0.85],
                                           [400, 2.6],
                                           [600, 3.4],
                                           [800, 3.8],
                                           [1000, 4.1],
                                           [1200, 4.4],
                                           [1400, 4.7],
                                           [1600, 5]), hg=world3)

FCAOR1 = NodeConstant("FCAOR1", CT, val=([0, 1],
                                         [0.1, 0.9],
                                         [0.2, 0.7],
                                         [0.3, 0.5],
                                         [0.4, 0.2],
                                         [0.5, 0.1],
                                         [0.6, 0.05],
                                         [0.7, 0.05],
                                         [0.8, 0.05],
                                         [0.9, 0.05],
                                         [1, 0.05]), hg=world3)

# FCAOR2 values depend on the version used and on scenario chosen
if world3.version == 1972:
    FCAOR2 = NodeConstant("FCAOR2", CT, val=([0, 1],
                                             [0.1, 0.9],
                                             [0.2, 0.7],
                                             [0.3, 0.5],
                                             [0.4, 0.2],
                                             [0.5, 0.1],
                                             [0.6, 0.05],
                                             [0.7, 0.05],
                                             [0.8, 0.05],
                                             [0.9, 0.05],
                                             [1, 0.05]), hg=world3)
if world3.version == 2003:
    if N_SCENARIO > 1:
        FCAOR2 = NodeConstant("FCAOR2", CT, val=([0, 1],
                                                 [0.1, 0.1],
                                                 [0.2, 0.05],
                                                 [0.3, 0.05],
                                                 [0.4, 0.05],
                                                 [0.5, 0.05],
                                                 [0.6, 0.05],
                                                 [0.7, 0.05],
                                                 [0.8, 0.05],
                                                 [0.9, 0.05],
                                                 [1, 0.05]), hg=world3)
    if N_SCENARIO == 1:
        FCAOR2 = NodeConstant("FCAOR2", CT, val=([0, 1],
                                                 [0.1, 0.2],
                                                 [0.2, 0.1],
                                                 [0.3, 0.05],
                                                 [0.4, 0.05],
                                                 [0.5, 0.05],
                                                 [0.6, 0.05],
                                                 [0.7, 0.05],
                                                 [0.8, 0.05],
                                                 [0.9, 0.05],
                                                 [1, 0.05]), hg=world3)

# NRCM values depend on the version used and on scenario chosen (not used in 1972)
# ICOR2T values depend on the version used (not used in 1972)
if world3.version == 2003:
    if 1 <= N_SCENARIO <= 5 or 7 <= N_SCENARIO <= 8:
        NRCM = NodeConstant("NRCM", CT, val=([-1, 0],
                                             [0, 0]), hg=world3)
    if N_SCENARIO == 6 or 9 <= N_SCENARIO <= 11:
        NRCM = NodeConstant("NRCM", CT, val=([-1, -0.04],
                                             [0, 0]), hg=world3)
    ICOR2T = NodeConstant("ICOR2T", CT, val=([0, 3.75],
                                             [0.1, 3.6],
                                             [0.2, 3.47],
                                             [0.3, 3.36],
                                             [0.4, 3.25],
                                             [0.5, 3.16],
                                             [0.6, 3.1],
                                             [0.7, 3.06],
                                             [0.8, 3.02],
                                             [0.9, 3.01],
                                             [1, 3]), hg=world3)

    nrcm = NodeFlow("nrcm", hg=world3)
    icor2t = NodeFlow("icor2t", hg=world3)

pcrum = NodeFlow("pcrum", hg=world3)
fcaor = NodeFlow("fcaor", hg=world3)
fcaor1 = NodeFlow("fcaor1", hg=world3)
fcaor2 = NodeFlow("fcaor2", hg=world3)

nr = NodeStock("nr", val=NRI.val, hg=world3)
nrur = NodeFlow("nrur", hg=world3)
nruf = NodeFlow("nruf", hg=world3)

# nruf2 values depend on the version used (is a NodeConstant if version is 1972)
if world3.version == 2003:
    nruf2 = NodeDelay3("nruf2", hg=world3)

nrfr = NodeFlow("nrfr", hg=world3)

# nrtd and nrate values depend on the version used (not used in 1972)
if world3.version == 2003:
    nrtd = NodeStock("nrtd", val=NRUF1.val, hg=world3)
    nrate = NodeFlow("nrate", hg=world3)


################################
# Variables close to pollution #
################################
PPGF1 = NodeConstant("PPGF1", C, val=1, hg=world3)

# PPGF2 values depend on the version used (is a NodeDelay3 if version is 2003)
if world3.version == 1972:
    PPGF2 = NodeConstant("PPGF2", C, val=1, hg=world3)

FRPM = NodeConstant("FRPM", C, val=0.02, hg=world3)
IMEF = NodeConstant("IMEF", C, val=0.1, hg=world3)
IMTI = NodeConstant("IMTI", C, val=10, hg=world3)
FIPM = NodeConstant("FIPM", C, val=0.001, hg=world3)
AMTI = NodeConstant("AMTI", C, val=1, hg=world3)
PPTD = NodeConstant("PPTD", C, val=20, hg=world3)
PPOLI = NodeConstant("PPOLI", C, val=2.5e7, hg=world3)
PPOL70 = NodeConstant("PPOLI70", C, val=1.36e8, hg=world3)
AHL70 = NodeConstant("AHL70", C, val=1.5, hg=world3)

# DPOLX values depend on the version used (not used in 1972)
if world3.version == 2003:
    DPOLX = NodeConstant("DPOLX", C, val=1.2, hg=world3)

AHLM = NodeConstant("AHLM", CT, val=([1, 1],
                                     [251, 11],
                                     [501, 21],
                                     [751, 31],
                                     [1001, 41]), hg=world3)

# POLGFM values depend on the version used and on scenario chosen (not used in 1972)
# COPM values depend on the version used (not used in 1972)
if world3.version == 2003:
    if 1 <= N_SCENARIO <= 2 or 7 <= N_SCENARIO <= 8:
        POLGFM = NodeConstant("POLGFM", CT, val=([-1, 0],
                                                 [0, 0]), hg=world3)
    if 3 <= N_SCENARIO <= 6 or 9 <= N_SCENARIO <= 11:
        POLGFM = NodeConstant("POLGFM", CT, val=([-1, -0.04],
                                                 [0, 0]), hg=world3)
    COPM = NodeConstant("COPM", CT, val=([0, 1.25],
                                         [0.1, 1.2],
                                         [0.2, 1.15],
                                         [0.3, 1.11],
                                         [0.4, 1.08],
                                         [0.5, 1.05],
                                         [0.6, 1.03],
                                         [0.7, 1.02],
                                         [0.8, 1.01],
                                         [0.9, 1],
                                         [1, 1]), hg=world3)

    polgfm = NodeFlow("polgfm", hg=world3)
    copm = NodeFlow("copm", hg=world3)

ahlm = NodeFlow("ahlm", hg=world3)
ppgr = NodeFlow("ppgr", hg=world3)
ppgf = NodeFlow("ppgf", hg=world3)

# ppgf2 values depend on the version used (is a NodeConstant if version is 1972)
if world3.version == 2003:
    ppgf2 = NodeDelay3("ppgf2", hg=world3)

ppgio = NodeFlow("ppgio", hg=world3)
ppgao = NodeFlow("ppgao", hg=world3)
ppapr = NodeDelay3("ppapr", hg=world3)
ppol = NodeStock("ppol", val=PPOLI.val, hg=world3)
ppolx = NodeFlow("ppolx", hg=world3)
ppasr = NodeFlow("ppasr", hg=world3)
ahl = NodeFlow("ahl", hg=world3)

# ptd and ptdr values depend on the version used (not used in 1972)
if world3.version == 2003:
    ptd = NodeStock("ptd", val=PPGF1.val, hg=world3)
    ptdr = NodeFlow("ptdr", hg=world3)


###########
# Indexes #
###########
POF = NodeConstant("POF", C, val=0.22, hg=world3)
HUP = NodeConstant("HUP", C, val=4, hg=world3)
RHGDP = NodeConstant("RHGDP", C, val=9508, hg=world3)
RLGDP = NodeConstant("RLGDP", C, val=24, hg=world3)
TL = NodeConstant("TL", C, val=1.91, hg=world3)
GHAH = NodeConstant("GHAH", C, val=1e9, hg=world3)

LEI = NodeConstant("LEI", CT, val=([25, 0],
                                   [35, 0.16],
                                   [45, 0.33],
                                   [55, 0.5],
                                   [65, 0.67],
                                   [75, 0.84],
                                   [85, 1]), hg=world3)
EI = NodeConstant("EI", CT, val=([0, 0],
                                 [1000, 0.81],
                                 [2000, 0.88],
                                 [3000, 0.92],
                                 [4000, 0.95],
                                 [5000, 0.98],
                                 [6000, 0.99],
                                 [7000, 1]), hg=world3)
GDPPC = NodeConstant("GDPPC", CT, val=([0, 120],
                                       [200, 600],
                                       [400, 1200],
                                       [600, 1800],
                                       [800, 2500],
                                       [1000, 3200]), hg=world3)
foa = NodeFlow("foa", hg=world3)
foi = NodeFlow("foi", hg=world3)
fos = NodeFlow("fos", hg=world3)

resint = NodeFlow("resint", hg=world3)
plinid = NodeFlow("plinid", hg=world3)
cio = NodeFlow("cio", hg=world3)
ciopc = NodeFlow("ciopc", hg=world3)

lei = NodeFlow("lei", hg=world3)
ei = NodeFlow("ei", hg=world3)
gdppc = NodeFlow("gdppc", hg=world3)

hwi = NodeFlow("hwi", hg=world3)
gdpi = NodeFlow("gdpi", hg=world3)
hef = NodeFlow("hef", hg=world3)
algha = NodeFlow("algha", hg=world3)
alggha = NodeFlow("alggha", hg=world3)
ulgha = NodeFlow("ulgha", hg=world3)



#####################################
# Basic functions used in equations #
#####################################
def nodes_mltpld(*l):
    out = l[0]
    for x in l[1:]:
        out = out * x
    return out

def nodes_sum(*l):
    return sum([i for i in l])

def nodes_dif(x, y): return x - y

def nodes_div(x, y): return x / y

def clip(c1, c2, ts, t):
    if t <= ts : return c1
    else : return c2

def f_tab(tab, x):
    if tab[0][0] > x:
        return tab[0][1]
    if tab[-1][0] < x:
        return tab[-1][1]
    else:
        i = 0
        while i < len(tab):
            if tab[i][0] <= x <= tab[i+1][0]:
                coeff = (tab[i+1][1]-tab[i][1]) / (tab[i+1][0]-tab[i][0])
                return tab[i][1] + coeff * (x-tab[i][0])
            i += 1

def f_tab_div(x, y, z): return f_tab(x, y/z)

def f_tab_dif(x, y, z): return f_tab(x, y - z)


###########################
# Equations on population #
###########################

# Functions which are not defined in basic ones
def p1_evo(b, d1, mat1): return b - d1 - mat1
def p2_evo(mat1, d2, mat2): return mat1 - d2 - mat2
def p3_evo(mat2, d3, mat3): return mat2 - d3 - mat3
def f_mat1(p1, m1): return p1 * (1 - m1) / 15
def f_mat2(p2, m2): return p2 * (1 - m2) / 30
def f_mat3(p3, m3): return p3 * (1 - m3) / 20


def f_cdr(d, pop): return 1000 * d / pop
def f_ehspc(hsapc, ehspc, hsid): return (hsapc - ehspc) / hsid
def f_lmhs(lmhs1, lmhs2, t): return clip(lmhs1, lmhs2, 1940, t)
def f_lmc(cmi, fpu): return 1 - cmi * fpu


def f_b(d, pet, tf, p2, rlt, t): return clip(d, 0.5 * tf * p2 / rlt, t, pet)
def f_cbr(b, pop): return 1000 * b / pop
def f_tf(mtf, fce, dtf): return min(mtf, mtf * (1 - fce) + dtf * fce)
def f_dcfs(dcfsn, frsn, sfsn, t, zpgt): return clip(2, dcfsn * frsn * sfsn, t, zpgt)
def f_fie(iopc, aiopc): return (iopc - aiopc) / aiopc
def f_aiopc(iopc, aiopc, ieat): return (iopc - aiopc) / ieat
def f_nfc(mtf, dtf): return mtf / dtf - 1
def f_fce(fce, fcfpc, gdpu, t, fcest): return clip(1, f_tab_div(fce, fcfpc, gdpu), t, fcest)


# Creation of equations

# Population dynamics
world3.add_equation(nodes_sum, pop, [p1, p2, p3, p4])

world3.add_equation(p1_evo, p1, [b, d1, mat1])
world3.add_equation(nodes_mltpld, d1, [p1, m1])
world3.add_equation(f_tab_div, m1, [M1, le, OY])
world3.add_equation(f_mat1, mat1, [p1, m1])

world3.add_equation(p2_evo, p2, [mat1, d2, mat2])
world3.add_equation(nodes_mltpld, d2, [p2, m2])
world3.add_equation(f_tab_div, m2, [M2, le, OY])
world3.add_equation(f_mat2, mat2, [p2, m2])

world3.add_equation(p3_evo, p3, [mat2, d3, mat3])
world3.add_equation(nodes_mltpld, d3, [p3, m3])
world3.add_equation(f_tab_div, m3, [M3, le, OY])
world3.add_equation(f_mat3, mat3, [p3, m3])

world3.add_equation(nodes_dif, p4, [mat3, d4])
world3.add_equation(nodes_mltpld, d4, [p4, m4])
world3.add_equation(f_tab_div, m4, [M4, le, OY])

# Death
world3.add_equation(nodes_sum, d, [d1, d2, d3, d4])
world3.add_equation(f_cdr, cdr, [d, pop])

world3.add_equation(nodes_mltpld, le, [LEN, lmf, lmhs, lmp, lmc])
world3.add_equation(f_tab_div, lmf, [LMF, fpc, SFPC])

world3.add_equation(f_tab_div, hsapc, [HSAPC, sopc, GDPU])
world3.add_equation(f_ehspc, ehspc, [hsapc, ehspc, HSID])
world3.add_equation(f_lmhs, lmhs, [lmhs1, lmhs2, t])
world3.add_equation(f_tab_div, lmhs1, [LMHS1, ehspc, GDPU])
world3.add_equation(f_tab_div, lmhs2, [LMHS2, ehspc, GDPU])

world3.add_equation(f_tab_div, fpu, [FPU, pop, UP])
world3.add_equation(f_tab_div, cmi, [CMI, iopc, GDPU])
world3.add_equation(f_lmc, lmc, [cmi, fpu])
world3.add_equation(f_tab, lmp, [LMP, ppolx])

# Birth
world3.add_equation(f_b, b, [d, PET, tf, p2, RLT, t])
world3.add_equation(f_cbr, cbr, [b, pop])

world3.add_equation(f_tf, tf, [mtf, fce, dtf])
world3.add_equation(nodes_mltpld, mtf, [MTFN, fm])
world3.add_equation(f_tab_div, fm, [FM, le, OY])
world3.add_equation(nodes_mltpld, dtf, [dcfs, cmple])

world3.add_equation(f_tab_div, cmple, [CMPLE, ple, OY])
world3.add_equation(ple.f_delayinit, ple, [le, LPD])

world3.add_equation(f_dcfs, dcfs, [DCFSN, frsn, sfsn, t, ZPGT])
world3.add_equation(f_tab_div, sfsn, [SFSN, diopc, GDPU])

world3.add_equation(diopc.f_delayinit, diopc, [iopc, SAD])

world3.add_equation(f_tab, frsn, [FRSN, fie])
world3.add_equation(f_fie, fie, [iopc, aiopc])

world3.add_equation(f_aiopc, aiopc, [iopc, aiopc, IEAT])

world3.add_equation(f_nfc, nfc, [mtf, dtf])
world3.add_equation(f_fce, fce, [FCE, fcfpc, GDPU, t, FCEST])
world3.add_equation(fcfpc.f_delayinit, fcfpc, [fcapc, HSID])
world3.add_equation(nodes_mltpld, fcapc, [fsafc, sopc])
world3.add_equation(f_tab, fsafc, [FSAFC, nfc])


########################
# Equations on capital #
########################

# Functions which are not defined in basic ones
def f_io(ic, fcaor, cuf, icor): return (ic * (1 - fcaor) * cuf) / icor
def f_fioai(fioaa, fioas, fioac): return 1 - fioaa - fioas - fioac


def f_so(sc, cuf, scor): return sc * cuf / scor


def f_lf(p2, p3, lfpf): return (p2 + p3) * lfpf
def f_lufd(luf, lufd, lufdt): return (luf - lufd) / lufdt


# Creation of equations

# Industrial
world3.add_equation(nodes_div, iopc, [io, pop])
world3.add_equation(f_io, io, [ic, fcaor, cuf, icor])

if world3.version == 1972:
    world3.add_equation(clip, icor, [ICOR2, ICOR1, t, PYEAR])
if world3.version == 2003:
    world3.add_equation(clip, icor, [icor2, ICOR1, t, PYEAR])

world3.add_equation(nodes_dif, ic, [icir, icdr])
world3.add_equation(nodes_div, icdr, [ic, alic])
world3.add_equation(clip, alic, [ALIC2, ALIC1, t, PYEAR])
world3.add_equation(nodes_mltpld, icir, [io, fioai])

world3.add_equation(f_fioai, fioai, [fioaa, fioas, fioac])
world3.add_equation(clip, fioac, [fioacv, fioacc, t, IET])
world3.add_equation(clip, fioacc, [FIOAC2, FIOAC1, t, PYEAR])
world3.add_equation(f_tab_div, fioacv, [FIOACV, iopc, IOPCD])

if world3.version == 2003:
    world3.add_equation(nodes_mltpld, icor2, [icor2t, coym, copm])

# Services
world3.add_equation(clip, isopc, [isopc2, isopc1, t, PYEAR])
world3.add_equation(f_tab_div, isopc1, [ISOPC1, iopc, GDPU])
world3.add_equation(f_tab_div, isopc2, [ISOPC2, iopc, GDPU])

world3.add_equation(clip, fioas, [fioas2, fioas1, t, PYEAR])
world3.add_equation(f_tab_div, fioas1, [FIOAS1, sopc, isopc])
world3.add_equation(f_tab_div, fioas2, [FIOAS2, sopc, isopc])

world3.add_equation(nodes_mltpld, scir, [io, fioas])
world3.add_equation(nodes_dif, sc, [scir, scdr])
world3.add_equation(nodes_div, scdr, [sc, alsc])
world3.add_equation(clip, alsc, [ALSC2, ALSC1, t, PYEAR])

world3.add_equation(f_so, so, [sc, cuf, scor])
world3.add_equation(nodes_div, sopc, [so, pop])
world3.add_equation(clip, scor, [SCOR2, SCOR1, t, PYEAR])

# Jobs
world3.add_equation(nodes_sum, j, [pjis, pjas, pjss])
world3.add_equation(nodes_mltpld, pjis, [ic, jpicu])
world3.add_equation(f_tab_div, jpicu, [JPICU, iopc, GDPU])
world3.add_equation(nodes_mltpld, pjss, [sc, jpscu])
world3.add_equation(f_tab_div, jpscu, [JPSCU, sopc, GDPU])
world3.add_equation(nodes_mltpld, pjas, [jph, al])
world3.add_equation(f_tab_div, jph, [JPH, aiph, UAGI])

world3.add_equation(f_lf, lf, [p2, p3, LFPF])
world3.add_equation(nodes_div, luf, [j, lf])
world3.add_equation(f_lufd, lufd, [luf, lufd, LUFDT])
world3.add_equation(f_tab, cuf, [CUF, lufd])


############################
# Equations on agriculture #
############################

# Functions which are not defined in basic ones
def f_al(ldr, ler, lrui): return ldr - ler - lrui
def f_pal(ldr): return - ldr
def f_f(ly, al, lfh, pl): return ly * al * lfh * (1 - pl)
def f_ldr(tai, fiald, dcph): return tai * fiald / dcph


def f_cai(tai, fiald): return tai * (1 - fiald)
def f_ai(cai, ai, alai): return (cai - ai) / alai
def f_aiph(ai, falm, al): return ai * (1 - falm) / al
def f_mpld(ly, dcph, sd): return ly / (dcph * sd)
def f_mpai(alai, ly, mlymc, lymc): return alai * ly * mlymc / lymc


def f_llmy(llmy2, llmy1, llmytm, oy, t):
    return clip(0.95 ** ((t - llmytm) / oy) * llmy1 + (1 - 0.95 ** ((t - llmytm) / oy)) * llmy2, llmy1, t, llmytm)
def f_lrui(uilr, uil, uildt): return max(0, uilr - uil) / uildt
def f_uil(lrui): return lrui


def f_lfr(ilf, lfert, lfrt): return (ilf - lfert) / lfrt
def f_pfr(fr, pfr, fspd): return (fr - pfr) / fspd
def f_lytd(lytdr): return lytdr
def f_lytdr(lytd, lycm, t, pyear): return clip(lytd * lycm, 0, t, pyear)


# Creation of equations

# Loop 1
world3.add_equation(nodes_div, lfc, [al, PALT])
world3.add_equation(f_al, al, [ldr, ler, lrui])
world3.add_equation(f_pal, pal, [ldr])

world3.add_equation(f_f, f, [ly, al, LFH, PL])
world3.add_equation(nodes_div, fpc, [f, pop])
world3.add_equation(clip, ifpc, [ifpc2, ifpc1, t, PYEAR])
world3.add_equation(f_tab_div, ifpc1, [IFPC1, iopc, GDPU])
world3.add_equation(f_tab_div, ifpc2, [IFPC2, iopc, GDPU])

world3.add_equation(nodes_mltpld, tai, [io, fioaa])
world3.add_equation(clip, fioaa, [fioaa2, fioaa1, t, PYEAR])
world3.add_equation(f_tab_div, fioaa1, [FIOAA1, fpc, ifpc])
world3.add_equation(f_tab_div, fioaa2, [FIOAA2, fpc, ifpc])

world3.add_equation(f_ldr, ldr, [tai, fiald, dcph])
world3.add_equation(f_tab_div, dcph, [DCPH, pal, PALT])

# Loop 2
world3.add_equation(f_cai, cai, [tai, fiald])
world3.add_equation(f_ai, ai, [cai, ai, alai])
world3.add_equation(clip, alai, [ALAI2, ALAI1, t, PYEAR])
world3.add_equation(f_aiph, aiph, [ai, falm, al])

world3.add_equation(f_tab_div, lymc, [LYMC, aiph, UAGI])
world3.add_equation(nodes_mltpld, ly, [lyf, lfert, lymc, lymap])

if world3.version == 1972:
    world3.add_equation(clip, lyf, [LYF2, LYF1, t, PYEAR])
if world3.version == 2003:
    world3.add_equation(clip, lyf, [lyf2, LYF1, t, PYEAR])

world3.add_equation(clip, lymap, [lymap2, lymap1, t, PYEAR])
world3.add_equation(f_tab_div, lymap1, [LYMAP1, io, IO70])
world3.add_equation(f_tab_div, lymap2, [LYMAP2, io, IO70])

world3.add_equation(f_tab_div, fiald, [FIALD, mpld, mpai])
world3.add_equation(f_mpld, mpld, [ly, dcph, SD])
world3.add_equation(f_mpai, mpai, [alai, ly, mlymc, lymc])
world3.add_equation(f_tab_div, mlymc, [MLYMC, aiph, UAGI])

if world3.version == 2003:
    world3.add_equation(lyf2.f_delayinit, lyf2, [lytd, TDD])

# Loop 3
world3.add_equation(nodes_mltpld, all, [ALLN, llmy])
world3.add_equation(f_llmy, llmy, [llmy2, llmy1, LLMYTM, OY, t])
world3.add_equation(f_tab_div, llmy1, [LLMY1, ly, ILF])
world3.add_equation(f_tab_div, llmy2, [LLMY2, ly, ILF])
world3.add_equation(nodes_div, ler, [al, all])

world3.add_equation(f_tab_div, uilpc, [UILPC, iopc, GDPU])
world3.add_equation(nodes_mltpld, uilr, [uilpc, pop])
world3.add_equation(f_lrui, lrui, [uilr, uil, UILDT])
world3.add_equation(f_uil, uil, [lrui])

# Loop 4
world3.add_equation(nodes_dif, lfert, [lfr, lfd])
world3.add_equation(f_tab, lfdr, [LFDR, ppolx])
world3.add_equation(nodes_mltpld, lfd, [lfert, lfdr])

# Loop 5
world3.add_equation(f_lfr, lfr, [ILF, lfert, lfrt])
world3.add_equation(f_tab, lfrt, [LFRT, falm])

world3.add_equation(f_tab, falm, [FALM, pfr])
world3.add_equation(nodes_div, fr, [fpc, SFPC])
world3.add_equation(f_pfr, pfr, [fr, pfr, FSPD])

if world3.version == 2003:
    world3.add_equation(f_lytd, lytd, [lytdr])
    world3.add_equation(f_lytdr, lytdr, [lytd, lycm, t, PYEAR])

    world3.add_equation(f_tab_dif, lycm, [LYCM, DFR, fr])
    world3.add_equation(f_tab, coym, [COYM, lyf])


##########################
# Equations on resources #
##########################

# Functions which are not defined in basic ones
def f_nr(nrur): return - nrur
def f_nrtd(nrate): return nrate
def f_nrate(nrtd, nrcm, t, pyear): return clip(nrtd * nrcm, 0, t, pyear)
def f_nrcm(nrcm, nrur, dnrur): return f_tab(nrcm, 1 - nrur/dnrur)


# Creation of equations

world3.add_equation(f_nr, nr, [nrur])
world3.add_equation(nodes_mltpld, nrur, [pop, pcrum, nruf])

if world3.version == 1972:
    world3.add_equation(clip, nruf, [NRUF2, NRUF1, t, PYEAR])
if world3.version == 2003:
    world3.add_equation(clip, nruf, [nruf2, NRUF1, t, PYEAR])

world3.add_equation(f_tab_div, pcrum, [PCRUM, iopc, GDPU])

world3.add_equation(nodes_div, nrfr, [nr, NRI])

world3.add_equation(clip, fcaor, [fcaor2, fcaor1, t, FCAORTM])
world3.add_equation(f_tab, fcaor1, [FCAOR1, nrfr])
world3.add_equation(f_tab, fcaor2, [FCAOR2, nrfr])

if world3.version == 2003:
    world3.add_equation(nruf2.f_delayinit, nruf2, [nrtd, TDD])
    world3.add_equation(f_nrtd, nrtd, [nrate])
    world3.add_equation(f_nrate, nrate, [nrtd, nrcm, t, PYEAR])
    world3.add_equation(f_nrcm, nrcm, [NRCM, nrur, DNRUR])

    world3.add_equation(f_tab, icor2t, [ICOR2T, nruf])


##########################
# Equations on pollution #
##########################

# Functions which are not defined in basic ones
def f_ppgr(ppgio, ppgao, ppgf): return (ppgio + ppgao) * ppgf
def f_ppasr(ppol, ahl): return ppol / (1.4 * ahl)
def f_ptd(ptdr): return ptdr
def f_ptdr(ptd, polgfm, t, pyear): return clip(ptd * polgfm, 0, t, pyear)
def f_polgfm(polgfm, ppolx, dpolx): return f_tab(polgfm, 1 - ppolx/dpolx)


# Creation of equations
world3.add_equation(f_ppgr, ppgr, [ppgio, ppgao, ppgf])

if world3.version == 1972:
    world3.add_equation(clip, ppgf, [PPGF2, PPGF1, t, PYEAR])
if world3.version == 2003:
    world3.add_equation(clip, ppgf, [ppgf2, PPGF1, t, PYEAR])

world3.add_equation(nodes_mltpld, ppgio, [pcrum, pop, FRPM, IMEF, IMTI])
world3.add_equation(nodes_mltpld, ppgao, [aiph, al, FIPM, AMTI])
world3.add_equation(ppapr.f_delayinit, ppapr, [ppgr, PPTD])
world3.add_equation(nodes_dif, ppol, [ppapr, ppasr])
world3.add_equation(nodes_div, ppolx, [ppol, PPOL70])
world3.add_equation(f_ppasr, ppasr, [ppol, ahl])

world3.add_equation(f_tab, ahlm, [AHLM, ppolx])
world3.add_equation(nodes_mltpld, ahl, [AHL70, ahlm])

if world3.version == 2003:
    world3.add_equation(ppgf2.f_delayinit, ppgf2, [ptd, TDD])
    world3.add_equation(f_ptd, ptd, [ptdr])
    world3.add_equation(f_ptdr, ptdr, [ptd, polgfm, t, PYEAR])

    world3.add_equation(f_polgfm, polgfm, [POLGFM, ppolx, DPOLX])

    world3.add_equation(f_tab, copm, [COPM, ppgf])


########################
# Equations on indexes #
########################

# Functions which are not defined in basic ones
def f_foa(pof, f, so, io): return (pof * f) / (pof * f + so+ io)
def f_foi(pof, f, so, io): return io / (pof * f + so+ io)
def f_fos(pof, f, so, io): return so / (pof * f + so+ io)


def f_plinid(ppgio, ppgf, io): return (ppgio * ppgf) / io


def f_hwi(lei, ei, gdpi): return (lei + ei + gdpi) / 3
def f_gdpi(gdppc, rlgdp, rhgdp): return log(gdppc / rlgdp, 10) / log(rhgdp / rlgdp, 10)


def f_hef(alggha, ulgha, algha, tl): return (alggha + ulgha + algha) / tl
def f_algha(ppgr, hup, ghah): return ppgr * hup / ghah


# Creation of equations

# Distribution of outputs between the different sector
world3.add_equation(f_foa, foa, [POF, f, so, io])
world3.add_equation(f_foi, foi, [POF, f, so, io])
world3.add_equation(f_fos, fos, [POF, f, so, io])

# Industrial outputs indexes
world3.add_equation(nodes_div, resint, [nrur, io])
world3.add_equation(f_plinid, plinid, [ppgio, ppgf, io])

world3.add_equation(nodes_mltpld, cio, [io, fioac])
world3.add_equation(nodes_div, ciopc, [cio, pop])

# Human Welfare Index
world3.add_equation(f_hwi, hwi, [lei, ei, gdpi])

world3.add_equation(f_tab_div, lei, [LEI, le, OY])

world3.add_equation(f_tab_div, ei, [EI, gdppc, GDPU])

world3.add_equation(f_gdpi, gdpi, [gdppc, RLGDP, RHGDP])
world3.add_equation(f_tab_div, gdppc, [GDPPC, iopc, GDPU])

# Human Ecological Footprint
world3.add_equation(f_hef, hef, [alggha, ulgha, algha, TL])

world3.add_equation(f_algha, algha, [ppgr, HUP, GHAH])
world3.add_equation(nodes_div, alggha, [al, GHAH])
world3.add_equation(nodes_div, ulgha, [uil, GHAH])
