########################################################################################################################
# © Copyright French Civil Aviation Authority
# Author: Julien LEGAVRE (2022)
# Contributor: Alexandre GONDRAN

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

C = "CONSTANT"
CT = "TABLE OF CONSTANTS"


class ErrorNodeAlreadyExists(Exception):
    pass

########################################################################################################################
# Node is a general class from which all types of nodes will take arguments.
# It has a name, a value, an associated function, predecessors, successors and a rank.
########################################################################################################################


class Node:
    def __init__(self, name, val=None, hg=None):
        self.name = name
        self.val = val
        self.cons = None
        self.pred = []
        self.succ = []
        self.rank = None
        if hg is not None:
            hg.add_node(self)

    def __repr__(self):
        value = "None"
        if self.val:
            value = "{:.03f}".format(self.val)
        return "{0.name:<8} {3} IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)

    def set_cons(self, f, pred):
        self.cons = f
        self.pred = pred
        for p in pred:
            p.succ.append(self)

    def get_pred_name(self):
        return [p.name for p in self.pred]

    def get_succ_name(self):
        return [p.name for p in self.succ]

########################################################################################################################
# NodeStock is a node which is computed by calculating its derivate.
# It has a historic in order to be able to show its evolution.
########################################################################################################################

class NodeStock(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = [val]

    def eval(self, ts, save=True):
        # text = "{}:{}->".format(self.name, self.val)
        if self.val:
            self.val = self.val + self.cons(*[p.val for p in self.pred]) * ts
        else:
            self.val = self.cons(*[p.val for p in self.pred]) * ts
        if save:
            self.hist.append(self.val)
        # text += "{}".format(self.val)
        # print(text)

########################################################################################################################
# NodeFlow is a node which is computed each time.
# It also has a historic in order to be able to show its evolution.
########################################################################################################################


class NodeFlow(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = []

    def eval(self, dt, save=True):
        # text = "{}:{}->".format(self.name, self.val)
        self.val = self.cons(*[p.val for p in self.pred])
        if save:
            self.hist.append(self.val)
        # text += "{}".format(self.val)
        # print(text)

########################################################################################################################
# NodeDelay3 is a node which is computed each time by using its 2 previous values.
# I1, I2 and I3 are "memory" variables which are used in the evaluation of the node value.
# It also has a historic in order to be able to show its evolution.
# Its evaluation requires a constant and another node.
# f_delayinit is a function in order to associate a constant and a node to the NodeDelay3.
########################################################################################################################


class NodeDelay3(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = []
        self.cst = None
        self.node = None
        self.I1 = None
        self.I2 = None
        self.I3 = None

    def eval(self, ts, save=True):
        # text = "{}:{}->".format(self.name, self.val)
        self.cons(*[p.val for p in self.pred])
        dl = self.cst / 3
        RT1 = self.I1 / dl
        self.I1 = self.I1 + (self.node - RT1) * ts
        RT2 = self.I2 / dl
        self.I2 = self.I2 + (RT1 - RT2) * ts
        self.I3 = self.I3 + (RT2 - self.I3 / dl) * ts
        self.val = self.I3 / dl
        if save:
            self.hist.append(self.val)
        # text += "{}".format(self.val)
        # print(text)

    def f_delayinit(self, flow, constant):
        self.node = flow
        self.cst = constant
        if not self.hist:
            self.val = flow
            self.I1 = self.I2 = self.I3 = flow * constant / 3

########################################################################################################################
# NodeConstant is a node which has a fix value.
# It can be a constant (C) or a table of constants (CT).
########################################################################################################################


class NodeConstant(Node):
    def __init__(self, name, t, val=None, hg=None):
        super().__init__(name, val, hg)
        self.type = t

    def __repr__(self):
        value = "None"
        if self.val is not None:
            if self.type == CT:
                l1 = ",".join([str(x) for x in self.val[0]])
                l2 = ",".join([str(x) for x in self.val[1]])
                value = "[{}]:[{}]".format(l1, l2)
            else:
                value = "{0.val:.03f} ".format(self)
        return "{0.name:<8} {3} IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)

########################################################################################################################
# World3 is the class where all nodes will be. It will be created link between them in World3.
# It requires a version (1972 or 2003) in order to choose initial values and constants.
# Different methods are developed in this class: "MyWorld3: Equations and Explanations" details them.

# Types of World3 attributes:
# version: int
# nodes: dict with str as key and node as value
# nbrank: int
# nodesrank: list of nodes
# stocks: list of nodes
########################################################################################################################


class World3:
    def __init__(self, version: int, nodes=[]):
        self.version = version
        self.nodes = {n.name: n for n in nodes}
        self.nbrank = None
        self.nodesrank = None
        self.stocks = [n for n in nodes if type(n) == NodeStock]

    def __repr__(self):
        return "\n".join([str(v) for c,v in self.nodes.items()])

    def add_node(self, node):
        if node.name in self.nodes:
            print("Node {} already exists. Modify the modelling :".format(node.name))
            print(self.nodes[node.name])
            raise ErrorNodeAlreadyExists()
        self.nodes[node.name] = node
        if type(node) == NodeStock:
            self.stocks.append(node)

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_equation(self, f, x_target, x_s):
        x_target.set_cons(f, x_s)

    def eval(self, ts):
        for ns in self.nodesrank:
            ns.eval(ts)

    def run(self, it, ft, ts):
        self.set_rank()
        nb_step = int((ft - it) / ts)
        for i in range(nb_step):
            self.eval(ts)
        for stock in self.stocks:
            stock.hist.pop()

    ##############################################################################
    # sub_graph_vertex: allow to obtain sub-graphs                               #
    # from known values (Constants and initial values of Stocks)                 #
    # d2: list of node name if node respect the condition                        #
    # d1: dict with node name as key and its place in d2 as value                #
    # gM: list of lists of predecessors for each node, with the d2 order of node #
    # gP: list of lists of successors for each node, with the d2 order of node   #
    ##############################################################################

    def sub_graph_vertex(self, cond):
        d2 = [name for name, n in self.nodes.items() if cond(n)]
        d1 = {name: i for i, name in enumerate(d2)}
        size = len(d2)
        gM = [[] for _ in range(size)]
        gP = [[] for _ in range(size)]
        for name in d2:
            n = self.nodes[name]
            for u in n.pred:
                if cond(u):
                    gM[d1[name]].append(d1[u.name])
                    gP[d1[u.name]].append(d1[name])
        return d2, gM, gP

    #################################################################################
    # set_rank: allow to have the order to follow to solve the graph                #
    # dM: list of the number of predecessors for each node                          #
    # S0: list of order to evaluate nodes which have no predecessors                #
    # rank_rec: build the list of order r by recurrence using the first solution S0 #
    # nodesrank: list of nodes ordered by priority in the calcul                    #
    #################################################################################

    def set_rank(self):
        d2, gM, gP = self.sub_graph_vertex(lambda x: type(x) == NodeDelay3 or type(x) == NodeFlow)
        size = len(d2)
        dM = [len(gi) for gi in gM]
        S0 = [i for i, di in enumerate(dM) if di == 0]
        r = [None] * size

        def rank_rec(Sk, k):
            Sk1 = []
            for i in Sk:
                r[i] = k
                for j in gP[i]:
                    dM[j] -= 1
                    if dM[j] == 0:
                        Sk1.append(j)
            if len(Sk1) > 0:
                return rank_rec(Sk1, k+1)

        rank_rec(S0, 0)
        self.nbrank = max(r) + 1
        self.nodesrank = [self.nodes[d2[j]] for _, j in sorted([(ri, i) for i, ri in enumerate(r)])]
        self.nodesrank += self.stocks
