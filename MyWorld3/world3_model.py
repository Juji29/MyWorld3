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

import copy
from system_dynamic import C, CT
from math import log

NEVER = 4000 # the year 4000

class Scenario(object):
    def __init__(self):
        self.more_nonrenewable_resources = False
        self.more_nonrenewable_resources_year = NEVER
        self.pollution_control = False # à policy_year
        #self.pollution_control_year = NEVER
        self.policy_year = NEVER
        self.land_yield_tech = False # à policy_year
        self.land_protection_year = NEVER
        self.resource_tech = False # à policy_year
        self.fertility_control_year = NEVER
        self.zero_pop_growth_year = NEVER
        self.stable_industrial_output = False
        self.industrial_equilibrium_year = NEVER

    def copy(self):
        return copy.copy(self)

scenario1 = Scenario()

scenario2 = Scenario()
scenario2.more_nonrenewable_resources = True
scenario2.more_nonrenewable_resources_year = 2002

scenario3 = scenario2.copy()
scenario3.pollution_control = True
scenario3.policy_year = 2002

scenario4 = scenario3.copy()
scenario4.land_yield_tech = True

scenario5 = scenario4.copy()
scenario5.land_protection_year = 2002

scenario6 = scenario5.copy()
scenario6.resource_tech = True

scenario7 = scenario2.copy()
scenario7.zero_pop_growth_year = 2002
scenario7.fertility_control_year = 2002

scenario8 = scenario7.copy()
scenario8.stable_industrial_output = True
scenario8.industrial_equilibrium_year = 2002
scenario8.policy_year = 2002

scenario9 = scenario8.copy()
scenario9.pollution_control = True
scenario9.land_yield_tech = True
scenario9.land_protection_year = 2002
scenario9.resource_tech = True

scenario10 = scenario9.copy()
year_change = 1982
scenario10.policy_year = year_change
scenario10.zero_pop_growth_year = year_change
scenario10.fertility_control_year = year_change
scenario10.industrial_equilibrium_year = year_change
scenario10.land_protection_year = year_change
scenario10.more_nonrenewable_resources_year = year_change

scenario11 = scenario9.copy()
year_change = 2032
scenario11.policy_year = year_change
scenario11.zero_pop_growth_year = year_change
scenario11.fertility_control_year = year_change
scenario11.industrial_equilibrium_year = year_change
scenario11.land_protection_year = year_change
scenario11.more_nonrenewable_resources_year = year_change

scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5, scenario6, scenario7, scenario8, scenario9, scenario10, scenario11]

SYSTEM = 'system'
AGRICULTURE = 'agriculture'
POPULATION = 'population'
CAPITAL = "capital"
NR_RESSOURCES = "no-renewable ressources"

######################
# Initial conditions #
######################
def load(world3):
    world3.scene = scenarios[world3.scenario - 1]
    TS = world3.addConstant("TS", C, val=world3.time_step, detail="time step", cat=SYSTEM)
    t = world3.addStock("time", val=world3.init_time, detail="time", unit="year", cat=SYSTEM)
    world3.add_equation(lambda x: 1, t, [TS])

    #########
    # Units #
    #########
    OY   = world3.addConstant("OY", C, val=1, detail="One year",
                              unit="year", cat=SYSTEM)
    UAGI = world3.addConstant("UAGI", C, val=1,
                              detail="Unit of Agricultural Inputs per Hectare",
                              cat=AGRICULTURE)
    UP   = world3.addConstant("UP", C, val=1, detail="Unit of Person",
                              cat=POPULATION)
    GDPU = world3.addConstant("GDPU", C, val=1,
                              detail="Gross Domestic Product Unit",
                              cat=CAPITAL)


    ######################################
    # Variables close to population #
    ######################################
    P1I = world3.addConstant("P1I", C, val=6.50e8,
                       detail="Initial population aged from 0 to 14 years at the year 1900",
                       unit="person", cat=POPULATION)
    P2I = world3.addConstant("P2I", C, val=7.00e8,
                       detail="Initial population aged from 15 to 44 years at the year 1900",
                       unit="person", cat=POPULATION)
    P3I = world3.addConstant("P3I", C, val=1.90e8,
                       detail="Initial population aged from 45 to 64 years at the year 1900",
                       unit="person", cat=POPULATION)
    P4I = world3.addConstant("P4I", C, val=6.00e7,
                       detail="Initial population older than adge 65 at the year 1900",
                       unit="person", cat=POPULATION)

    M1 = world3.addConstant("M1", CT, val=([20, 0.0567],
                                     [30, 0.0366],
                                     [40, 0.0243],
                                     [50, 0.0155],
                                     [60, 0.0082],
                                     [70, 0.0023],
                                     [80, 0.001]),
                      detail="Mortality rate in population aged from 0 to 14 years",
                      unit=None, cat=POPULATION)
    M2 = world3.addConstant("M2", CT, val=([20, 0.0266],
                                     [30, 0.0171],
                                     [40, 0.011],
                                     [50, 0.0065],
                                     [60, 0.004],
                                     [70, 0.0016],
                                     [80, 0.0008]),
                      detail="Mortality rate in population aged from 15 to 44 years",
                      unit=None, cat=POPULATION)
    M3 = world3.addConstant("M3", CT, val=([20, 0.0562],
                                     [30, 0.0373],
                                     [40, 0.0252],
                                     [50, 0.0171],
                                     [60, 0.0118],
                                     [70, 0.0083],
                                     [80, 0.006]),
                      detail="Mortality rate in population aged from 45 to 64 years",
                      unit=None, cat=POPULATION)
    M4 = world3.addConstant("M4", CT, val=([20, 0.13],
                                     [30, 0.11],
                                     [40, 0.09],
                                     [50, 0.07],
                                     [60, 0.06],
                                     [70, 0.05],
                                     [80, 0.04]),
                      detail="Mortality rate in population older than age 65",
                      unit=None, cat=POPULATION)

    pop = world3.addFlow("pop", detail="Total Population",
                   unit="capita", cat=POPULATION)

    p1 = world3.addStock("p1", val=P1I.val)
    p2 = world3.addStock("p2", val=P2I.val)
    p3 = world3.addStock("p3", val=P3I.val)
    p4 = world3.addStock("p4", val=P4I.val)

    m1 = world3.addFlow("m1")
    m2 = world3.addFlow("m2")
    m3 = world3.addFlow("m3")
    m4 = world3.addFlow("m4")

    d1 = world3.addFlow("d1")
    d2 = world3.addFlow("d2")
    d3 = world3.addFlow("d3")
    d4 = world3.addFlow("d4")

    mat1 = world3.addFlow("mat1")
    mat2 = world3.addFlow("mat2")
    mat3 = world3.addFlow("mat3")

    # Related to death
    LEN = world3.addConstant("LEN", C, val=28)
    HSID = world3.addConstant("HSID", C, val=20)
    EHSPCI = world3.addConstant("EHSPCI", C, val=0)

    # LMF values depend on the version used
    if world3.version == 1972:
        LMF = world3.addConstant("LMF", CT, val=([0, 0],
                                           [1, 1],
                                           [2, 1.2],
                                           [3, 1.3],
                                           [4, 1.35],
                                           [5, 1.4]))
    if world3.version == 2003:
        LMF = world3.addConstant("LMF", CT, val=([0, 0],
                                           [1, 1],
                                           [2, 1.43],
                                           [3, 1.5],
                                           [4, 1.5],
                                           [5, 1.5]))

    HSAPC = world3.addConstant("HSAPC", CT, val=([0, 0],
                                           [250, 20],
                                           [500, 50],
                                           [750, 95],
                                           [1000, 140],
                                           [1250, 175],
                                           [1500, 200],
                                           [1750, 220],
                                           [2000, 230]))
    LMHS1 = world3.addConstant("LMHS1", CT, val=([0, 1],
                                           [20, 1.1],
                                           [40, 1.4],
                                           [60, 1.6],
                                           [80, 1.7],
                                           [100, 1.8]))

    # LMHS2 values depend on the version used
    if world3.version == 1972:
        LMHS2 = world3.addConstant("LMHS2", CT, val=([0, 1],
                                               [20, 1.4],
                                               [40, 1.6],
                                               [60, 1.8],
                                               [80, 1.95],
                                               [100, 2]))
    if world3.version == 2003:
        LMHS2 = world3.addConstant("LMHS2", CT, val=([0, 1],
                                               [20, 1.5],
                                               [40, 1.9],
                                               [60, 2],
                                               [80, 2],
                                               [100, 2]))

    FPU = world3.addConstant("FPU", CT, val=([0, 0],
                                       [2e9, 0.2],
                                       [4e9, 0.4],
                                       [6e9, 0.5],
                                       [8e9, 0.58],
                                       [1e10, 0.65],
                                       [1.2e10, 0.72],
                                       [1.4e10, 0.78],
                                       [1.6e10, 0.8]))
    CMI = world3.addConstant("CMI", CT, val=([0, 0.5],
                                       [200, 0.05],
                                       [400, -0.1],
                                       [600, -0.08],
                                       [800, -0.02],
                                       [1000, 0.05],
                                       [1200, 0.1],
                                       [1400, 0.15],
                                       [1600, 0.2]))
    LMP = world3.addConstant("LMP", CT, val=([0, 1],
                                       [10, 0.99],
                                       [20, 0.97],
                                       [30, 0.95],
                                       [40, 0.9],
                                       [50, 0.85],
                                       [60, 0.75],
                                       [70, 0.65],
                                       [80, 0.55],
                                       [90, 0.4],
                                       [100, 0.2]))

    lmf = world3.addFlow("lmf")
    hsapc = world3.addFlow("hsapc")
    lmhs1 = world3.addFlow("lmhs1")
    lmhs2 = world3.addFlow("lmhs2")
    fpu = world3.addFlow("fpu")
    cmi = world3.addFlow("cmi")
    lmp = world3.addFlow("lmp")

    d = world3.addFlow("d")
    cdr = world3.addFlow("cdr")
    lmhs = world3.addFlow("lmhs")
    ehspc = world3.addStock("ehspc", val=EHSPCI.val)
    lmc = world3.addFlow("lmc")
    le = world3.addFlow("le")

    # Related to birth
    RLT = world3.addConstant("RLT", C, val=30)
    PET = world3.addConstant("PET", C, val=4000)
    MTFN = world3.addConstant("MTFN", C, val=12)
    LPD = world3.addConstant("LPD", C, val=20)
    AIOPCI = world3.addConstant("AIOPCI", C, val=43.3)

    # ZPGT values depend on scenario chosen
    # mise en place de la politique de conrôle de naissance à 2 enfants par femme
    ZPGT = world3.addConstant("ZPGT", C, val=world3.scene.zero_pop_growth_year)

    # DCFSN values depend on the version used
    if world3.version == 1972:
        DCFSN = world3.addConstant("DCFSN", C, val=4)
    if world3.version == 2003:
        DCFSN = world3.addConstant("DCFSN", C, val=3.8)

    SAD = world3.addConstant("SAD", C, val=20)
    IEAT = world3.addConstant("IEAT", C, val=3)

    # FCEST values depend on scenario used
    # on fixe la fertillité à 1 en 2002 dans la cadre du contrôle des naissances
    FCEST = world3.addConstant("FCEST", C, val=world3.scene.fertility_control_year)

    # FM values depend on the version used
    if world3.version == 1972:
        FM = world3.addConstant("FM", CT, val=([0, 0],
                                         [10, 0.2],
                                         [20, 0.4],
                                         [30, 0.6],
                                         [40, 0.8],
                                         [50, 0.9],
                                         [60, 1],
                                         [70, 1.05],
                                         [80, 1.1]))
    if world3.version == 2003:
        FM = world3.addConstant("FM", CT, val=([0, 0],
                                         [10, 0.2],
                                         [20, 0.4],
                                         [30, 0.6],
                                         [40, 0.7],
                                         [50, 0.75],
                                         [60, 0.79],
                                         [70, 0.84],
                                         [80, 0.87]))

    CMPLE = world3.addConstant("CMPLE", CT, val=([0, 3],
                                           [10, 2.1],
                                           [20, 1.6],
                                           [30, 1.4],
                                           [40, 1.3],
                                           [50, 1.2],
                                           [60, 1.1],
                                           [70, 1.05],
                                           [80, 1]))

    # SFSN values depend on the version used
    if world3.version == 1972:
        SFSN = world3.addConstant("SFSN", CT, val=([0, 1.25],
                                             [200, 1],
                                             [400, 0.9],
                                             [600, 0.8],
                                             [800, 0.75]))
    if world3.version == 2003:
        SFSN = world3.addConstant("SFSN", CT, val=([0, 1.25],
                                             [200, 0.94],
                                             [400, 0.715],
                                             [600, 0.59],
                                             [800, 0.5]))

    FRSN = world3.addConstant("FRSN", CT, val=([-0.2, 0.5],
                                         [-0.1, 0.6],
                                         [0, 0.7],
                                         [0.1, 0.85],
                                         [0.2, 1]))
    FCE = world3.addConstant("FCE", CT, val=([0, 0.75],
                                       [0.5, 0.85],
                                       [1, 0.9],
                                       [1.5, 0.95],
                                       [2, 0.98],
                                       [2.5, 0.99],
                                       [3, 1]))
    FSAFC = world3.addConstant("FSAFC", CT, val=([0, 0],
                                           [2, 0.005],
                                           [4, 0.015],
                                           [6, 0.025],
                                           [8, 0.03],
                                           [10, 0.035]))
    fm = world3.addFlow("fm")
    fce = world3.addFlow("fce")
    frsn = world3.addFlow("frsn")
    sfsn = world3.addFlow("sfsn")
    cmple = world3.addFlow("cmple")
    fsafc = world3.addFlow("fsafc")

    b = world3.addFlow("b")
    cbr = world3.addFlow("cbr")
    tf = world3.addFlow("tf")
    mtf = world3.addFlow("mtf")
    dtf = world3.addFlow("dtf")
    ple = world3.addDelay3("ple")
    dcfs = world3.addFlow("dcfs")
    diopc = world3.addDelay3("diopc")
    fie = world3.addFlow("fie")
    aiopc = world3.addStock("aiopc", val=AIOPCI.val)
    nfc = world3.addFlow("nfc")
    fcfpc = world3.addDelay3("fcfpc")
    fcapc = world3.addFlow("fcapc")


    ################################
    # Variables close to capital #
    ################################
    # Related to industry
    ICOR1 = world3.addConstant("ICOR1", C, val=3)

    # ICOR2 values depend on the version used (is a NodeFlow if version is 2003)
    if world3.version == 1972:
        ICOR2 = world3.addConstant("ICOR2", C, val=3)

    ICI = world3.addConstant("ICI", C, val=2.1e11)
    ALIC1 = world3.addConstant("ALIC1", C, val=14)
    #"Average Lifetime of Industrial Capital"
    # ALIC2 values depend on scenario chosen
    ALIC20 = 18 if world3.scene.stable_industrial_output else 14
    ALIC2 = world3.addConstant("ALIC2", C, val=ALIC20)
    # bacule ALIC1 -> ALIC2 à PYEAR

    # IET values depend on scenario chosen "Industrial Equilibrium Time"
    IET = world3.addConstant("IET", C, val=world3.scene.industrial_equilibrium_year)

    FIOAC1 = world3.addConstant("FIOAC1", C, val=0.43)
    FIOAC2 = world3.addConstant("FIOAC2", C, val=0.43)

    # IOPCD values depend on scenario chosen
    # "Industrial Output Per Capita Desired"
    IOPCD0 = 350 if world3.scene.stable_industrial_output else 400
    IOPCD = world3.addConstant("IOPCD", C, val=IOPCD0)
    
    # PYEAR values depend on the version used and on scenario chosen
    if world3.version == 1972:
        PYEAR = world3.addConstant("PYEAR", C, val=1975)
    if world3.version == 2003:
        PYEAR = world3.addConstant("PYEAR", C, val=world3.scene.policy_year)

    FIOACV = world3.addConstant("FIOACV", CT, val=([0, 0.3],
                                             [0.2, 0.32],
                                             [0.4, 0.34],
                                             [0.6, 0.36],
                                             [0.8, 0.38],
                                             [1, 0.43],
                                             [1.2, 0.73],
                                             [1.4, 0.77],
                                             [1.6, 0.81],
                                             [1.8, 0.82],
                                             [2, 0.83]))
    fioacv = world3.addFlow("fioacv")

    iopc = world3.addFlow("iopc")
    io = world3.addFlow("io")
    icor = world3.addFlow("icor")

    # ICOR2 values depend on the version used (is a NodeConstant if version is 1972)
    if world3.version == 2003:
        icor2 = world3.addFlow("icor2")

    ic = world3.addStock("ic", val=ICI.val)
    icdr = world3.addFlow("icdr")
    alic = world3.addFlow("alic")
    icir = world3.addFlow("icir")
    fioai = world3.addFlow("fioai")
    fioac = world3.addFlow("fioac")
    fioacc = world3.addFlow("fioacc")

    # Related to services
    SCI = world3.addConstant("SCI", C, val=1.44e11)
    ALSC1 = world3.addConstant("ALSC1", C, val=20)

    # ALSC2 values depend on scenario chosen
    # "Average Lifetime of Service Capital"
    # ALSC1 -> ALSC2 at PYEAR
    ALSC20 = 25 if world3.scene.stable_industrial_output else 20
    ALSC2 = world3.addConstant("ALSC2", C, val=ALSC20)

    SCOR1 = world3.addConstant("SCOR1", C, val=1)
    SCOR2 = world3.addConstant("SCOR2", C, val=1)

    ISOPC1 = world3.addConstant("ISOPC1", CT, val=([0, 40],
                                             [200, 300],
                                             [400, 640],
                                             [600, 1000],
                                             [800, 1220],
                                             [1000, 1450],
                                             [1200, 1650],
                                             [1400, 1800],
                                             [1600, 2000]))
    ISOPC2 = world3.addConstant("ISOPC2", CT, val=([0, 40],
                                             [200, 300],
                                             [400, 640],
                                             [600, 1000],
                                             [800, 1220],
                                             [1000, 1450],
                                             [1200, 1650],
                                             [1400, 1800],
                                             [1600, 2000]))
    FIOAS1 = world3.addConstant("FIOAS1", CT, val=([0, 0.3],
                                             [0.5, 0.2],
                                             [1, 0.1],
                                             [1.5, 0.05],
                                             [2, 0]))
    FIOAS2 = world3.addConstant("FIOAS2", CT, val=([0, 0.3],
                                             [0.5, 0.2],
                                             [1, 0.1],
                                             [1.5, 0.05],
                                             [2, 0]))
    isopc1 = world3.addFlow("isopc1")
    isopc2 = world3.addFlow("isopc2")
    fioas1 = world3.addFlow("fioas1")
    fioas2 = world3.addFlow("fioas2")

    isopc = world3.addFlow("isopc")
    fioas = world3.addFlow("fioas")
    scir = world3.addFlow("scir")
    sc = world3.addStock("sc", val=SCI.val)
    scdr = world3.addFlow("scdr")
    alsc = world3.addFlow("alsc")
    so = world3.addFlow("so")
    sopc = world3.addFlow("sopc")
    scor = world3.addFlow("scor")

    # Related to jobs
    LFPF = world3.addConstant("LFPF", C, val=0.75)
    LUFDT = world3.addConstant("LUFDT", C, val=2)
    LUFDI = world3.addConstant("LUFDI", C, val=1)

    JPICU = world3.addConstant("JPICU", CT, val=([50, 3.7e-4],
                                           [200, 1.8e-4],
                                           [350, 1.2e-4],
                                           [500, 9e-5],
                                           [650, 7e-5],
                                           [800, 6e-5]))
    JPSCU = world3.addConstant("JPSCU", CT, val=([50, 1.1e-3],
                                           [200, 6e-4],
                                           [350, 3.5e-4],
                                           [500, 2e-4],
                                           [650, 1.5e-4],
                                           [800, 1.5e-4]))
    JPH = world3.addConstant("JPH", CT, val=([2, 2],
                                       [6, 0.5],
                                       [10, 0.4],
                                       [14, 0.3],
                                       [18, 0.27],
                                       [22, 0.24],
                                       [26, 0.2],
                                       [30, 0.2]))
    CUF = world3.addConstant("CUF", CT, val=([1, 1],
                                       [3, 0.9],
                                       [5, 0.7],
                                       [7, 0.3],
                                       [9, 0.1],
                                       [11, 0.1]))
    jpicu = world3.addFlow("jpicu")
    jpscu = world3.addFlow("jpscu")
    jph = world3.addFlow("jph")
    cuf = world3.addFlow("cuf")

    j = world3.addFlow("j")
    pjis = world3.addFlow("pjis")
    pjss = world3.addFlow("pjss")
    pjas = world3.addFlow("pjas")
    lf = world3.addFlow("lf")
    luf = world3.addFlow("luf")
    lufd = world3.addStock("lufd", val=LUFDI.val)


    ##################################
    # Variables close to agriculture #
    ##################################
    # Loop 1
    PALT = world3.addConstant("PALT", C, val=3.2e9)
    ALI = world3.addConstant("ALI", C, val=0.9e9)
    PALI = world3.addConstant("PALI", C, val=2.3e9)
    LFH = world3.addConstant("LFH", C, val=0.7)
    PL = world3.addConstant("PL", C, val=0.1)

    IFPC1 = world3.addConstant("IFPC1", CT, val=([0, 230],
                                           [200, 480],
                                           [400, 690],
                                           [600, 850],
                                           [800, 970],
                                           [1000, 1070],
                                           [1200, 1150],
                                           [1400, 1210],
                                           [1600, 1250]))
    IFPC2 = world3.addConstant("IFPC2", CT, val=([0, 230],
                                           [200, 480],
                                           [400, 690],
                                           [600, 850],
                                           [800, 970],
                                           [1000, 1070],
                                           [1200, 1150],
                                           [1400, 1210],
                                           [1600, 1250]))
    FIOAA1 = world3.addConstant("FIOAA1", CT, val=([0, 0.4],
                                             [0.5, 0.2],
                                             [1, 0.1],
                                             [1.5, 0.025],
                                             [2, 0],
                                             [2.5, 0]))
    FIOAA2 = world3.addConstant("FIOAA2", CT, val=([0, 0.4],
                                             [0.5, 0.2],
                                             [1, 0.1],
                                             [1.5, 0.025],
                                             [2, 0],
                                             [2.5, 0]))
    DCPH = world3.addConstant("DCPH", CT, val=([0, 100000],
                                         [0.1, 7400],
                                         [0.2, 5200],
                                         [0.3, 3500],
                                         [0.4, 2400],
                                         [0.5, 1500],
                                         [0.6, 750],
                                         [0.7, 300],
                                         [0.8, 150],
                                         [0.9, 75],
                                         [1, 50]))
    ifpc1 = world3.addFlow("ifpc1")
    ifpc2 = world3.addFlow("ifpc2")
    fioaa1 = world3.addFlow("fioaa1")
    fioaa2 = world3.addFlow("fioaa2")
    dcph = world3.addFlow("dcph")

    lfc = world3.addFlow("lfc")
    al = world3.addStock("al", val=ALI.val)
    pal = world3.addStock("pal", val=PALI.val)
    f = world3.addFlow("f")
    fpc = world3.addFlow("fpc")
    ifpc = world3.addFlow("ifpc")
    tai = world3.addFlow("tai")
    fioaa = world3.addFlow("fioaa")
    ldr = world3.addFlow("ldr")

    # Loop 2
    ALAI1 = world3.addConstant("ALAI1", C, val=2)

    # ALAI2 values depend on scenario chosen
    # "Average Lifetime of Agricultural Inputs"
    # ALAI1 -> ALAI2 at PYEAR
    ALAI20 = 2.5 if world3.scene.stable_industrial_output else 2
    ALAI2 = world3.addConstant("ALAI2", C, val=ALAI20)

    AII = world3.addConstant("AII", C, val=5e9)
    LYF1 = world3.addConstant("LYF1", C, val=1)

    # LYF2 values depend on the version used (is a NodeDelay3 if version is 2003)
    if world3.version == 1972:
        LYF2 = world3.addConstant("LYF2", C, val=1)

    IO70 = world3.addConstant("IO70", C, val=7.9e11)
    SD = world3.addConstant("SD", C, val=0.07)

    # TDD values depend on the version used (not used in 1972)
    if world3.version == 2003:
        TDD = world3.addConstant("TDD", C, val=20)

    # LYMC values depend on the version used
    if world3.version == 1972:
        LYMC = world3.addConstant("LYMC", CT, val=([0, 1],
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
                                             [1000, 10]))
    if world3.version == 2003:
        LYMC = world3.addConstant("LYMC", CT, val=([0, 1],
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
                                             [1000, 10]))

    LYMAP1 = world3.addConstant("LYMAP1", CT, val=([0, 1],
                                             [10, 1],
                                             [20, 0.7],
                                             [30, 0.4]))

    # LYMAP2 values depend on the version used
    if world3.version == 1972:
        LYMAP2 = world3.addConstant("LYMAP2", CT, val=([0, 1],
                                                 [10, 1],
                                                 [20, 0.7],
                                                 [30, 0.4]))
    if world3.version == 2003:
        LYMAP2 = world3.addConstant("LYMAP2", CT, val=([0, 1],
                                                 [10, 1],
                                                 [20, 0.98],
                                                 [30, 0.95]))

    FIALD = world3.addConstant("FIALD", CT, val=([0, 0],
                                           [0.25, 0.05],
                                           [0.5, 0.15],
                                           [0.75, 0.3],
                                           [1, 0.5],
                                           [1.25, 0.7],
                                           [1.5, 0.85],
                                           [1.75, 0.95],
                                           [2, 1]))
    MLYMC = world3.addConstant("MLYMC", CT, val=([0, 0.075],
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
                                           [600, 0.005]))
    lymc = world3.addFlow("lymc")
    lymap = world3.addFlow("lymap")
    lymap1 = world3.addFlow("lymap1")
    lymap2 = world3.addFlow("lymap2")
    fiald = world3.addFlow("fiald")
    mlymc = world3.addFlow("mlymc")

    cai = world3.addFlow("cai")
    ai = world3.addStock("ai", val=AII.val)
    alai = world3.addFlow("alai")
    aiph = world3.addFlow("aiph")
    ly = world3.addFlow("ly")
    lyf = world3.addFlow("lyf")

    # lyf2 values depend on the version used (is a NodeConstant if version is 1972)
    if world3.version == 2003:
        lyf2 = world3.addDelay3("lyf2")

    mpld = world3.addFlow("mpld")
    mpai = world3.addFlow("mpai")

    # Loop 3
    # ALLN values depend on the version used
    if world3.version == 1972:
        ALLN = world3.addConstant("ALLN", C, val=6000)
    if world3.version == 2003:
        ALLN = world3.addConstant("ALLN", C, val=1000)

    UILDT = world3.addConstant("UILDT", C, val=10)
    UILI = world3.addConstant("UILI", C, val=8.2e6)

    # LLMYTM values depend on scenario chosen
    LLMYTM = world3.addConstant("LLMYTM", C, val=world3.scene.land_protection_year)
    
    LLMY1 = world3.addConstant("LLMY1", CT, val=([0, 1.2],
                                           [1, 1],
                                           [2, 0.63],
                                           [3, 0.36],
                                           [4, 0.16],
                                           [5, 0.055],
                                           [6, 0.04],
                                           [7, 0.025],
                                           [8, 0.015],
                                           [9, 0.01]))

    # LLMY2 values depend on the version used
    if world3.version == 1972:
        LLMY2 = world3.addConstant("LLMY2", CT, val=([0, 1.2],
                                               [1, 1],
                                               [2, 0.63],
                                               [3, 0.36],
                                               [4, 0.16],
                                               [5, 0.055],
                                               [6, 0.04],
                                               [7, 0.025],
                                               [8, 0.015],
                                               [9, 0.01]))
    if world3.version == 2003:
        LLMY2 = world3.addConstant("LLMY2", CT, val=([0, 1.2],
                                               [1, 1],
                                               [2, 0.63],
                                               [3, 0.36],
                                               [4, 0.29],
                                               [5, 0.26],
                                               [6, 0.24],
                                               [7, 0.22],
                                               [8, 0.21],
                                               [9, 0.2]))

    UILPC = world3.addConstant("UILPC", CT, val=([0, 0.005],
                                           [200, 0.008],
                                           [400, 0.015],
                                           [600, 0.025],
                                           [800, 0.04],
                                           [1000, 0.055],
                                           [1200, 0.07],
                                           [1400, 0.08],
                                           [1600, 0.09]))
    llmy = world3.addFlow("llmy")
    llmy1 = world3.addFlow("llmy1")
    llmy2 = world3.addFlow("llmy2")
    uilpc = world3.addFlow("uilpc")

    all = world3.addFlow("all")
    ler = world3.addFlow("ler")
    uilr = world3.addFlow("uilr")
    lrui = world3.addFlow("lrui")
    uil = world3.addStock("uil", val=UILI.val)

    # Loop 4
    LFERTI = world3.addConstant("LFERTI", C, val=600)

    LFDR = world3.addConstant("LFDR", CT, val=([0, 0],
                                         [10, 0.1],
                                         [20, 0.3],
                                         [30, 0.5]))
    lfdr = world3.addFlow("lfdr")

    lfert = world3.addStock("lfert", val=LFERTI.val)
    lfd = world3.addFlow("lfd")

    # Loop 5
    ILF = world3.addConstant("ILF", C, val=600)
    SFPC = world3.addConstant("SFPC", C, val=230)
    FSPD = world3.addConstant("FSPD", C, val=2)
    PFRI = world3.addConstant("PFRI", C, val=1)

    # DFR values depend on the version used (not used in 1972)
    if world3.version == 2003:
        DFR = world3.addConstant("DFR", C, val=2)

    LFRT = world3.addConstant("LFRT", CT, val=([0, 20],
                                         [0.02, 13],
                                         [0.04, 8],
                                         [0.06, 4],
                                         [0.08, 2],
                                         [0.1, 2]))
    FALM = world3.addConstant("FALM", CT, val=([0, 0],
                                         [1, 0.04],
                                         [2, 0.07],
                                         [3, 0.09],
                                         [4, 0.1]))

    # LYCM values depend on the version used and on scenario chosen (not used in 1972)
    # COYM values depend on the version used (not used in 1972)
    if world3.version == 2003:
        if world3.scene.land_yield_tech:
            LYCM = world3.addConstant("LYCM", CT, val=([0, 0],
                                                 [1, 0.04]))
        else:
            LYCM = world3.addConstant("LYCM", CT, val=([0, 0],
                                                 [1, 0]))
        COYM = world3.addConstant("COYM", CT, val=([1, 1],
                                             [1.2, 1.05],
                                             [1.4, 1.12],
                                             [1.6, 1.25],
                                             [1.8, 1.35],
                                             [2, 1.5]))

        lycm = world3.addFlow("lycm")
        coym = world3.addFlow("coym")

    lfrt = world3.addFlow("lfrt")
    falm = world3.addFlow("falm")

    lfr = world3.addFlow("lfr")
    fr = world3.addFlow("fr")
    pfr = world3.addStock("pfr", val=PFRI.val)

    # lytd and lytdr values depend on the version used (not used in 1972)
    if world3.version == 2003:
        lytd = world3.addStock("lytd", val=LYF1.val)
        lytdr = world3.addFlow("lytdr")

    ################################
    # Variables close to resources #
    ################################
    # NRI values depend on scenario chosen
    NRI0 = 2e12 if world3.scene.more_nonrenewable_resources else 1e12
    NRI = world3.addConstant("NRI", C, val=NRI0)
    
    NRUF1 = world3.addConstant("NRUFI", C, val=1)

    # NRUF2 values depend on the version used (is a NodeDelay3 if version is 2003)
    if world3.version == 1972:
        NRUF2 = world3.addConstant("NRUF2", C, val=1)

    # FCAORTM values depend on scenario chosen : fraction of capital allocated to obtaining resources
    FCAORTM0 = world3.scene.more_nonrenewable_resources_year if world3.scene.more_nonrenewable_resources else NEVER
    FCAORTM = world3.addConstant("FCAORTM", C, val=FCAORTM0)

    # DNRUR values depend on the version used (not used in 1972)
    if world3.version == 2003:
        DNRUR = world3.addConstant("DNRUR", C, val=4.8e9)

    # PCRUM values depend on the version used
    if world3.version == 1972:
        PCRUM = world3.addConstant("PCRUM", CT, val=([0, 0],
                                               [200, 0.85],
                                               [400, 2.6],
                                               [600, 4.4],
                                               [800, 5.4],
                                               [1000, 6.2],
                                               [1200, 6.8],
                                               [1400, 7],
                                               [1600, 7]))
    if world3.version == 2003:
        PCRUM = world3.addConstant("PCRUM", CT, val=([0, 0],
                                               [200, 0.85],
                                               [400, 2.6],
                                               [600, 3.4],
                                               [800, 3.8],
                                               [1000, 4.1],
                                               [1200, 4.4],
                                               [1400, 4.7],
                                               [1600, 5]))

    FCAOR1 = world3.addConstant("FCAOR1", CT, val=([0, 1],
                                             [0.1, 0.9],
                                             [0.2, 0.7],
                                             [0.3, 0.5],
                                             [0.4, 0.2],
                                             [0.5, 0.1],
                                             [0.6, 0.05],
                                             [0.7, 0.05],
                                             [0.8, 0.05],
                                             [0.9, 0.05],
                                             [1, 0.05]))

    # FCAOR2 values depend on the version used and on scenario chosen
    if world3.version == 1972:
        FCAOR2 = world3.addConstant("FCAOR2", CT, val=([0, 1],
                                                 [0.1, 0.9],
                                                 [0.2, 0.7],
                                                 [0.3, 0.5],
                                                 [0.4, 0.2],
                                                 [0.5, 0.1],
                                                 [0.6, 0.05],
                                                 [0.7, 0.05],
                                                 [0.8, 0.05],
                                                 [0.9, 0.05],
                                                 [1, 0.05]))
    if world3.version == 2003:
        if world3.scene.more_nonrenewable_resources:
            FCAOR2 = world3.addConstant("FCAOR2", CT, val=([0, 1],
                                                     [0.1, 0.1],
                                                     [0.2, 0.05],
                                                     [0.3, 0.05],
                                                     [0.4, 0.05],
                                                     [0.5, 0.05],
                                                     [0.6, 0.05],
                                                     [0.7, 0.05],
                                                     [0.8, 0.05],
                                                     [0.9, 0.05],
                                                     [1, 0.05]))
        else:
            FCAOR2 = world3.addConstant("FCAOR2", CT, val=([0, 1],
                                                     [0.1, 0.2],
                                                     [0.2, 0.1],
                                                     [0.3, 0.05],
                                                     [0.4, 0.05],
                                                     [0.5, 0.05],
                                                     [0.6, 0.05],
                                                     [0.7, 0.05],
                                                     [0.8, 0.05],
                                                     [0.9, 0.05],
                                                     [1, 0.05]))

    # NRCM values depend on the version used and on scenario chosen (not used in 1972)
    # ICOR2T values depend on the version used (not used in 1972)
    if world3.version == 2003:
        if world3.scene.resource_tech:
            NRCM = world3.addConstant("NRCM", CT, val=([-1, -0.04],
                                                 [0, 0]))
        else:
            NRCM = world3.addConstant("NRCM", CT, val=([-1, 0],
                                                 [0, 0]))
        ICOR2T = world3.addConstant("ICOR2T", CT, val=([0, 3.75],
                                                 [0.1, 3.6],
                                                 [0.2, 3.47],
                                                 [0.3, 3.36],
                                                 [0.4, 3.25],
                                                 [0.5, 3.16],
                                                 [0.6, 3.1],
                                                 [0.7, 3.06],
                                                 [0.8, 3.02],
                                                 [0.9, 3.01],
                                                 [1, 3]))

        nrcm = world3.addFlow("nrcm")
        icor2t = world3.addFlow("icor2t")

    pcrum = world3.addFlow("pcrum")
    fcaor = world3.addFlow("fcaor") #"fraction of capital allocated to obtaining resources"
    fcaor1 = world3.addFlow("fcaor1")
    fcaor2 = world3.addFlow("fcaor2")

    nr = world3.addStock("nr", val=NRI.val)
    nrur = world3.addFlow("nrur")
    nruf = world3.addFlow("nruf")

    # nruf2 values depend on the version used (is a NodeConstant if version is 1972)
    if world3.version == 2003:
        nruf2 = world3.addDelay3("nruf2")

    nrfr = world3.addFlow("nrfr")

    # nrtd and nrate values depend on the version used (not used in 1972)
    if world3.version == 2003:
        nrtd = world3.addStock("nrtd", val=NRUF1.val)
        nrate = world3.addFlow("nrate")


    ################################
    # Variables close to pollution #
    ################################
    PPGF1 = world3.addConstant("PPGF1", C, val=1)

    # PPGF2 values depend on the version used (is a NodeDelay3 if version is 2003)
    if world3.version == 1972:
        PPGF2 = world3.addConstant("PPGF2", C, val=1)

    FRPM = world3.addConstant("FRPM", C, val=0.02)
    IMEF = world3.addConstant("IMEF", C, val=0.1)
    IMTI = world3.addConstant("IMTI", C, val=10)
    FIPM = world3.addConstant("FIPM", C, val=0.001)
    AMTI = world3.addConstant("AMTI", C, val=1)
    PPTD = world3.addConstant("PPTD", C, val=20)
    PPOLI = world3.addConstant("PPOLI", C, val=2.5e7)
    PPOL70 = world3.addConstant("PPOLI70", C, val=1.36e8)
    AHL70 = world3.addConstant("AHL70", C, val=1.5)

    # DPOLX values depend on the version used (not used in 1972)
    if world3.version == 2003:
        DPOLX = world3.addConstant("DPOLX", C, val=1.2)

    AHLM = world3.addConstant("AHLM", CT, val=([1, 1],
                                         [251, 11],
                                         [501, 21],
                                         [751, 31],
                                         [1001, 41]))

    # POLGFM values depend on the version used and on scenario chosen (not used in 1972)
    # COPM values depend on the version used (not used in 1972)
    if world3.version == 2003:
        if world3.scene.pollution_control :
            POLGFM = world3.addConstant("POLGFM", CT, val=([-1, -0.04],
                                                     [0, 0]))
        else :
            POLGFM = world3.addConstant("POLGFM", CT, val=([-1, 0],
                                                     [0, 0]))
        COPM = world3.addConstant("COPM", CT, val=([0, 1.25],
                                             [0.1, 1.2],
                                             [0.2, 1.15],
                                             [0.3, 1.11],
                                             [0.4, 1.08],
                                             [0.5, 1.05],
                                             [0.6, 1.03],
                                             [0.7, 1.02],
                                             [0.8, 1.01],
                                             [0.9, 1],
                                             [1, 1]))

        polgfm = world3.addFlow("polgfm")
        copm = world3.addFlow("copm")

    ahlm = world3.addFlow("ahlm")
    ppgr = world3.addFlow("ppgr")
    ppgf = world3.addFlow("ppgf")

    # ppgf2 values depend on the version used (is a NodeConstant if version is 1972)
    if world3.version == 2003:
        ppgf2 = world3.addDelay3("ppgf2")

    ppgio = world3.addFlow("ppgio")
    ppgao = world3.addFlow("ppgao")
    ppapr = world3.addDelay3("ppapr")
    ppol = world3.addStock("ppol", val=PPOLI.val)
    ppolx = world3.addFlow("ppolx")
    ppasr = world3.addFlow("ppasr")
    ahl = world3.addFlow("ahl")

    # ptd and ptdr values depend on the version used (not used in 1972)
    if world3.version == 2003:
        ptd = world3.addStock("ptd", val=PPGF1.val)
        ptdr = world3.addFlow("ptdr")


    ###########
    # Indexes #
    ###########
    POF = world3.addConstant("POF", C, val=0.22)
    HUP = world3.addConstant("HUP", C, val=4)
    RHGDP = world3.addConstant("RHGDP", C, val=9508)
    RLGDP = world3.addConstant("RLGDP", C, val=24)
    TL = world3.addConstant("TL", C, val=1.91)
    GHAH = world3.addConstant("GHAH", C, val=1e9)

    LEI = world3.addConstant("LEI", CT, val=([25, 0],
                                       [35, 0.16],
                                       [45, 0.33],
                                       [55, 0.5],
                                       [65, 0.67],
                                       [75, 0.84],
                                       [85, 1]))
    EI = world3.addConstant("EI", CT, val=([0, 0],
                                     [1000, 0.81],
                                     [2000, 0.88],
                                     [3000, 0.92],
                                     [4000, 0.95],
                                     [5000, 0.98],
                                     [6000, 0.99],
                                     [7000, 1]))
    GDPPC = world3.addConstant("GDPPC", CT, val=([0, 120],
                                           [200, 600],
                                           [400, 1200],
                                           [600, 1800],
                                           [800, 2500],
                                           [1000, 3200]))
    foa = world3.addFlow("foa")
    foi = world3.addFlow("foi")
    fos = world3.addFlow("fos")

    resint = world3.addFlow("resint")
    plinid = world3.addFlow("plinid")
    cio = world3.addFlow("cio")
    ciopc = world3.addFlow("ciopc")

    lei = world3.addFlow("lei")
    ei = world3.addFlow("ei")
    gdppc = world3.addFlow("gdppc")

    hwi = world3.addFlow("hwi")
    gdpi = world3.addFlow("gdpi")
    hef = world3.addFlow("hef")
    algha = world3.addFlow("algha")
    alggha = world3.addFlow("alggha")
    ulgha = world3.addFlow("ulgha")



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
