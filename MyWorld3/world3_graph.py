from world3_dynamic import *
from math import log
import matplotlib.pyplot as plt

h = Hypergraph()


######################
# Initial conditions #
######################
version = 1972

IT = NodeConstant("IT", C, val=1900, hg=h) #Initial time - dt
FT = NodeConstant("FT", C, val=2100, hg=h) #Final time
TS = NodeConstant("TS", C, val=0.5, hg=h)
t = NodeStock("time", val=IT.val, hg=h)
h.add_edge(lambda x: 1, t, [TS])

nbpas = int((FT.val - IT.val) / TS.val)

######################
# Constantes d'unité #
######################
RHGDP = NodeConstant("RHGDP", C, val=9508., hg=h)
RLGDP = NodeConstant("RLGDP", C, val=24., hg=h)
TL = NodeConstant("TL", C, val=1.91, hg=h)
HGHA = NodeConstant("HGHA", C, val=1e9, hg=h)
OY = NodeConstant("OY", C, val=1., hg=h)
UAGI = NodeConstant("UAGI", C, val=1., hg=h)
UP = NodeConstant("UP", C, val=1., hg=h)
GDPU = NodeConstant("GDPU", C, val=1., hg=h)

###################
# Basic functions #
###################
def prod(*l):
    out = l[0]
    for x in l[1:]:
        out = out * x
    return out

def somme(*l):
    return sum([i for i in l])

def moins(x, y): return x - y
def div(x, y): return x / y

def clip(c1, c2, ts, t):
    if t <= ts : return c1
    else : return c2

def f_tab(tab, x):
    if tab[0][0] > x:
        #if  abs(tab[0][0] - x) > 5:
            #print(tab, x)
            #exit(0)
        return tab[0][1]
    if tab[-1][0] < x:
        #if abs(x - tab[-1][0]) > 5:
            #print(tab, x)
            #exit(0)
        return tab[-1][1]
    else:
        i = 0
        while i < len(tab):
            if tab[i][0] <= x <= tab[i+1][0]:
                coeff = (tab[i+1][1]-tab[i][1]) / (tab[i+1][0]-tab[i][0])
                return tab[i][1] + coeff * (x-tab[i][0])
            i += 1

def f_tab1(x, y, z): return f_tab(x, y/z)

def f_tab2(x, y, z): return f_tab(x, y - z)

######################################
# Variables close to population #
######################################
P1I = NodeConstant("P1I", C, val=6.50e8, hg=h)
P2I = NodeConstant("P2I", C, val=7.00e8, hg=h)
P3I = NodeConstant("P3I", C, val=1.90e8, hg=h)
P4I = NodeConstant("P4I", C, val=6.00e7, hg=h)

p1 = NodeStock("p1", val=P1I.val, hg=h)
p2 = NodeStock("p2", val=P2I.val, hg=h)
p3 = NodeStock("p3", val=P3I.val, hg=h)
p4 = NodeStock("p4", val=P4I.val, hg=h)
pop = NodeFlow("pop", hg=h)

M1 = NodeConstant("M1", CT, val=([20, 0.0567],
                                 [30, 0.0366],
                                 [40, 0.0243],
                                 [50, 0.0155],
                                 [60, 0.0082],
                                 [70, 0.0023],
                                 [80, 0.001]), hg=h)
M2 = NodeConstant("M2", CT, val=([20, 0.0266],
                                 [30, 0.0171],
                                 [40, 0.011],
                                 [50, 0.0065],
                                 [60, 0.004],
                                 [70, 0.0016],
                                 [80, 0.0008]), hg=h)
M3 = NodeConstant("M3", CT, val=([20, 0.0562],
                                 [30, 0.0373],
                                 [40, 0.0252],
                                 [50, 0.0171],
                                 [60, 0.0118],
                                 [70, 0.0083],
                                 [80, 0.006]), hg=h)
M4 = NodeConstant("M4", CT, val=([20, 0.13],
                                 [30, 0.11],
                                 [40, 0.09],
                                 [50, 0.07],
                                 [60, 0.06],
                                 [70, 0.05],
                                 [80, 0.04]), hg=h)

m1 = NodeFlow("m1", hg=h)
m2 = NodeFlow("m2", hg=h)
m3 = NodeFlow("m3", hg=h)
m4 = NodeFlow("m4", hg=h)

d1 = NodeFlow("d1", hg=h)
d2 = NodeFlow("d2", hg=h)
d3 = NodeFlow("d3", hg=h)
d4 = NodeFlow("d4", hg=h)

mat1 = NodeFlow("mat1", hg=h)
mat2 = NodeFlow("mat2", hg=h)
mat3 = NodeFlow("mat3", hg=h)

#Related to death
d = NodeFlow("d", hg=h)
cdr = NodeFlow("cdr", hg=h)

LEN = NodeConstant("LEN", C, val=28, hg=h)
HSID = NodeConstant("HSID", C, val=20, hg=h)
LMF = NodeConstant("LMF", CT, val=([0, 0],
                                   [1, 1],
                                   [2, 1.2],
                                   [3, 1.3],
                                   [4, 1.35],
                                   [5, 1.4]), hg=h)
HSAPC = NodeConstant("HSAPC", CT, val=([0, 0],
                                       [250, 20],
                                       [500, 50],
                                       [750, 95],
                                       [1000, 140],
                                       [1250, 175],
                                       [1500, 200],
                                       [1750, 220],
                                       [2000, 230]), hg=h)
LMHS1 = NodeConstant("LMHS1", CT, val=([0, 1],
                                       [20, 1.1],
                                       [40, 1.4],
                                       [60, 1.6],
                                       [80, 1.7],
                                       [100, 1.8]), hg=h)
LMHS2 = NodeConstant("LMHS2", CT, val=([0, 1],
                                       [20, 1.4],
                                       [40, 1.6],
                                       [60, 1.8],
                                       [80, 1.95],
                                       [100, 2]), hg=h)
FPU = NodeConstant("FPU", CT, val=([0, 0],
                                   [2.0e9, 0.2],
                                   [4.0e9, 0.4],
                                   [6.0e9, 0.5],
                                   [8.0e9, 0.58],
                                   [1.0e10, 0.65],
                                   [1.2e10, 0.72],
                                   [1.4e10, 0.78],
                                   [1.6e10, 0.8]), hg=h)
CMI = NodeConstant("CMI", CT, val=([0, 0.5],
                                   [200, 0.05],
                                   [400, -0.1],
                                   [600, -0.08],
                                   [800, -0.02],
                                   [1000, 0.05],
                                   [1200, 0.1],
                                   [1400, 0.15],
                                   [1600, 0.2]), hg=h)
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
                                   [100, 0.2]), hg=h)

lmhs = NodeFlow("lmhs", hg=h)
lmhs1 = NodeFlow("lmhs1", hg=h)
lmhs2 = NodeFlow("lmhs2", hg=h)
lmf = NodeFlow("lmf", hg=h)
hsapc = NodeFlow("hsapc", hg=h)
lmp = NodeFlow("lmp", hg=h)
cmi = NodeFlow("cmi", hg=h)
fpu = NodeFlow("fpu", hg=h)
lmc = NodeFlow("lmc", hg=h)
le = NodeFlow("le", hg=h)

#Related to birth
b = NodeFlow("b", hg=h)
cbr = NodeFlow("cbr", hg=h)

RLT = NodeConstant("RLT", C, val=30, hg=h)
PET = NodeConstant("PET", C, val=4000, hg=h)
MTFN = NodeConstant("MTFN", C, val=12, hg=h)
LPD = NodeConstant("LPD", C, val=20, hg=h)
ZPGT = NodeConstant("ZPGT", C, val=4000, hg=h)
DCFSN = NodeConstant("DCFSN", C, val=4, hg=h)
SAD = NodeConstant("SAD", C, val=20, hg=h)
IEAT = NodeConstant("IEAT", C, val=3, hg=h)
FCEST = NodeConstant("FCEST", C, val=4000, hg=h)
FRSNI = NodeConstant("FRSNI", C, val=0.785, hg=h)

FM = NodeConstant("FM", CT, val=([0, 0],
                                 [10, 0.2],
                                 [20, 0.4],
                                 [30, 0.6],
                                 [40, 0.8],
                                 [50, 0.9],
                                 [60, 1],
                                 [70, 1.05],
                                 [80, 1.1]), hg=h)
FCE = NodeConstant("FCE", CT, val=([0, 0.75],
                                   [0.5, 0.85],
                                   [1, 0.9],
                                   [1.5, 0.95],
                                   [2, 0.98],
                                   [2.5, 0.99],
                                   [3, 1]), hg=h)
FRSN = NodeConstant("FRSN", CT, val=([-0.2, 0.5],
                                     [-0.1, 0.6],
                                     [0, 0.7],
                                     [0.1, 0.875],
                                     [0.2, 1]), hg=h)
SFSN = NodeConstant("SFSN", CT, val=([0, 1.25],
                                     [200, 1],
                                     [400, 0.9],
                                     [600, 0.8],
                                     [800, 0.75]), hg=h)
CMPLE = NodeConstant("CMPLE", CT, val=([0, 3],
                                       [10, 2.1],
                                       [20, 1.6],
                                       [30, 1.4],
                                       [40, 1.3],
                                       [50, 1.2],
                                       [60, 1.1],
                                       [70, 1.05],
                                       [80, 1]), hg=h)
FSAFC = NodeConstant("FSAFC", CT, val=([0, 0],
                                       [2, 0.005],
                                       [4, 0.015],
                                       [6, 0.025],
                                       [8, 0.03],
                                       [10, 0.035]), hg=h)
fm = NodeFlow("fm", hg=h)
fce = NodeFlow("fce", hg=h)
frsn = NodeFlow("frsn", val=FRSNI.val, hg=h)
sfsn = NodeFlow("sfsn", hg=h)
if version == 1972:
    nruf2 = NodeConstant("nruf2", C, val=1, hg=h)
    ppgf2 = NodeConstant("ppgf2", C, val=1, hg=h)
cmple = NodeFlow("cmple", hg=h)
fsafc = NodeFlow("fsafc", hg=h)

tf = NodeFlow("tf", hg=h)
mtf = NodeFlow("mtf", hg=h)
dtf = NodeFlow("dtf", hg=h)
dcfs = NodeFlow("dcfs", hg=h)
fie = NodeFlow("fie", hg=h)
nfc = NodeFlow("nfc", hg=h)
fcapc = NodeFlow("fcapc", hg=h)

################################
# Variables close to capital #
################################
#Related to industry
ICOR1 = NodeConstant("ICOR1", C, val=3, hg=h)
if version == 1972:
    icor2 = NodeConstant("ICOR2", C, val=3, hg=h)
ICI = NodeConstant("ICI", C, val=2.1e11, hg=h)
ALIC = NodeConstant("ALIC", C, val=14, hg=h)
IET = NodeConstant("IET", C, val=4000, hg=h)
FIOACC = NodeConstant("FIOACC", C, val=0.43, hg=h)
IOPCD = NodeConstant("IOPCD", C, val=400, hg=h)
PYEAR = NodeConstant("PYEAR", C, val=1975, hg=h)

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
                                         [2, 0.83]), hg=h)
fioacv = NodeFlow("fioacv", hg=h)

iopc = NodeFlow("iopc", hg=h)
io = NodeFlow("io", hg=h)
icor = NodeFlow("icor", hg=h)
if version == 2003:
    icor2 = NodeFlow("icor2", hg=h)
ic = NodeStock("ic", val=ICI.val, hg=h)
icdr = NodeFlow("icdr", hg=h)
icir = NodeFlow("icir", hg=h)
fioai = NodeFlow("fioai", hg=h)
fioac = NodeFlow("fioac", hg=h)

#Related to services
SCI = NodeConstant("SCI", C, val=1.44e11, hg=h)
ALSC = NodeConstant("ALSC", C, val=20, hg=h)
SCOR = NodeConstant("SCOR", C, val=1, hg=h)

ISOPC1 = NodeConstant("ISOPC1", CT, val=([0, 40],
                                         [200, 300],
                                         [400, 640],
                                         [600, 1000],
                                         [800, 1220],
                                         [1000, 1450],
                                         [1200, 1650],
                                         [1400, 1800],
                                         [1600, 2000]), hg=h)
ISOPC2 = NodeConstant("ISOPC2", CT, val=([0, 40],
                                         [200, 300],
                                         [400, 640],
                                         [600, 1000],
                                         [800, 1220],
                                         [1000, 1450],
                                         [1200, 1650],
                                         [1400, 1800],
                                         [1600, 2000]), hg=h)
FIOAS1 = NodeConstant("FIOAS1", CT, val=([0, 0.3],
                                         [0.5, 0.2],
                                         [1, 0.1],
                                         [1.5, 0.05],
                                         [2, 0]), hg=h)
FIOAS2 = NodeConstant("FIOAS2", CT, val=([0, 0.3],
                                         [0.5, 0.2],
                                         [1, 0.1],
                                         [1.5, 0.05],
                                         [2, 0]), hg=h)
isopc1 = NodeFlow("isopc1", hg=h)
isopc2 = NodeFlow("isopc2", hg=h)
fioas1 = NodeFlow("fioas1", hg=h)
fioas2 = NodeFlow("fioas2", hg=h)

isopc = NodeFlow("isopc", hg=h)
fioas = NodeFlow("fioas", hg=h)
scir = NodeFlow("scir", hg=h)
sc = NodeStock("sc", val=SCI.val, hg=h)
scdr = NodeFlow("scdr", hg=h)
so = NodeFlow("so", hg=h)
sopc = NodeFlow("sopc", hg=h)

#Related to jobs
LFPF = NodeConstant("LFPF", C, val=0.75, hg=h)
LUFDT = NodeConstant("LUFDT", C, val=2, hg=h)
LUFDI =NodeConstant("LUFDI", C, val=2.8, hg=h)
CUFI = NodeConstant("CUFI", C, val=0.999, hg=h)

JPICU = NodeConstant("JPICU", CT, val=([50, 0.37],
                                       [200, 0.18],
                                       [350, 0.12],
                                       [500, 0.09],
                                       [650, 0.07],
                                       [800, 0.06]), hg=h)
JPSCU = NodeConstant("JPSCU", CT, val=([50, 1.1],
                                       [200, 0.6],
                                       [350, 0.35],
                                       [500, 0.2],
                                       [650, 0.15],
                                       [800, 0.15]), hg=h)
JPH = NodeConstant("JPH", CT, val=([2, 2],
                                   [6, 0.5],
                                   [10, 0.4],
                                   [14, 0.3],
                                   [18, 0.27],
                                   [22, 0.24],
                                   [26, 0.2],
                                   [30, 0.2]), hg=h)
CUF = NodeConstant("CUF", CT, val=([1, 1],
                                   [3, 0.995],
                                   [5, 0.7],
                                   [7, 0.3],
                                   [9, 0.1],
                                   [11, 0.1]), hg=h)
jpicu = NodeFlow("jpicu", hg=h)
jpscu = NodeFlow("jpscu", hg=h)
jph = NodeFlow("jph", hg=h)
cuf = NodeFlow("cuf", val=CUFI.val, hg=h)

j = NodeFlow("j", hg=h)
pjis = NodeFlow("pjis", hg=h)
pjss = NodeFlow("pjss", hg=h)
pjas = NodeFlow("pjas", hg=h)
lf = NodeFlow("lf", hg=h)
luf = NodeFlow("luf", hg=h)
lufd = NodeStock("lufd", val=LUFDI.val, hg=h)

##################################
# Variables close to agriculture #
##################################
#Loop 1
PALT = NodeConstant("PALT", C, val=3.2e9, hg=h)
ALI = NodeConstant("ALI", C, val=0.9e9, hg=h)
PALI = NodeConstant("PALI", C, val=2.3e9, hg=h)
LFH = NodeConstant("LFH", C, val=0.7, hg=h)
PL = NodeConstant("PL", C, val=0.1, hg=h)

IFPC1 = NodeConstant("IFPC1", CT, val=([0, 230],
                                       [200, 480],
                                       [400, 690],
                                       [600, 850],
                                       [800, 970],
                                       [1000, 1070],
                                       [1200, 1150],
                                       [1400, 1210],
                                       [1600, 1250]), hg=h)
IFPC2 = NodeConstant("IFPC2", CT, val=([0, 230],
                                       [200, 480],
                                       [400, 690],
                                       [600, 850],
                                       [800, 970],
                                       [1000, 1070],
                                       [1200, 1150],
                                       [1400, 1210],
                                       [1600, 1250]), hg=h)
FIOAA1 = NodeConstant("FIOAA1", CT, val=([0, 0.4],
                                         [0.5, 0.205],
                                         [1, 0.1],
                                         [1.5, 0.025],
                                         [2, 0],
                                         [2.5, 0]), hg=h)
FIOAA2 = NodeConstant("FIOAA2", CT, val=([0, 0.4],
                                         [0.5, 0.205],
                                         [1, 0.1],
                                         [1.5, 0.025],
                                         [2, 0],
                                         [2.5, 0]), hg=h)
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
                                     [1, 50]), hg=h)
ifpc1 = NodeFlow("ifpc1", hg=h)
ifpc2 = NodeFlow("ifpc2", hg=h)
fioaa1 = NodeFlow("fioaa1", hg=h)
fioaa2 = NodeFlow("fioaa2", hg=h)
dcph = NodeFlow("dcph", hg=h)

lfc = NodeFlow("lfc", hg=h)
al = NodeStock("al", val=ALI.val, hg=h)
pal = NodeStock("pal", val=PALI.val, hg=h)
f = NodeFlow("f", hg=h)
fpc = NodeFlow("fpc", hg=h)
ifpc = NodeFlow("ifpc", hg=h)
tai = NodeFlow("tai", hg=h)
fioaa = NodeFlow("fioaa", hg=h)
ldr = NodeFlow("ldr", hg=h)

#Loop 2
ALAI = NodeConstant("ALAI", C, val=2, hg=h)
AII = NodeConstant("AII", C, val=6.21e9, hg=h)
LYF1 = NodeConstant("LYF1", C, val=1, hg=h)
if version == 1972:
    lyf2 = NodeConstant("lyf2", C, val=1, hg=h)
IO70 = NodeConstant("IO70", C, val=7.9e11, hg=h)
SD = NodeConstant("SD", C, val=0.07, hg=h)
TDD = NodeConstant("TDD", C, val=20, hg=h)

LYMC = NodeConstant("LYMC", CT, val=([0, 1],
                                     [40, 3],
                                     [80, 3.8],
                                     [120, 4.4],
                                     [160, 4.9],
                                     [200, 5.4],
                                     [240, 5.7],
                                     [280, 6.0],
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
                                     [1000, 10]), hg=h)
LYMAP1 = NodeConstant("LYMAP1", CT, val=([0, 1],
                                         [10, 1],
                                         [20, 0.7],
                                         [30, 0.4]), hg=h)
LYMAP2 = NodeConstant("LYMAP2", CT, val=([0, 1],
                                         [10, 1],
                                         [20, 0.7],
                                         [30, 0.4]), hg=h)
FIALD = NodeConstant("FIALD", CT, val=([0, 0],
                                       [0.25, 0.05],
                                       [0.5, 0.15],
                                       [0.75, 0.3],
                                       [1, 0.5],
                                       [1.25, 0.7],
                                       [1.5, 0.85],
                                       [1.75, 0.95],
                                       [2, 1]), hg=h)
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
                                       [600, 0.005]), hg=h)
lymc = NodeFlow("lymc", hg=h)
lymap = NodeFlow("lymap", hg=h)
lymap1 = NodeFlow("lymap1", hg=h)
lymap2 = NodeFlow("lymap2", hg=h)
fiald = NodeFlow("fiald", hg=h)
mlymc = NodeFlow("mlymc", hg=h)

cai = NodeFlow("cai", hg=h)
ai = NodeStock("ai", val=AII.val, hg=h)
aiph = NodeFlow("aiph", hg=h)
ly = NodeFlow("ly", hg=h)
lyf = NodeFlow("lyf", hg=h)
mpld = NodeFlow("mpld", hg=h)
mpai = NodeFlow("mpai", hg=h)

#Loop 3
ALLN = NodeConstant("ALLN", C, val=6000, hg=h)
UILDT = NodeConstant("UILDT", C, val=10, hg=h)
UILI = NodeConstant("UILI", C, val=8.2e6, hg=h)
LLMYTM = NodeConstant("LLMYTM", C, val=4000, hg=h)

LLMY1 = NodeConstant("LLMY1", CT, val=([0, 1.2],
                                       [1, 1],
                                       [2, 0.63],
                                       [3, 0.36],
                                       [4, 0.16],
                                       [5, 0.055],
                                       [6, 0.04],
                                       [7, 0.025],
                                       [8, 0.015],
                                       [9, 0.01]), hg=h)
LLMY2 = NodeConstant("LLMY2", CT, val=([0, 1.2],
                                       [1, 1],
                                       [2, 0.63],
                                       [3, 0.36],
                                       [4, 0.16],
                                       [5, 0.055],
                                       [6, 0.04],
                                       [7, 0.025],
                                       [8, 0.015],
                                       [9, 0.01]), hg=h)
UILPC = NodeConstant("UILPC", CT, val=([0, 0.005],
                                       [200, 0.008],
                                       [400, 0.015],
                                       [600, 0.025],
                                       [800, 0.04],
                                       [1000, 0.055],
                                       [1200, 0.07],
                                       [1400, 0.08],
                                       [1600, 0.09]), hg=h)
llmy = NodeFlow("llmy", hg=h)
llmy1 = NodeFlow("llmy1", hg=h)
llmy2 = NodeFlow("llmy2", hg=h)
uilpc = NodeFlow("uilpc", hg=h)

all = NodeFlow("all", hg=h)
ler = NodeFlow("ler", hg=h)
uilr = NodeFlow("uilr", hg=h)
lrui = NodeFlow("lrui", hg=h)
uil = NodeStock("uil", val=UILI.val, hg=h)

#Loop 4
LFERTI = NodeConstant("LFERTI", C, val=600, hg=h)

LFDR = NodeConstant("LFDR", CT, val=([0, 0],
                                     [10, 0.1],
                                     [20, 0.3],
                                     [30, 0.5]), hg=h)
lfdr = NodeFlow("lfdr", hg=h)

lfert = NodeStock("lfert", val=LFERTI.val, hg=h)
lfd = NodeFlow("lfd", hg=h)

#Loop 5
ILF = NodeConstant("ILF", C, val=600, hg=h)
SFPC = NodeConstant("SFPC", C, val=230, hg=h)
FSPD = NodeConstant("FSPD", C, val=2, hg=h)
PFRI = NodeConstant("PFRI", C, val=1.17, hg=h)
if version == 2003:
    DFR = NodeConstant("DFR", C, val=2, hg=h)

LFRT = NodeConstant("LFRT", CT, val=([0, 20],
                                     [0.02, 13],
                                     [0.04, 8],
                                     [0.06, 4],
                                     [0.08, 2],
                                     [0.1, 2]), hg=h)
FALM = NodeConstant("FALM", CT, val=([0, 0],
                                     [1, 0.04],
                                     [2, 0.07],
                                     [3, 0.09],
                                     [4, 0.1]), hg=h)
if version == 2003:
    LYCM = NodeConstant("LYCM", CT, val=([0, 0],
                                         [1, 0.04]), hg=h)
    COYM = NodeConstant("COYM", CT, val=([1, 1],
                                         [1.2, 1.05],
                                         [1.4, 1.12],
                                         [1.6, 1.25],
                                         [1.8, 1.35],
                                         [2, 1.5]), hg=h)
lfrt = NodeFlow("lfrt", hg=h)
falm = NodeFlow("falm", hg=h)
if version == 2003:
    lycm = NodeFlow("lycm", hg=h)
    coym = NodeFlow("coym", hg=h)

lfr = NodeFlow("lfr", hg=h)
fr = NodeFlow("fr", hg=h)
pfr = NodeStock("pfr", val=PFRI.val, hg=h)
if version == 2003:
    lytd = NodeStock("lytd", val=LYF1.val, hg=h)
    lytdr = NodeFlow("lytdr", hg=h)

################################
# Variables close to resources #
################################
NRI = NodeConstant("NRI", C, val=1e12, hg=h)
NRUF1 = NodeConstant("NRUFI", C, val=1, hg=h)
if version == 2003:
    DNRUR = NodeConstant("DNRUR", C, val=4.8e9, hg=h)
FCAORTM = NodeConstant("FCAORTM", C, val=4000, hg=h)

PCRUM = NodeConstant("PCRUM", CT, val=([0, 0],
                                       [200, 0.85],
                                       [400, 2.6],
                                       [600, 4.4],
                                       [800, 5.4],
                                       [1000, 6.2],
                                       [1200, 6.8],
                                       [1400, 7.0],
                                       [1600, 7.0]), hg=h)
FCAOR1 = NodeConstant("FCAOR1", CT, val=([0, 1],
                                         [0.1, 0.9],
                                         [0.2, 0.7],
                                         [0.3, 0.495],
                                         [0.4, 0.2],
                                         [0.5, 0.1],
                                         [0.6, 0.05],
                                         [0.7, 0.05],
                                         [0.8, 0.05],
                                         [0.9, 0.05],
                                         [1, 0.05]), hg=h)
FCAOR2 = NodeConstant("FCAOR2", CT, val=([0, 1],
                                         [0.1, 0.9],
                                         [0.2, 0.7],
                                         [0.3, 0.495],
                                         [0.4, 0.2],
                                         [0.5, 0.1],
                                         [0.6, 0.05],
                                         [0.7, 0.05],
                                         [0.8, 0.05],
                                         [0.9, 0.05],
                                         [1, 0.05]), hg=h)
if version == 2003:
    NRCM = NodeConstant("NRCM", CT, val=([-1, -0.04],
                                         [0, 0]), hg=h)
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
                                             [1, 3]), hg=h)
pcrum = NodeFlow("pcrum", hg=h)
fcaor = NodeFlow("fcaor", hg=h)
fcaor1 = NodeFlow("fcaor1", hg=h)
fcaor2 = NodeFlow("fcaor2", hg=h)
if version == 2003:
    nrcm = NodeFlow("nrcm", hg=h)
    icor2t = NodeFlow("icor2t", hg=h)

nr = NodeStock("nr", val=NRI.val, hg=h)
nrur = NodeFlow("nrur", hg=h)
nruf = NodeFlow("nruf", hg=h)
nrfr = NodeFlow("nrfr", hg=h)
if version == 2003:
    nrtd = NodeStock("nrtd", val=NRUF1.val, hg=h)
    nrate = NodeFlow("nrate", hg=h)

################################
# Variables close to pollution #
################################
PPGF1 = NodeConstant("PPGF1", C, val=1, hg=h)
FRPM = NodeConstant("FRPM", C, val=0.02, hg=h)
IMEF = NodeConstant("IMEF", C, val=0.1, hg=h)
IMTI = NodeConstant("IMTI", C, val=10, hg=h)
FIPM = NodeConstant("FIPM", C, val=0.001, hg=h)
AMTI = NodeConstant("AMTI", C, val=1, hg=h)
PPTD = NodeConstant("PPTD", C, val=20, hg=h)
PPOLI = NodeConstant("PPOLI", C, val=2.5e7, hg=h)
PPOL70 = NodeConstant("PPOLI70", C, val=1.36e8, hg=h)
AHL70 = NodeConstant("AHL70", C, val=1.5, hg=h)
if version == 2003:
    DPOLX = NodeConstant("DPOLX", C, val=1.2, hg=h)

AHLM = NodeConstant("AHLM", CT, val=([1, 1],
                                     [251, 11],
                                     [501, 21],
                                     [751, 31],
                                     [1001, 41]), hg=h)
if version == 2003:
    POLGFM = NodeConstant("POLGFM", CT, val=([-1, -0.04],
                                             [0, 0]), hg=h)
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
                                         [1, 1]), hg=h)

ahlm = NodeFlow("ahlm", hg=h)
if version == 2003:
    polgfm = NodeFlow("polgfm", hg=h)
    copm = NodeFlow("copm", hg=h)

ppgr = NodeFlow("ppgr", hg=h)
ppgf = NodeFlow("ppgf", hg=h)
ppgio = NodeFlow("ppgio", hg=h)
ppgao = NodeFlow("ppgao", hg=h)
ppol = NodeStock("ppol", val=PPOLI.val, hg=h)
ppolx = NodeFlow("ppolx", hg=h)
ppasr = NodeFlow("ppasr", hg=h)
ahl = NodeFlow("ahl", hg=h)
if version == 2003:
    ptd = NodeStock("ptd", val=PPGF1.val, hg=h)
    ptdr = NodeFlow("ptdr", hg=h)

################
# Update Index #
################
if version == 2003:
    HUP = NodeConstant("HUP", C, val=4, hg=h)

    LEI = NodeConstant("LEI", CT, val=([25, 0],
                                       [35, 0.16],
                                       [45, 0.33],
                                       [55, 0.5],
                                       [65, 0.67],
                                       [75, 0.84],
                                       [85, 1]), hg=h)
    EI = NodeConstant("EI", CT, val=([0, 0],
                                     [1000, 0.81],
                                     [2000, 0.88],
                                     [3000, 0.92],
                                     [4000, 0.95],
                                     [5000, 0.98],
                                     [6000, 0.99],
                                     [7000, 1]), hg=h)
    GDPPC = NodeConstant("GDPPC", CT, val=([0, 120],
                                           [200, 600],
                                           [400, 1200],
                                           [600, 1800],
                                           [800, 2500],
                                           [1000, 3200]), hg=h)
    lei = NodeFlow("lei", hg=h)
    ei = NodeFlow("ei", hg=h)
    gdppc = NodeFlow("gdppc", hg=h)

    hwi = NodeFlow("hwi", hg=h)
    gdpi = NodeFlow("gdpi", hg=h)
    hef = NodeFlow("hef", hg=h)
    algha = NodeFlow("algha", hg=h)
    alggha = NodeFlow("alggha", hg=h)
    ulgha = NodeFlow("ulgha", hg=h)

####################
# Smooth functions #
####################
ehspc = NodeSmooth("ehspc", "SMOOTH", nbpas, hg=h)
ple = NodeSmooth("ple", "DELAY3", nbpas, hg=h)
diopc = NodeSmooth("diopc", "DELAY3", nbpas, hg=h)
aiopc = NodeSmooth("aiopc", "SMOOTH", nbpas, hg=h)
fcfpc = NodeSmooth("fcfpc", "DELAY3", nbpas, hg=h)
# = NodeSmooth("lufd", "SMOOTH", nbpas, hg=h)
if version == 2003:
    lyf2 = NodeSmooth("lyf2", "DELAY3", nbpas, hg=h)
    nruf2 = NodeSmooth("nruf2", "DELAY3", nbpas, hg=h)
    ppgf2 = NodeSmooth("ppgf2", "DELAY3", nbpas, hg=h)
ppapr = NodeSmooth("ppapr", "DELAY3", nbpas, hg=h)

#######################
# Edges on population #
#######################
h.add_edge(somme, pop, [p1, p2, p3, p4])
h.add_edge(prod, d1, [p1, m1])
h.add_edge(prod, d2, [p2, m2])
h.add_edge(prod, d3, [p3, m3])
h.add_edge(prod, d4, [p4, m4])

def f_mat1(p1, m1): return p1 * (1 - m1) / 15
h.add_edge(f_mat1, mat1, [p1, m1])
def f_mat2(p2, m2): return p2 * (1 - m2) / 30
h.add_edge(f_mat2, mat2, [p2, m2])
def f_mat3(p3, m3): return p3 * (1 - m3) / 20
h.add_edge(f_mat3, mat3, [p3, m3])

h.add_edge(f_tab1, m1, [M1, le, OY])
h.add_edge(f_tab1, m2, [M2, le, OY])
h.add_edge(f_tab1, m3, [M3, le, OY])
h.add_edge(f_tab1, m4, [M4, le, OY])

def p1_evo(b, d1, mat1):
    return b - d1 - mat1
def p2_evo(mat1, d2, mat2):
    return mat1 - d2 - mat2
def p3_evo(mat2, d3, mat3):
    return mat2 - d3 - mat3

h.add_edge(p1_evo, p1, [b, d1, mat1])
h.add_edge(p2_evo, p2, [mat1, d2, mat2])
h.add_edge(p3_evo, p3, [mat2, d3, mat3])
h.add_edge(moins, p4, [mat3, d4])

h.add_edge(somme, d, [d1, d2, d3, d4])
def f_cdr(d, pop): return 1000 * d / pop
h.add_edge(f_cdr, cdr, [d, pop])

h.add_edge(prod, le, [LEN, lmf, lmhs, lmp, lmc])

h.add_edge(f_tab1, lmf, [LMF, fpc, SFPC])
h.add_edge(f_tab1, hsapc, [HSAPC, sopc, GDPU])

def f_lmhs(lmhs1, lmhs2, t): return clip(lmhs1, lmhs2, 1940, t)
h.add_edge(f_lmhs, lmhs, [lmhs1, lmhs2, t])

h.add_edge(f_tab1, lmhs1, [LMHS1, ehspc, GDPU])
h.add_edge(f_tab1, lmhs2, [LMHS2, ehspc, GDPU])
h.add_edge(f_tab1, fpu, [FPU, pop, UP])
h.add_edge(f_tab1, cmi, [CMI, iopc, GDPU])

def f_lmc(cmi, fpu): return 1 - cmi * fpu
h.add_edge(f_lmc, lmc, [cmi, fpu])

h.add_edge(f_tab, lmp, [LMP, ppolx])

def f_b(d, pet, tf, p2, rlt, t): return clip(d, 0.5 * tf * p2 / rlt, t, pet)
h.add_edge(f_b, b, [d, PET, tf, p2, RLT, t])

def f_cbr(b, pop): return 1000 * b / pop
h.add_edge(f_cbr, cbr, [b, pop])

def f_tf(mtf, fce, dtf): return min(mtf, mtf * (1 - fce) + dtf * fce)
h.add_edge(f_tf, tf, [mtf, fce, dtf])

h.add_edge(prod, mtf, [MTFN, fm])

h.add_edge(f_tab1, fm, [FM, le, OY])

h.add_edge(prod, dtf, [dcfs, cmple])

h.add_edge(f_tab1, cmple, [CMPLE, ple, OY])

def f_dcfs(dcfsn, frsn, sfsn, t, zpgt): return clip(2, dcfsn * frsn * sfsn, t, zpgt)
h.add_edge(f_dcfs, dcfs, [DCFSN, frsn, sfsn, t, ZPGT])

h.add_edge(f_tab1, sfsn, [SFSN, diopc, GDPU])
h.add_edge(f_tab, frsn, [FRSN, fie])

def f_fie(iopc, aiopc): return (iopc - aiopc) / aiopc
h.add_edge(f_fie, fie, [iopc, aiopc])

def f_nfc(mtf, dtf): return mtf / dtf - 1
h.add_edge(f_nfc, nfc, [mtf, dtf])

def f_fce(fce, fcfpc, gdpu, t, fcest): return clip(1, f_tab1(fce, fcfpc, gdpu), t, fcest)
h.add_edge(f_fce, fce, [FCE, fcfpc, GDPU, t, FCEST])

h.add_edge(prod, fcapc, [fsafc, sopc])

h.add_edge(f_tab, fsafc, [FSAFC, nfc])

####################
# Edges on capital #
####################
h.add_edge(div, iopc, [io, pop])

def f_io(ic, fcaor, cuf, icor): return (ic * (1 - fcaor) * cuf) / icor
h.add_edge(f_io, io, [ic, fcaor, cuf, icor])

h.add_edge(clip, icor, [icor2, ICOR1, t, PYEAR])

if version == 2003:
    h.add_edge(prod, icor2, [icor2t, coym, copm])

h.add_edge(moins, ic, [icir, icdr])
h.add_edge(div, icdr, [ic, ALIC])

h.add_edge(prod, icir, [io, fioai])

def f_fioai(fioaa, fioas, fioac): return 1 - fioaa - fioas - fioac
h.add_edge(f_fioai, fioai, [fioaa, fioas, fioac])

h.add_edge(clip, fioac, [fioacv, FIOACC, t, IET])

h.add_edge(f_tab1, fioacv, [FIOACV, iopc, IOPCD])

h.add_edge(clip, isopc, [isopc2, isopc1, t, PYEAR])

h.add_edge(f_tab1, isopc1, [ISOPC1, iopc, GDPU])
h.add_edge(f_tab1, isopc2, [ISOPC2, iopc, GDPU])

h.add_edge(clip, fioas, [fioas2, fioas1, t, PYEAR])

h.add_edge(f_tab1, fioas1, [FIOAS1, sopc, isopc])
h.add_edge(f_tab1, fioas2, [FIOAS2, sopc, isopc])

h.add_edge(prod, scir, [io, fioas])
h.add_edge(moins, sc, [scir, scdr])
h.add_edge(div, scdr, [sc, ALSC])

def f_so(sc, cuf, scor): return sc *cuf / scor
h.add_edge(f_so, so, [sc, cuf, SCOR])

h.add_edge(div, sopc, [so, pop])

def f_j(pjis, pjas, pjss): return pjis + pjas + pjss
h.add_edge(f_j, j, [pjis, pjas, pjss])

h.add_edge(prod, pjis, [ic, jpicu])
def f_jpicu(jpicu, iopc, gdpu): return 0.001 * f_tab1(jpicu, iopc, gdpu)
h.add_edge(f_jpicu, jpicu, [JPICU, iopc, GDPU])

h.add_edge(prod, pjss, [sc, jpscu])
def f_jpscu(jpscu, sopc, gdpu): return 0.001 * f_tab1(jpscu, sopc, gdpu)
h.add_edge(f_jpscu, jpscu, [JPSCU, sopc, GDPU])

h.add_edge(prod, pjas, [jph, al])
h.add_edge(f_tab1, jph, [JPH, aiph, UAGI])

def f_lf(p2, p3, lfpf): return (p2 + p3) * lfpf
h.add_edge(f_lf, lf, [p2, p3, LFPF])

h.add_edge(div, luf, [j, lf])

def f_lufd(luf, lufd, lufdt): return (luf - lufd) / lufdt
h.add_edge(f_lufd, lufd, [luf, lufd, LUFDT])

h.add_edge(f_tab, cuf, [CUF, lufd])

########################
# Edges on agriculture #
########################
#Loop 1
h.add_edge(div, lfc, [al, PALT])

def f_al(ldr, ler, lrui): return ldr - ler - lrui
h.add_edge(f_al, al, [ldr, ler, lrui])

def f_pal(ldr): return - ldr
h.add_edge(f_pal, pal, [ldr])

def f_f(ly, al, lfh, pl): return ly * al * lfh * (1 - pl)
h.add_edge(f_f, f, [ly, al, LFH, PL])

h.add_edge(div, fpc, [f, pop])

h.add_edge(clip, ifpc, [ifpc2, ifpc1, t, PYEAR])

h.add_edge(f_tab1, ifpc1, [IFPC1, iopc, GDPU])
h.add_edge(f_tab1, ifpc2, [IFPC2, iopc, GDPU])

h.add_edge(prod, tai, [io, fioaa])

h.add_edge(clip, fioaa, [fioaa2, fioaa1, t, PYEAR])

h.add_edge(f_tab1, fioaa1, [FIOAA1, fpc, ifpc])
h.add_edge(f_tab1, fioaa2, [FIOAA2, fpc, ifpc])

def f_ldr(tai, fiald, dcph): return tai * fiald / dcph
h.add_edge(f_ldr, ldr, [tai, fiald, dcph])

h.add_edge(f_tab1, dcph, [DCPH, pal, PALT])

#Loop 2
def f_cai(tai, fiald): return tai * (1 - fiald)
h.add_edge(f_cai, cai, [tai, fiald])

def f_ai(cai, ai, alai): return (cai - ai) / alai
h.add_edge(f_ai, ai, [cai, ai, ALAI])

def f_aiph(ai, falm, al): return ai * (1 - falm) / al
h.add_edge(f_aiph, aiph, [ai, falm, al])

h.add_edge(f_tab1, lymc, [LYMC, aiph, UAGI])

h.add_edge(prod, ly, [lyf, lfert, lymc, lymap])

h.add_edge(clip, lyf, [lyf2, LYF1, t, PYEAR])

h.add_edge(clip, lymap, [lymap2, lymap1, t, PYEAR])

h.add_edge(f_tab1, lymap1, [LYMAP1, io, IO70])
h.add_edge(f_tab1, lymap2, [LYMAP2, io, IO70])
h.add_edge(f_tab1, fiald, [FIALD, mpld, mpai])

def f_mpld(ly, dcph, sd): return ly / (dcph * sd)
h.add_edge(f_mpld, mpld, [ly, dcph, SD])

def f_mpai(alai, ly, mlymc, lymc): return alai * ly * mlymc / lymc
h.add_edge(f_mpai, mpai, [ALAI, ly, mlymc, lymc])

h.add_edge(f_tab1, mlymc, [MLYMC, aiph, UAGI])

#Loop 3
h.add_edge(prod, all, [ALLN, llmy])

def f_llmy(llmy2, llmy1, llmytm, oy, t): return clip(0.95 ** ((t - llmytm) / oy) * llmy1 + (1 - 0.95 ** ((t - llmytm) / oy)) * llmy2, llmy1, t, llmytm)
h.add_edge(f_llmy, llmy, [llmy2, llmy1, LLMYTM, OY, t])

h.add_edge(f_tab1, llmy1, [LLMY1, ly, ILF])
h.add_edge(f_tab1, llmy2, [LLMY2, ly, ILF])

h.add_edge(div, ler, [al, all])

h.add_edge(f_tab1, uilpc, [UILPC, iopc, GDPU])

h.add_edge(prod, uilr, [uilpc, pop])

def f_lrui(uilr, uil, uildt): return max(0, uilr - uil) / uildt
h.add_edge(f_lrui, lrui, [uilr, uil, UILDT])

def f_uil(lrui): return lrui
h.add_edge(f_uil, uil, [lrui])

#Loop 4
h.add_edge(moins, lfert, [lfr, lfd])
h.add_edge(f_tab, lfdr, [LFDR, ppolx])
h.add_edge(prod, lfd, [lfert, lfdr])

#Loop 5
def f_lfr(ilf, lfert, lfrt): return (ilf - lfert) / lfrt
h.add_edge(f_lfr, lfr, [ILF, lfert, lfrt])

h.add_edge(f_tab, lfrt, [LFRT, falm])
h.add_edge(f_tab, falm, [FALM, pfr])
h.add_edge(div, fr, [fpc, SFPC])

def f_pfr(fr, pfr, fspd): return (fr - pfr) / fspd
h.add_edge(f_pfr, pfr, [fr, pfr, FSPD])

if version == 2003:
    def f_lytd(lytdr): return - lytdr
    h.add_edge(f_lytd, lytd, [lytdr])

    def f_lytdr(lytd, lycm, t, pyear): return clip(lytd * lycm, 0, t, pyear)
    h.add_edge(f_lytdr, lytdr, [lytd, lycm, t, PYEAR])

    h.add_edge(f_tab2, lycm, [LYCM, DFR, fr])
    h.add_edge(f_tab, coym, [COYM, lyf])

######################
# Edges on resources #
######################
def f_nr(nrur): return - nrur
h.add_edge(f_nr, nr, [nrur])
h.add_edge(prod, nrur, [pop, pcrum, nruf])

h.add_edge(clip, nruf, [nruf2, NRUF1, t, PYEAR])

h.add_edge(f_tab1, pcrum, [PCRUM, iopc, GDPU])
h.add_edge(div, nrfr, [nr, NRI])

h.add_edge(clip, fcaor, [fcaor2, fcaor1, t, FCAORTM])

h.add_edge(f_tab, fcaor1, [FCAOR1, nrfr])
h.add_edge(f_tab, fcaor2, [FCAOR2, nrfr])

if version == 2003:
    def f_nrtd(nrate): return - nrate
    h.add_edge(f_nrtd, nrtd, [nrate])

    def f_nrate(nrtd, nrcm, t, pyear): return clip(nrtd * nrcm, 0, t, pyear)
    h.add_edge(f_nrate, nrate, [nrtd, nrcm, t, PYEAR])

    def f_nrcm(nrcm, nrur, dnrur): return f_tab(nrcm, 1 - nrur/dnrur)
    h.add_edge(f_nrcm, nrcm, [NRCM, nrur, DNRUR])
    h.add_edge(f_tab, icor2t, [ICOR2T, nruf])

######################
# Edges on pollution #
######################
def f_ppgr(ppgio, ppgao, ppgf): return (ppgio + ppgao) * ppgf
h.add_edge(f_ppgr, ppgr, [ppgio, ppgao, ppgf])

h.add_edge(clip, ppgf, [ppgf2, PPGF1, t, PYEAR])

h.add_edge(prod, ppgio, [pcrum, pop, FRPM, IMEF, IMTI])
h.add_edge(prod, ppgao, [aiph, al, FIPM, AMTI])

h.add_edge(moins, ppol, [ppapr, ppasr])
h.add_edge(div, ppolx, [ppol, PPOL70])

def f_ppasr(ppol, ahl): return ppol / (1.4 * ahl)
h.add_edge(f_ppasr, ppasr, [ppol, ahl])

h.add_edge(f_tab, ahlm, [AHLM, ppolx])
h.add_edge(prod, ahl, [AHL70, ahlm])

if version == 2003:
    def f_ptd(ptdr): return - ptdr
    h.add_edge(f_ptd, ptd, [ptdr])

    def f_ptdr(ptd, polgfm, t, pyear): return clip(ptd * polgfm, 0, t, pyear)
    h.add_edge(f_ptdr, ptdr, [ptd, polgfm, t, PYEAR])

    def f_polgfm(polgfm, ppolx, dpolx): return f_tab(polgfm, 1 - ppolx/dpolx)
    h.add_edge(f_polgfm, polgfm, [POLGFM, ppolx, DPOLX])

    h.add_edge(f_tab, copm, [COPM, ppgf])

###################
# Edges on update #
###################
if version == 2003:
    def f_hwi(lei, ei, gdpi): return (lei + ei + gdpi) / 3
    h.add_edge(f_hwi, hwi, [lei, ei, gdpi])

    h.add_edge(f_tab1, lei, [LEI, le, OY])
    h.add_edge(f_tab1, ei, [EI, gdppc, GDPU])

    def f_gdpi(gdppc, rlgdp, rhgdp): return log(gdppc / rlgdp) / log(rhgdp / rlgdp)
    h.add_edge(f_gdpi, gdpi, [gdppc, RLGDP, RHGDP])

    h.add_edge(f_tab1, gdppc, [GDPPC, iopc, GDPU])

    def f_hef(alggha, ulgha, algha, tl): return (alggha + ulgha + algha) / tl
    h.add_edge(f_hef, hef, [alggha, ulgha, algha, TL])

    def f_algha(ppgr, hup, hgha): return ppgr * hup / hgha
    h.add_edge(f_algha, algha, [ppgr, HUP, HGHA])

    h.add_edge(div, alggha, [al, HGHA])
    h.add_edge(div, ulgha, [uil, HGHA])

##############################
# Edges linked to NodeSmooth #
##############################
h.add_edge(ehspc.f_smooth, ehspc, [hsapc, HSID])
h.add_edge(ple.f_smooth, ple, [le, LPD])
h.add_edge(diopc.f_smooth, diopc, [iopc, SAD])
h.add_edge(aiopc.f_smooth, aiopc, [iopc, IEAT])
h.add_edge(fcfpc.f_smooth, fcfpc, [fcapc, HSID])
#h.add_edge(lufd.f_smooth, lufd, [luf, LUFDT])
if version == 2003:
    h.add_edge(lyf2.f_smooth, lyf2, [lytd, TDD])
    h.add_edge(nruf2.f_smooth, nruf2, [nrtd, TDD])
    h.add_edge(ppgf2.f_smooth, ppgf2, [ptd, TDD])
h.add_edge(ppapr.f_smooth, ppapr, [ppgr, PPTD])



