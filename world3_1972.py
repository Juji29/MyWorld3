from sd import *
from multiaxes import affiche

h = Hypergraph()

TI = NodeConstant("TI", C, val=1900, hg=h)
DT = NodeConstant("DT", C, val=1, hg=h)
t = NodeStock("time", val=TI.val, hg=h)
h.add_edge(lambda x: x, t, [DT])

######################
# Constantes d'unité #
######################
RHGDP = NodeConstant("RHGDP", C, val=9508, hg=h)
RLGDP = NodeConstant("RLGDP", C, val=24, hg=h)
TL = NodeConstant("TL", C, val=1.91, hg=h)
HGHA = NodeConstant("HGHA", C, val=1e9, hg=h)
OY = NodeConstant("OY", C, val=1, hg=h)
UAGI = NodeConstant("UAGI", C, val=1, hg=h)
UP = NodeConstant("UP", C, val=1, hg=h)
GDPU = NodeConstant("GDPU", C, val=1, hg=h)

###################
# Basic functions #
###################
def prod(*l):
    out = l[0]
    for x in l[1:]:
        out = out * x
    return out

def moins(x, y): return x - y
def div(x, y): return x / y

def clip(c1, c2, ts, t):
    if t < ts : return c1
    else : return c2

def f_tab(tab, x):
    for i in range(len(tab)-1):
        if tab[i][0] == tab[0][0] and x < tab[i][0]:
            return tab[0][1]
            # raise ExceptionLowerLimit()
        if tab[i][0] == tab[-1][0] and x > tab[i][0]:
            return tab[-1][1]
            # raise ExceptionUpperLimit()
        if x == tab[i][0]:
            return k
        if tab[i][0] < x < tab[i+1][0]:
            coeff = (tab[i+1][1]-tab[i][1]) / (tab[i+1][0]-tab[i][0])
            return tab[i][1] + coeff * (x-tab[i][0])

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
pop = NodeFlow("pop", val=P1I.val+P2I.val+P3I.val+P4I.val, hg=h)

M1 = NodeConstant("M1", CT, val=([20, 0.0567], [30, 0.0366], [40, 0.0243], [50, 0.0155], [60, 0.0082], [70, 0.0023], [80, 0.001]), hg=h)
M2 = NodeConstant("M2", CT, val=([20, 0.0266], [30, 0.0171], [40, 0.011], [50, 0.0065], [60, 0.004], [70, 0.0016], [80, 0.0008]), hg=h)
M3 = NodeConstant("M3", CT, val=([20, 0.0562], [30, 0.0373], [40, 0.0252], [50, 0.0171], [60, 0.0118], [70, 0.0083], [80, 0.006]), hg=h)
M4 = NodeConstant("M4", CT, val=([20, 0.13], [30, 0.11], [40, 0.09], [50, 0.07], [60, 0.06], [70, 0.05], [80, 0.04]), hg=h)

m1 = NodeFlow("m1", val=M1.val, hg=h)
m2 = NodeFlow("m2", val=M2.val, hg=h)
m3 = NodeFlow("m3", val=M3.val, hg=h)
m4 = NodeFlow("m4", val=M4.val, hg=h)

FIFTEEN = NodeConstant("FIFTEEN", C, val=15, hg=h)
TWENTY = NodeConstant("TWENTY", C, val=20, hg=h)
THIRTY = NodeConstant("THIRTY", C, val=30, hg=h)

d1 = NodeStock("d1", hg=h)
d2 = NodeStock("d2", hg=h)
d3 = NodeStock("d3", hg=h)
d4 = NodeStock("d4", hg=h)

mat1 = NodeStock("mat1", hg=h)
mat2 = NodeStock("mat2", hg=h)
mat3 = NodeStock("mat3", hg=h)

#Related to death
d = NodeFlow("d", hg=h)
cdr = NodeFlow("cdr", hg=h)

LEN = NodeConstant("LEN", C, val=28, hg=h)
LMF = NodeConstant("LMF", CT, val=([0, 0], [1, 1], [2, 1.43], [3, 1.5], [4, 1.5], [5, 1.5]), hg=h)
LMHS1 = NodeConstant("LMHS1", CT, val=([0, 1], [20, 1.1], [40, 1.4], [60, 1.6], [80, 1.7], [100, 1.8]), hg=h)
LMHS2 = NodeConstant("LMHS2", CT, val=([0, 1], [20, 1.5], [40, 1.9], [60, 2], [80, 2], [100, 2]), hg=h)
LMP = NodeConstant("LMP", CT, val=([0, 1], [10, 0.99], [20, 0.97], [30, 0.95], [40, 0.9], [50, 0.85], [60, 0.75], [70, 0.65], [80, 0.55], [90, 0.4], [100, 0.2]), hg=h)
CMI = NodeConstant("CMI", CT, val=([0, 0.5], [200, 0.05], [400, -0.1], [600, -0.08], [800, -0.02], [1000, 0.05], [1200, 0.1], [1400, 0.15], [1600, 0.2]), hg=h)
FPU = NodeConstant("FPU", CT, val=([0, 0], [2.0e9, 0.2], [4.0e9, 0.4], [6.0e9, 0.5], [8.0e9, 0.58], [1.0e10, 0.65], [1.2e10, 0.72], [1.4e10, 0.78], [1.6e10, 0.8]), hg=h)

lmhs = NodeFlow("lmhs", hg=h)
lmf = NodeFlow("lmf", val=LMF.val, hg=h)
lmp = NodeFlow("lmp", val=LMP.val, hg=h)
cmi = NodeFlow("cmi", val=CMI.val, hg=h)
fpu = NodeFlow("fpu", val=FPU.val, hg=h)
lmc = NodeFlow("lmc", hg=h)
le = NodeStock("le", hg=h)

#Related to birth
b = NodeStock("b", hg=h)
cbr = NodeFlow("cbr", hg=h)

RLT = NodeConstant("RLT", C, val=30, hg=h)
PET = NodeConstant("PET", C, val=4000, hg=h)
MTFN = NodeConstant("MTFN", C, val=12, hg=h)
LPD = NodeConstant("LPD", C, val=20, hg=h)
ZPGT = NodeConstant("ZPGT", C, val=4000, hg=h)
DCFSN = NodeConstant("DCFSN", C, val=3.8, hg=h)
SAD = NodeConstant("SAD", C, val=20, hg=h)
#FRSNI = NodeConstant("FRSNI", C, val=0.82, hg=h)
IEAT = NodeConstant("IEAT", C, val=3, hg=h)
FCEST = NodeConstant("FCEST", C, val=4000, hg=h)

FM = NodeConstant("FM", CT, val=([0, 0], [10, 0.2], [20, 0.4], [30, 0.6], [40, 0.7], [50, 0.75], [60, 0.79], [70, 0.84], [80, 0.87]), hg=h)
FCE = NodeConstant("FCE", CT, val=([0, 0.75], [0.5, 0.85], [1, 0.9], [1.5, 0.95], [2, 0.98], [2.5, 0.99], [3, 1]), hg=h)
FRSN = NodeConstant("FRSN", CT, val=([-0.2, 0.5], [-0.1, 0.6], [0, 0.7], [0.1, 0.85], [0.2, 1]), hg=h)
SFSN = NodeConstant("SFSN", CT, val=([0, 1.25], [200, 0.94], [400, 0.715], [600, 0.59], [800, 0.5]), hg=h)
CMPLE = NodeConstant("CMPLE", CT, val=([0, 3], [10, 2.1], [20, 1.6], [30, 1.4], [40, 1.3], [50, 1.2], [60, 1.1], [70, 1.05], [80, 1]), hg=h)
FSAFC  =NodeConstant("FSAFC", CT, val=([0, 0], [2, 0.005], [4, 0.015], [6, 0.025], [8, 0.03], [10, 0.035]), hg=h)
fm = NodeFlow("fm", val=FM.val, hg=h)
fce = NodeFlow("fce", val=FCE.val, hg=h)
frsn = NodeFlow("frsn", val=FRSN.val, hg=h)
sfsn = NodeFlow("sfsn", val=SFSN.val, hg=h)
cmple = NodeFlow("cmple", val=CMPLE.val, hg=h)
fsafc = NodeFlow("fsafc", val=FSAFC.val, hg=h)

tf = NodeFlow("tf", hg=h)
mtf = NodeFlow("MTF", hg=h)
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
ICI = NodeConstant("ICI", C, val=210e9, hg=h)
ALIC = NodeConstant("ALIC", C, hg=h)
ALIC1 = NodeConstant("ALIC1", C, val=14, hg=h)
ALIC2 = NodeConstant("ALIC2", C, val=14, hg=h)
IET = NodeConstant("ICOR1", C, val=4000, hg=h)
FIOACC = NodeConstant("FIOACC", C, hg=h)
FIOAC1 = NodeConstant("FIOAC1", C, val=0.43, hg=h)
FIOAC2 = NodeConstant("FIOAC2", C, val=0.43, hg=h)
IOPCD = NodeConstant("IOPCD", C, val=400, hg=h)
PYEAR = NodeConstant("PYEAR", C, val=1995, hg=h)

FIOACV = NodeConstant("FIOACV", CT, val=([0, 0.3], [0.2, 0.32], [0.4, 0.34], [0.6, 0.36], [0.8, 0.38], [1, 0.43], [1.2, 0.73], [1.4, 0.77], [1.6, 0.81], [1.8, 0.82], [2, 0.83]), hg=h)
fioacv = NodeFlow("fioacv", val=FIOACV.val, hg=h)

iopc = NodeFlow("iopc", hg=h)
io = NodeFlow("io", hg=h)
icor = NodeFlow("icor", hg=h)
ic = NodeStock("ic", hg=h)
icdr = NodeStock("icdr", hg=h)
icir = NodeStock("icir", hg=h)
fioai = NodeFlow("fioai", hg=h)
fioac = NodeFlow("fioac", hg=h)

#Related to services
SCI = NodeConstant("SCI", C, val=144e9, hg=h)
ALSC = NodeConstant("ALSC", C, hg=h)
ALSC1 = NodeConstant("ALSC1", C, val=20, hg=h)
ALSC2 = NodeConstant("ALSC2", C, val=20, hg=h)
SCOR = NodeConstant("SCOR", C, hg=h)
SCOR1 = NodeConstant("SCOR1", C, val=1, hg=h)
SCOR2 = NodeConstant("SCOR2", C, val=1, hg=h)

ISOPC1 = NodeConstant("ISOPC1", CT, val=([0, 40], [200, 300], [400, 640], [600, 1000], [800, 1220], [1000, 1450], [1200, 1650], [1400, 1800], [1600, 2000]), hg=h)
ISOPC2 = NodeConstant("ISOPC2", CT, val=([0, 40], [200, 300], [400, 640], [600, 1000], [800, 1220], [1000, 1450], [1200, 1650], [1400, 1800], [1600, 2000]), hg=h)
FIOAS1 = NodeConstant("FIOAS1", CT, val=([0, 0.3], [0.5, 0.2], [1, 0.1], [1.5, 0.05], [2, 0]), hg=h)
FIOAS2 = NodeConstant("FIOAS2", CT, val=([0, 0.3], [0.5, 0.2], [1, 0.1], [1.5, 0.05], [2, 0]), hg=h)
isopc1 = NodeFlow("ispoc1", val=ISOPC1.val, hg=h)
isopc2 = NodeFlow("ispoc2", val=ISOPC2.val, hg=h)
fioas1 = NodeFlow("fioas1", val=FIOAS1.val, hg=h)
fioas2 = NodeFlow("fioas2", val=FIOAS2.val, hg=h)

isopc = NodeFlow("ispoc", hg=h)
fioas = NodeFlow("fioas", hg=h)
scir = NodeStock("scir", hg=h)
sc = NodeStock("sc", hg=h)
scdr = NodeStock("scdr", hg=h)
so = NodeFlow("so", hg=h)
sopc = NodeFlow("sopc", hg=h)

#Related to jobs
LFPF = NodeConstant("LFPF", C, val=0.75, hg=h)
LUFDT = NodeConstant("LUFDT", C, val=2, hg=h)
#CUFI = NodeConstant("CUFI", C, val=1, hg=h)

JPICU = NodeConstant("JPICU", CT, val=([50, 0.37], [200, 0.18], [350, 0.12], [500, 0.09], [650, 0.07], [800, 0.06]), hg=h)
JPSCU = NodeConstant("JPSCU", CT, val=([50, 1.1], [200, 0.6], [350, 0.35], [500, 0.2], [650, 0.15], [800, 0.15]), hg=h)
JPH = NodeConstant("JPH", CT, val=([2, 2], [6, 0.5], [10, 0.4], [14, 0.3], [18, 0.27], [22, 0.24], [26, 0.2], [30, 0.2]), hg=h)
CUF = NodeConstant("CUF", CT, val=([1, 1], [3, 0.9], [5, 0.7], [7, 0.3], [9, 0.1], [11, 0.1]), hg=h)
jpicu = NodeFlow("jpicu", val=JPICU.val, hg=h)
jpscu = NodeFlow("jpscu", val=JPSCU.val, hg=h)
jph = NodeFlow("jph", val=JPH.val, hg=h)
cuf = NodeFlow("cuf", val=CUF.val, hg=h)

j = NodeFlow("j", hg=h)
pjis = NodeFlow("pjis", hg=h)
pjss = NodeFlow("pjss", hg=h)
pjas = NodeFlow("pjas", hg=h)
lf = NodeFlow("lf", hg=h)
luf = NodeFlow("luf", hg=h)

##################################
# Variables close to agriculture #
##################################
#Loop 1
PALT = NodeConstant("PALT", C, val=3.2e9, hg=h)
ALI = NodeConstant("ALI", C, val=0.9e9, hg=h)
PALI = NodeConstant("PALI", C, val=2.3e9, hg=h)
LFH = NodeConstant("LFH", C, val=0.7, hg=h)
PL = NodeConstant("PL", C, val=0.1, hg=h)

IFPC1 = NodeConstant("IFPC1", CT, val=([0, 230], [200, 480], [400, 690], [600, 850], [800, 970], [1000, 1070], [1200, 1150], [1400, 1210], [1600, 1250]), hg=h)
IFPC2 = NodeConstant("IFPC2", CT, val=([0, 230], [200, 480], [400, 690], [600, 850], [800, 970], [1000, 1070], [1200, 1150], [1400, 1210], [1600, 1250]), hg=h)
FIOAA1 = NodeConstant("FIOAA1", CT, val=([0, 0.4], [0.5, 0.2], [1, 0.1], [1.5, 0.025], [2, 0], [2.5, 0]), hg=h)
FIOAA2 = NodeConstant("FIOAA2", CT, val=([0, 0.4], [0.5, 0.2], [1, 0.1], [1.5, 0.025], [2, 0], [2.5, 0]), hg=h)
DCPH = NodeConstant("DCPH", CT, val=([0, 10000], [0.1, 7400], [0.2, 5200], [0.3, 3500], [0.4, 2400], [0.5, 1500], [0.6, 750], [0.7, 300], [0.8, 150], [0.9, 75], [1, 50]), hg=h)
ifpc1 = NodeFlow("ifpc1", val=IFPC1.val,  hg=h)
ifpc2 = NodeFlow("ifpc2", val=IFPC2.val, hg=h)
fioaa1 = NodeFlow("fioaa1", val=FIOAA1.val, hg=h)
fioaa2 = NodeFlow("fioaa2", val=FIOAA2.val, hg=h)
dcph = NodeFlow("dcph", val=DCPH.val, hg=h)

lfc = NodeFlow("lfc", hg=h)
al = NodeStock("al", hg=h)
pal = NodeStock("pal", hg=h)
f = NodeFlow("f", hg=h)
fpc = NodeFlow("fpc", hg=h)
ifpc = NodeFlow("ifpc", hg=h)
tai = NodeFlow("tai", hg=h)
fioaa = NodeFlow("fioaa", hg=h)
ldr = NodeStock("ldr", hg=h)

#Loop 2
#AII = NodeConstant("AII", C, val=5e9, hg=h)
ALAI = NodeConsatnt("ALAI", C, hg=h)
ALAI1 = NodeConstant("ALAI1", C, val=2, hg=h)
ALAI2 = NodeConstant("ALAI2", C, val=2, hg=h)
LYF1 = NodeConstant("LYF1", C, val=1, hg=h)
IO70 = NodeConstant("IO70", C, val=790e9, hg=h)
#SD = NodeConstant("SD", C, val=0.07, hg=h)
TDD = NodeConstant("TDD", C, val=20, hg=h)

LYMC = NodeConstant("LYMC", CT, val=([0, 1], [40, 3], [80, 4.5], [120, 5], [160, 5.3], [200, 5.6], [240, 5.9], [280, 6.1], [320, 6.35], [360, 6.6], [400, 6.9], [440, 7.2], [480, 7.4], [520, 7.6], [560, 7.8], [600, 8], [640, 8.2], [680, 8.4], [720, 8.6], [760, 8.8], [800, 9], [840, 9.2], [880, 9.4], [920, 9.6], [960, 9.8], [1000, 10]), hg=h)
LYMAP1 = NodeConstant("LYMAP1", CT, val=([0, 1], [10, 1], [20, 0.7], [30, 0.4]), hg=h)
LYMAP2 = NodeConstant("LYMAP2", CT, val=([0, 1], [10, 1], [20, 0.98], [30, 0.95]), hg=h)
FIALD = NodeConstant("FIALD", CT, val=([0, 0], [0.25, 0.05], [0.5, 0.15], [0.75, 0.3], [1, 0.5], [1.25, 0.7], [1.5, 0.85], [1.75, 0.95], [2, 1]), hg=h)
MLYMC = NodeConstant("MLYMC", CT, val=([0, 0.075], [40, 0.03], [80, 0.015], [120, 0.011], [160, 0.009], [200, 0.008], [240, 0.007], [280, 0.006], [320, 0.005], [360, 0.005], [400, 0.005], [440, 0.005], [480, 0.005], [520, 0.005], [560, 0.005], [600, 0.005]), hg=h)
lymc = NodeFlow("lymc", val=LYMC.val, hg=h)
lymap = NodeFlow("lymap", hg=h)
lymap1 = NodeFlow("lymap1", val=LYMAP1.val, hg=h)
lymap2 = NodeFlow("lymap2", val=LYMAP2.val, hg=h)
fiald = NodeFlow("fiald", val=FIALD.val, hg=h)
mlymc = NodeFlow("mlymc", val=MLYMC.val, hg=h)

cai = NodeFlow("cai", hg=h)
aiph = NodeFlow("aiph", hg=h)
ly = NodeFlow("ny", hg=h)
lyf = NodeFlow("lyf", hg=h)
mpld = NodeFlow("mpld", hg=h)
mpai = NodeFlow("mpai", hg=h)

#Loop 3
ALLN = NodeConstant("ALLN", C, val=1000, hg=h)
UILDT = NodeConstant("UILDT", C, val=10, hg=h)
UILI = NodeConstant("UILI", C, val=8200000, hg=h)
LLMYTM = NodeConstant("LLMYTM", C, val=4000, hg=h)

LLMY1 = NodeConstant("LLMY1", CT, val=([0, 1.2], [1, 1], [2, 0.63], [3, 0.36], [4, 0.16], [5, 0.055], [6, 0.04], [7, 0.025], [8, 0.015], [9, 0.01]), hg=h)
LLMY2 = NodeConstant("LLMY2", CT, val=([0, 1.2], [1, 1], [2, 0.63], [3, 0.36], [4, 0.29], [5, 0.26], [6, 0.24], [7, 0.22], [8, 0.21], [9, 0.2]), hg=h)
UILPC = NodeConstant("UILPC", CT, val=([0, 0.005], [200, 0.008], [400, 0.015], [600, 0.025], [800, 0.04], [1000, 0.055], [1200, 0.07], [1400, 0.08], [1600, 0.09]), hg=h)
llmy = NodeFlow("llmy", hg=h)
llmy1 = NodeFlow("llmy1", val=LLMY1.val, hg=h)
llmy2 = NodeFlow("llmy2", val=LLMY2.val, hg=h)
uilpc = NodeFlow("uilpc", val=UILPC.val, hg=h)

all = NodeFlow("all", hg=h)
ler = NodeStock("ler", hg=h)
uilr = NodeFlow("uilr", hg=h)
lrui = NodeStock("lrui", hg=h)
uil = NodeStock("uil", hg=h)

#Loop 4
LFERTI = NodeConstant("LFERTI", C, val=600, hg=h)

LFDR = NodeConstant("LFDR", CT, val=([0, 0], [10, 0.1], [20, 0.3], [30, 0.5]), hg=h)
lfdr = NodFlow("lfdr", hg=h)

lfert = NodeStock("lfert", hg=h)
lfd = NodeStock("lfd", hg=h)

#Loop 5
ILF = NodeConstant("ILF", C, val=600, hg=h)
SFPC = NodeConstant("SFPC", C, val=230, hg=h)
PFRI = NodeConstant("PFRI", C, val=1, hg=h) #TODO Utilisé comme initialisation de SMOOTH
FSDP = NodeConstant("FSDP", C, val=2, hg=h)

LFRT = NodeConstant("LFRT", CT, val=([0, 20], [0.02, 13], [0.04, 8], [0.06, 4], [0.08, 2], [0.1, 2]), hg=h)
FALM = NodeConstant("FALM", CT, val=([0, 0], [1, 0.04], [2, 0.07], [3, 0.09], [4, 0.1]), hg=h)
lfrt = NodeFlow("lfrt", val=LFRT.val, hg=h)
falm = NodeFlow("falm", val=FALM.val, hg=h)

lfr = NodeStock("lfr", hg=h)
fr = NodeFlow("fr", hg=h)

################################
# Variables close to resources #
################################
NRI = NodeConstant("NRI", C, val=1e12, hg=h)
NRUF1 = NodeConstant("NRUFI", C, val=1, hg=h)
FCAORTM = NodeConstant("FCAORTM", C, val=4000, hg=h)

PCRUM = NodeConstant("PCRUM", CT, val=([0, 0], [200, 0.85], [400, 2.6], [600, 3.4], [800, 3.8], [1000, 4.1], [1200, 4.4], [1400, 4.7], [1600, 5]), hg=h)
FCAOR1 = NodeConstant("FCAOR1", CT, val=([0, 1], [0.1, 0.9], [0.2, 0.7], [0.3, 0.5], [0.4, 0.2], [0.5, 0.1], [0.6, 0.05], [0.7, 0.05], [0.8, 0.05], [0.9, 0.05], [1, 0.05]), hg=h)
FCAOR2 = NodeConstant("FCAOR2", CT, val=([0, 1], [0.1, 0.2], [0.2, 0.1], [0.3, 0.05], [0.4, 0.05], [0.5, 0.05], [0.6, 0.05], [0.7, 0.05], [0.8, 0.05], [0.9, 0.05], [1, 0.05]), hg=h)
pcrum = NodeFlow("pcrum", hg=h)
fcaor = NodeFlow("fcaor", hg=h)
fcaor1 = NodeFlow("fcaor1", val=FCAOR1.val, hg=h)
fcaor2 = NodeFlow("fcaor2", val=FCAOR2.val, hg=h)

nr = NodeStock("nr", hg=h)
nrur = NodeStock("nrur", hg=h)
nruf = NodeFlow("nruf", hg=h)
nrfr = NodeFlow("nrfr", hg=h)

################################
# Variables close to pollution #
################################
PPGF1 = NodeConstant("PPGF1", C, val=1, hg=h)
#FRPM = NodeConstant("FRPM", C, val=0.02, hg=h)
IMEF = NodeConstant("IMEF", C, val=0.1, hg=h)
IMTI = NodeConstant("IMTI", C, val=10, hg=h)
FIPM = NodeConstant("FIPM", C, val=0.001, hg=h)
AMTI = NodeConstant("AMTI", C, val=1, hg=h)
PPTD = NodeConstant("PPTD", C, val=20, hg=h)
PPOLI = NodeConstant("PPOLI", C, val=25e6, hg=h)
PPOLI70 = NodeConstant("PPOLI70", C, val=136e6, hg=h)
AHL70 = NodeConstant("AHL70", C, val=1.5, hg=h)

AHLM = NodeConstant("AHLM", CT, val=([1, 1], [251, 11], [501, 21], [751, 31], [1001, 41]), hg=h)
ahlm = NodeFlow("ahlm", val=AHLM.val, hg=h)

ppgr = NodeStock("ppgr", hg=h)
ppgf = NodeFlow("ppgf", hg=h)
ppgio = NodeFlow("ppgio", hg=h)
ppgao = NodeFlow("ppgao", hg=h)
ppol = NodeStock("ppol", hg=h)
ppolx = NodeFlow("ppolx", hg=h)
ppasr = NodeStock("ppasr", hg=h)
ahl = NodeFlow("ahl", hg=h)

####################
# Smooth functions #
####################
ple = NodeSmooth("ple", SMOOTH3, 200, le, LPD)
diopc = NodeSmooth("diopc", SMOOTH3, 200, iopc, SAD)
aiopc = NodeSmooth("aiopc", SMOOTH, 200, iopc, IEAT)
fcfpc = NodeSmooth("fcfpc", SMOOTH3, 200, fcapc, HSID)
lufd = NodeSmooth("lufd", SMOOTHI, 200, luf, LUFDT, 1)
ai = NodeSmooth("ai", SMOOTH, 200, cai, ALAI)
lyf2 = NodeSmooth("lyf2", SMOOTH3, 200, lytd, TDD)
pfr = NodeSmooth("pfr", SMOOTHI, 200, fr, FSPD, PFRI) # TODO choice Smooth or Smoothi
nruf2 = NodeSmooth("nruf2", SMOOTH3, 200, nrtd, TDDD)
ppgf2 = NodeSmooth("ppgf2", SMOOTH3, 200, ptd, TDD)
ppapr = NodeSmooth("ppapr", DELAY3, 200, ppgr, PPTD)
#######################
# Edges on population #
#######################
def f_mat(p, m, n):
    return div(prod(p, moins(1, m)), n)

h.add_edge(prod, d1, [p1, m1])
h.add_edge(prod, d2, [p2, m2])
h.add_edge(prod, d2, [p3, m3])
h.add_edge(prod, d4, [p4, m4])

h.add_edge(f_mat, mat1, [p1, m1, FIFTEEN])
h.add_edge(f_mat, mat2, [p2, m2, THIRTY])
h.add_edge(f_mat, mat3, [p3, m3, TWENTY])

h.add_edge(f_tab, m1, [M1, div(le, OY)])
h.add_edge(f_tab, m2, [M2, div(le, OY)])
h.add_edge(f_tab, m3, [M3, div(le, OY)])
h.add_edge(f_tab, m4, [M4, div(le, OY)])

def p1_evo(b, d1, mat1):
    return moins(moins(b, d1), mat1)
def p2_evo(mat1, d2, mat2):
    return moins(moins(mat1, d2), mat2)
def p3_evo(mat2, d3, mat3):
    return moins(moins(mat2, d3), mat3)
def p4_evo(mat3, d4):
    return moins(mat3, d4)

h.add_edge(p1_evo, p1, [b, d1, mat1])
h.add_edge(p2_evo, p2, [mat1, d2, mat2])
h.add_edge(p3_evo, p3, [mat2, d3, mat3])
h.add_edge(p4_evo, p4, [mat3, d4])


def f_cdr(d, pop): return 1000*d/pop
h.add_edge(f_cdr, cdr, [d, pop])

h.add_edge(f_tab, lmf, [LMF, div(fpc, SFPC)])

def f_lmhs(lmhs1, lmhs2, t): return clip(LMHS1_val, LMHS2_val, 1940, t.val)
def f_lmc(cmi, fpu): return moins(1, prod(cmi, fpu))
def f_le(len, lmf, lmhs, lmp, lmc): return prod(len, lmf, lmhs, lmp, lmc)

h.add_edge(f_lmhs, lmhs, [LMHS1, LMHS2, t])
h.add_edge(f_lmc, lmc, [cmi, fpu])
h.add_edge(f_le, le, [LEN, lmf, lmhs, lmp, lmc])

def f_mtf(mtfn, fm): return prod(mtfn, fm)
h.add_edge(f_mtf, mtf, [MTFN, FM])

def f_dcfs(dcfsn, frsn, sfsn, zpgt): return clip(2, dcfsn.val*prod(frsn, sfsn), t.val, zpgt.val)
h.add_edge(f_dcfs, dcfs, [dtf, DCFSN, FRSN, SFSN, ZPGT])

def f_dtf(dcfs, cmple): return prod(dcfs, cmple)
h.add_edge(f_dtf, dtf, [dcfs, CMPLE])

def f_tf(mtf, fce, dtf): return min(mtf, prod(mtf, moins(1, fce))+prod(dtf, fce))
h.add_edge(f_tf, tf, [mtf, FCE, dtf])

def f_b(d, t, pet, tf, p2, rlt):
    if t >= pet:
        return d
    else:
        return div(0.5*prod(tf, p2), rlt)
h.add_edge(f_b, b, [d, t.val, PET, tf, p2, RLT])

def f_cbr(b, pop): return 1000*b/pop
h.add_edge(f_cbr, cbr, [b, pop])





