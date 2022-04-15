import numpy as np
from scipy.integrate import solve_ivp, odeint
import matplotlib.pyplot as plt
from sd import *
from multiaxes import affiche

class ExceptionLowerLimit(Exception): pass
class ExceptionUpperLimit(Exception): pass

h = Hypergraph()

TI = Node(C, "TI", hg=h, val=1900)
DT = Node(C, "DT", val=1, hg=h)
t = Node(T, "time", hg=h, val=TI.val)
h.add_edge(lambda x: x, t, [DT])

######################################
# Variables proches de la population #
######################################
PI = Node(C, 'PI', val=1.65e9, hg=h)
p = Node(T, "p", val=PI.val, hg=h)

br = Node(N, "br", hg=h)
brfm = Node(N, "brfm", hg=h)
brpm = Node(N, "brpm", hg=h)
brmm = Node(N, "brmm", hg=h)
brcm = Node(N, "brcm", hg=h)
BRN0 = Node(C, "BRN0", val=0.04, hg=h)
BRN1 = Node(C, "BRN1", val=0.04, hg=h)
SWT1 = Node(C, "SWT0", val=1970, hg=h)

dr = Node(N, "dr", hg=h)
drfm = Node(N, "drfm", hg=h)
drpm = Node(N, "drpm", hg=h)
drmm = Node(N, "drmm", hg=h)
drcm = Node(N, "drcm", hg=h)
DRN0 = Node(C, "DRN0", val=0.028, hg=h)
DRN1 = Node(C, "DRN1", val=0.028, hg=h)
SWT3 = Node(C, "SWT3", val=1970, hg=h)

def prod(*l):
    out = l[0]
    for x in l[1:]:
        out = out * x
    return out
    
def div(x,y): return x / y
def moins(x,y): return x - y
    
def clip(c1, c2, ts, t):
    if t < ts : return c1
    else : return c2
    
def f_br(p, B0, B1, S, bf, bm, bc, bp, t):
    return prod(p,clip(B0,B1,S,t), bf, bm, bc, bp)

h.add_edge(moins, p, [br, dr])
h.add_edge(f_br, br, [p, BRN0, BRN1, SWT1, brfm, brmm, brcm, brpm, t])
h.add_edge(f_br, dr, [p, DRN0, DRN1, SWT3, drfm, drmm, drcm, drpm, t])

msl = Node(N, "msl", hg=h)
fr = Node(N, "fr", hg=h)
cr = Node(N, "cr", hg=h)
polr = Node(N, "polr", hg=h)
BRMMT = Node(CT, "BRMMT", val=([0,5,1],[1.2,1,0.85,0.75,0.7,0.7]), hg=h)
BRFMT = Node(CT, "BRFMT", val=([0,4,1],[0,1,1.6,1.9,2]), hg=h)
BRCMT = Node(CT, "BRCMT", val=([0,5,1],[1.05,1,0.9,0.7,0.6,0.55]), hg=h)
BRPMT = Node(CT, "BRPMT", val=([0,60,10],[1.02,0.9,0.7,0.4,0.25,0.15,0.1]), hg=h)
DRMMT = Node(CT, "DRMMT", val=([0,5,0.5],[3,1.8,1,0.8,0.7,0.6,0.53,0.5,0.5,0.5,0.5]), hg=h)
DRFMT = Node(CT, "DRFMT", val=([0,2,0.25],[30,3,2,1.4,1,0.7,0.6,0.5,0.5]), hg=h)
DRCMT = Node(CT, "DRCMT", val=([0,5,1],[0.9,1,1.2,1.5,1.9,3]), hg=h)
DRPMT = Node(CT, "DRPMT", val=([0,60,10],[0.92,1.23,2,3.2,4.8,6.8,9.2]), hg=h)

def f_tab(tab, x):
    xmin, xmax, pas = tab[0]
    y = tab[1]
    n = len(y)
    i = int((x-xmin)/pas)
    if x < xmin :
        i = 0
        #raise ExceptionLowerLimit()
    if x >= xmax :
        i = n - 2
        #raise ExceptionUpperLimit()
    xi = xmin + i*pas
    coeff = (y[i+1]-y[i]) / pas
    return y[i] + coeff * (x-xi)

h.add_edge(f_tab, brmm, [BRMMT, msl])
h.add_edge(f_tab, brfm, [BRFMT, fr])
h.add_edge(f_tab, brcm, [BRCMT, cr])
h.add_edge(f_tab, brpm, [BRPMT, polr])

h.add_edge(f_tab, drmm, [DRMMT, msl])
h.add_edge(f_tab, drfm, [DRFMT, fr])
h.add_edge(f_tab, drcm, [DRCMT, cr])
h.add_edge(f_tab, drpm, [DRPMT, polr])

LA = Node(C, "LA", val=135e6, hg=h)
PDN = Node(C, "PDN", val=26.5, hg=h)
def f_cr(p,l,pd) : return p/l/pd
h.add_edge(f_cr, cr, [p, LA, PDN])

################################
# Variables proches du capital #
################################
CII = Node(C,"CI0", val=0.4e9, hg=h)
ci = Node(T, "ci", hg=h, val=CII.val)

ecir = Node(N, "ecir", hg=h)
cir = Node(N, "cir", hg=h)
CIAFI = Node(C, "CIAFI", hg=h, val=0.2)
ciaf = Node(T, "ciaf", hg=h, val=CIAFI.val)
nrem = Node(N, "nrem", hg=h)
cig = Node(N, "cig", hg=h)
cim = Node(N, "cim", hg=h)
cid = Node(N, "cid", hg=h)

ECRIN = Node(C, "ECRIN", val=1, hg=h)
CIAFN = Node(C, "CIAFN", val=0.3, hg=h)
CIGN0 = Node(C, "CIGN0", val=0.05, hg=h)
CIGN1 = Node(C, "CIGN1", val=0.05, hg=h)
SWT4 = Node(C, "SWT4", val=1970, hg=h)
CIDN0 = Node(C, "CIDN0", val=0.025, hg=h)
CIDN1 = Node(C, "CIDN1", val=0.025, hg=h)
SWT5 = Node(C, "SWT5", val=1970, hg=h)

CIMT = Node(C, "CIMT", val=([0,5,1],[0.1, 1, 1.8, 2.4, 2.8, 3]))

h.add_edge(div, msl, [ecir, ECRIN])
def f_ecir(cir, nrem, ciaf, CIAFN):
    return cir * nrem * (1 - ciaf) / (1 - CIAFN)
h.add_edge(f_ecir, ecir, [cir, nrem, ciaf, CIAFN])
h.add_edge(div, cir, [ci, p])
h.add_edge(moins, ci, [cig, cid])
def f_cig(p, cim, CIGN0, CIGN1, SWT4, t):
    return prod(p, cim, clip(CIGN0, CIGN1, SWT4, t))
h.add_edge(f_cig, cig, [p, cim, CIGN0, CIGN1, SWT4, t])
def f_cid(ci, CIGN0, CIGN1, SWT4, t):
    return prod(ci, clip(CIGN0, CIGN1, SWT4, t))
h.add_edge(f_cid, cid, [ci, CIDN0, CIDN1, SWT5, t])

h.add_edge(f_tab, cim, [CIMT, msl])

##############################################
# variables proches des ressouces naturelles #
##############################################
NRI = Node(C, "NRI", val=900e9, hg=h)
nr = Node(T, "nr", hg=h, val=NRI.val)

nrfr = Node(N, "nrfr", hg=h)
nrur = Node(N, "nrur", hg=h)
nrmm = Node(N, "nrmm", hg=h)


NRUR0 = Node(C, "NRUR0", val=1, hg=h)
NRUR1 = Node(C, "NRUR1", val=1, hg=h)
SWT2 = Node(C, "SWT2", val=1970, hg=h)

NREMT = Node(CT, "NREMT", val=([0,1,0.25],[0, 0.15, 0.5, 0.85, 1]))
NRMMT = Node(CT, "NRMMT", val=([0,10,1],[0, 1, 1.8, 2.4, 2.9, 3.3, 3.6, 3.8, 3.9, 3.95, 4]))

h.add_edge(f_tab, nrem, [NREMT, nrfr])
h.add_edge(div, nrfr, [nr, NRI])
h.add_edge(lambda x: -x, nr, [nrur])
def f_nrur(p, NRUR0,NRUR1, SWT2, t, nrmm):
    return prod(p, clip(NRUR0,NRUR1, SWT2, t), nrmm)
h.add_edge(f_nrur, nrur, [p, NRUR0,NRUR1, SWT2, t, nrmm])
h.add_edge(f_tab, nrmm, [NRMMT, msl])

######################################
# Variables proches de l'agriculture #
######################################
CIAFT = Node(C, "CIAFT", val=15, hg=h)
FC0 = Node(C, "FC0", val=1, hg=h)
FC1 = Node(C, "FC1", val=1, hg=h)
FN = Node(C, "FN", val=1, hg=h)
SWT7 = Node(C, "SWT7", val=1970, hg=h)

CFIFRT = Node(CT, "CFIFRT", val=([0,2,0.5],[1, 0.6, 0.3, 0.15, 0.1]))
FPCIT = Node(CT, "FPCIT", val=([0,6,1],[0.5, 1, 1.4, 1.7, 1.9, 2.05, 2.2]))
FCMT = Node(CT, "FCMT", val=([0,5,1],[2.4, 1, 0.6, 0.4, 0.3, 0.2]))
FPMT = Node(CT, "FPMT", val=([0,60,10],[1.02, 0.9, 0.65, 0.35, 0.2, 0.1, 0.05]))

cfifr = Node(N, "cfifr", hg=h)
ciqr = Node(N, "ciqr", hg=h)
fpci = Node(N, "fpci", hg=h)
fcm = Node(N, "fcm", hg=h)
fpm = Node(N, "fpm", hg=h)
cira = Node(N, "cira", hg=h)

def f_ciaf(cfifr, ciqr, ciaf, CIAFT):
    return (cfifr * ciqr - ciaf) / CIAFT
h.add_edge(f_ciaf, ciaf, [cfifr, ciqr, ciaf, CIAFT])
h.add_edge(f_tab, cfifr, [CFIFRT, fr])
def f_fr(fpci, fcm, fpm, FC0, FC1, SWT7, t, FN):
    return prod(fpci, fcm, fpm, clip(FC0, FC1, SWT7, t) / FN)
h.add_edge(f_fr, fr, [fpci, fcm, fpm, FC0, FC1, SWT7, t, FN])
h.add_edge(f_tab, fpci, [FPCIT, cira])
h.add_edge(f_tab, fcm, [FCMT, cr])
h.add_edge(f_tab, fpm, [FPMT, polr])
def f_cira(cir, ciaf, CIAFN): return cir * ciaf / CIAFN
h.add_edge(f_cira, cira, [cir, ciaf, CIAFN])

##########################################
# Variables proches de la qualité de vie #
##########################################
QLS = Node(C, "QLS", val=1, hg=h)

CIQRT = Node(CT, "CIQRT", val=([0,2,0.5],[0.7, 0.8, 1, 1.5, 2]))
QLMT = Node(CT, "QLMT", val=([0,5,1],[0.2, 1, 1.7, 2.3, 2.7, 2.9]))
QLFT = Node(CT, "QLFT", val=([0,4,1],[0, 1, 1.8, 2.4, 2.7]))
QLPT = Node(CT, "QLPT", val=([0,60,10],[1.04, 0.85, 0.6, 0.3, 0.15, 0.05, 0.02]))
QLCT = Node(CT, "QLCT", val=([0,5,0.5],[2, 1.3, 1, 0.75, 0.55, 0.45, 0.38, 0.3, 0.25, 0.22, 0.2]))

qlm = Node(N, "qlm", hg=h)
qlf = Node(N, "qlf", hg=h)
qlp = Node(N, "qlp", hg=h)
qlc = Node(N, "qlc", hg=h)
ql = Node(N, "ql", hg=h)

def f_ciqr(CIQRT, qlm, qlf): return f_tab(CIQRT, qlm / qlf)
h.add_edge(f_ciqr, ciqr, [CIQRT, qlm, qlf])
h.add_edge(f_tab, qlm, [QLMT, msl])
h.add_edge(f_tab, qlf, [QLFT, fr])
h.add_edge(f_tab, qlp, [QLPT, polr])
h.add_edge(f_tab, qlc, [QLCT, cr])
h.add_edge(prod, ql, [QLS, qlm, qlc, qlf, qlp])

#####################################
# Variables proches de la pollution #
#####################################
POLI = Node(C, "POLI", val=0.2e9, hg=h)
POLS = Node(C, "POLS", val=3.6e9, hg=h)
POLN0 = Node(C, "POLN0", val=1, hg=h)
POLN1 = Node(C, "POLN1", val=1, hg=h)
SWT6 = Node(C, "SWT6", val=1, hg=h)

POLATT = Node(CT, "POLATT", val=([0, 60, 10],[0.6, 2.5, 5, 8, 11.5, 15.5, 20]))
POLCMT = Node(CT, "POLCMT", val=([0, 5, 1],[0.05, 1, 3, 5.4, 7.4, 8]))

pol = Node(T, "pol", hg=h, val=POLI.val)
polg = Node(N, "polg", hg=h)
pola = Node(N, "pola", hg=h)
polcm = Node(N, "polcm", hg=h)
polat = Node(N, "polat", hg=h)

h.add_edge(div, polr, [pol, POLS])
h.add_edge(moins, pol, [polg, pola])
def f_polg(p, POLN0,POLN1, SWT6, t, polcm):
    return prod(p, clip(POLN0,POLN1, SWT6, t), polcm)
h.add_edge(f_polg, polg, [p, POLN0,POLN1, SWT6, t, polcm])
h.add_edge(div, pola, [pol, polat])
h.add_edge(f_tab, polat, [POLATT, polr])
h.add_edge(f_tab, polcm, [POLCMT, cir])

print(h)
h.set_rank()
for i,xi in enumerate(h.nodesrank):
    print("niveau {} :".format(i), end='')
    for x in xi:
        print(" {}".format(x.name), end='')
    print()

t0, tf = 1900, 2100
time = [t0, tf]
#y0 = np.array([1, 2])

#time, p, ci, ciaf, nr, pol
label1 = ['année', 'population', 'capital', 'capital agriculture', 'ressources', 'polution']
#print(TI.val, PI.val, CII.val, CIAFI.val, NRI.val, POLI.val, flush=True)
y0 = np.array([TI.val, PI.val, CII.val, CIAFI.val, NRI.val, POLI.val])

#sol = solve_ivp(h.eval2, time, y0, dense_output=True)

nbpas = 201
dt = 1#0.5
#timeee = np.linspace(t0, tf, nbpas)
#y = y0
#record = []
#print(y0)
#for i, ti in enumerate(timeee):
#    record.append(y)
#    dy = h.eval2(ti, y)
#    y = y + dy*dt
#    print("{}:\n{}\n{}".format(i, y, dy))

def traj_rungeKutta(x0, f, nbIter, pas):
    nbVar = len(x0)
    x = np.zeros((nbVar,nbIter),float)
    x[:,0] = x0
    for k in range(nbIter-1):
        k1 = f(k,x[:,k])
        k2 = f(k,x[:,k] + pas / 2 * k1)
        k3 = f(k,x[:,k] + pas / 2 * k2)
        k4 = f(k,x[:,k] + pas * k3)
        x[:,k+1] = x[:,k] + pas / 6. * (k1 + 2*k2 + 2*k3 + k4)
    return x

nbVar = len(y0)

sol = traj_rungeKutta(y0, h.eval2, nbpas, dt)
#sol = solve_ivp(h.eval2, time, y0, dense_output=True)
#timee = np.arange(t0, tf, dt)
#sol = odeint(h.eval2, y0, timee)
#sol = sol.transpose()

#fig, ax1 = plt.subplots()
#for i in range(1,nbVar):
#    axi = ax1.twinx()
#    axi.plot(sol[i,:], label=label1[i])
#    plt.legend()


n = nbVar - 1
x = [range(t0, tf+1) for _ in range(n)]
y = [sol[i,:] for i in range(1, n+1)]
ymax = [max(sol[i,:])*1.1 for i in range(1, n+1)]
ymin = [0] * n
#ymax = [PI.val*5, CII.val*30, CIAFI.val*2, NRI.val, POLI.val*150]
xmin, xmax = t0, tf
labelX = "time"
labelY = label1[1:]
tx = 0.7
affiche(x, y, xmin, xmax, ymin, ymax, labelX, labelY, tx)

#print(record)
#yr = np.array(record)
#y = sol.sol(timeee)
#print(timeee)
#plt.plot(timeee[:150], yr.T[1][:150])
#plt.plot(time, y.T)
#plt.xlabel('time')
#plt.legend(['proies', 'prédateurs'], shadow=True)
#plt.title('Lotka-Volterra System')
#plt.show()
