import world3_graph as w3
from world3_plot import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #########
    # Solve #
    #########
    w3.h.set_rank()
    w3.h.run(w3.nbpas, w3.TS.val)

#################################
# Reading and analysing results #
#################################
ppolx_ref = read("Resultats_ref/Pyworld3/ppolx")
pop_ref = read("Resultats_ref/Pyworld3/pop")
fpc_ref = read("Resultats_ref/Pyworld3/fpc")
iopc_ref = read("Resultats_ref/Pyworld3/iopc")
nrfr_ref = read("Resultats_ref/Pyworld3/nrfr")

fioaa_ref = read("Resultats_ref/Pyworld3/fioaa")
aiph_ref = read("Resultats_ref/Pyworld3/aiph")
tai_ref = read("Resultats_ref/Pyworld3/tai")
io_ref = read("Resultats_ref/Pyworld3/io")
fcaor_ref = read("Resultats_ref/Pyworld3/fcaor")

lmf_ref = read("Resultats_ref/Pyworld3/lmf")
al_ref = read("Resultats_ref/Pyworld3/al")
ly_ref = read("Resultats_ref/Pyworld3/ly")

ai_ref = read("Resultats_ref/Pyworld3/ai")

delta_ppolx = comparaison(w3.ppolx.hist, ppolx_ref)
delta_pop = comparaison(w3.pop.hist, pop_ref)
delta_fpc = comparaison(w3.fpc.hist, fpc_ref)
delta_iopc = comparaison(w3.iopc.hist, iopc_ref)
delta_nrfr = comparaison(w3.nrfr.hist, nrfr_ref)

delta_fioaa = comparaison(w3.fioaa.hist, fioaa_ref)
delta_aiph = comparaison(w3.aiph.hist, aiph_ref)
delta_tai = comparaison(w3.tai.hist, tai_ref)
delta_io = comparaison(w3.io.hist, io_ref)
delta_fcaor = comparaison(w3.fcaor.hist, fcaor_ref)

delta_lmf = comparaison(w3.lmf.hist, lmf_ref)
delta_al = comparaison(w3.al.hist, al_ref)
delta_ly = comparaison(w3.ly.hist, ly_ref)

delta_ai = comparaison(w3.ai.hist, ai_ref)

# ploting and printing gaps between real results and historical ones
label_gap = ["Delta POP", "Delta FPC", "Delta IOPC", "Delta NRFR", "Delta FIOAA", "Delta AIPH", "Delta TAI",
             "Delta IO", "Delta FCAOR", "Delta LMF", "Delta AL", "Delta LY"]
sol_gap = [delta_pop, delta_fpc, delta_iopc, delta_nrfr, delta_fioaa, delta_aiph, delta_tai, delta_io, delta_fcaor,
           delta_lmf, delta_al, delta_ly]
sol_min_gap = [min(elt) for elt in sol_gap]
sol_max_gap = [max(elt) for elt in sol_gap]
afficherreur(w3.t.hist, sol_gap, label_gap)
gap_tot = 0
for var in sol_gap:
    for i in var:
        gap_tot += abs(i)
print(gap_tot/200/12)


######################
# Plots of variables #
######################
params = {'lines.linewidth': '3'}
plt.rcParams.update(params)
#standard_run_overview
stand_aff(w3.t.hist,
            [w3.nrfr.hist, w3.iopc.hist, w3.fpc.hist, w3.pop.hist, w3.ppolx.hist],
            ["NRFR", "IOPC", "FPC", "POP", "PPOLX"],
            [[0, 1], [0, 1e3], [0, 1e3], [0, 16e9], [0, 32]],
            img_background="background/overview.png",
            grid=1,
            title="World3 standard run")

#standard_run_capital_sector
stand_aff(w3.t.hist,
            [w3.fcaor.hist, w3.io.hist, w3.tai.hist, w3.aiph.hist, w3.fioaa.hist],
            ["FCAOR", "IO", "TAI", "AIPH", "FIOAA"],
            [[0, 1], [0, 4e12], [0, 4e12], [0, 200], [0, 0.201]],
            img_background="background/capital.png",
            grid=1,
            title="World3 standard run Capital sector")

#standard_run_agriculture_sector
stand_aff(w3.t.hist,
            [w3.ly.hist, w3.al.hist, w3.fpc.hist, w3.lmf.hist, w3.pop.hist],
            ["LY", "AL", "FPC", "LMF", "POP"],
            [[0, 4e3], [0, 4e9], [0, 800], [0, 1.6], [0, 16e9]],
            img_background="background/agriculture.png",
            grid=1,
            title="World3 standard run Agricultural sector")