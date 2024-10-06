########################################################################################################################
# © Copyright French Civil Aviation Authority
# Author: Julien LEGAVRE (2022)

# julien.legavre@alumni.enac.fr

# Updated by Lars Ekman, uablrek@gmail.com

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

import sys
import world3_model as w_sys
import system_dynamic as sd

VERSION = 2003
INITIAL_TIME = 1900
FINAL_TIME = 2100
TIME_STEP = 0.5
N_SCENARIO = 1

if __name__ == "__main__":
    world3 = sd.World3(VERSION, N_SCENARIO, INITIAL_TIME, FINAL_TIME, TIME_STEP)
    w_sys.load(world3)

    print('digraph world {')
    for _,n in world3.nodes.items():
        if n.cat == w_sys.SYSTEM:
            continue
        if type(n) == sd.NodeStock:
            l = n.name.upper()
            if n.detail != None:
                print(f'{n.name} [shape=box label={l} tooltip="{n.detail}"]')
            else:
                print(f'{n.name} [shape=box label={l}]')
        if type(n) == sd.NodeFlow:
            l = n.name.upper()
            if n.detail != None:
                print(f'{n.name} [shape=ellipse label={l} tooltip="{n.detail}"]')
            else:
                print(f'{n.name} [shape=ellipse label={l}]')
        if type(n) == sd.NodeDelay3:
            print(f'{n.name} [shape=Mcircle]')
    for _,n in world3.nodes.items():
        if n.cat == w_sys.SYSTEM:
            continue        
        if type(n) != sd.NodeConstant:
            for s in n.get_succ_name():
                print(f'{n.name} -> {s}')
    print('}')
