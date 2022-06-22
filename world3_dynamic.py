import numpy as np
from scipy.integrate import solve_ivp, odeint
import matplotlib.pyplot as plt

C = "CONSTANT"
CT = "CONSTANT_TABLE"


class ErrorNodeAlreadyExists(Exception): pass


class Node:
    def __init__(self, name, val=None, hg=None):
        self.name = name  # string
        self.val = val    # float
        self.cons = None  # fonction
        self.pred = []    # predecesseurs
        self.succ = []    # successeurs
        self.rank = None  # rang
        if hg is not None: # ajout du noeud à l'hypergraphe hg
            hg.add_node(self)

    def __repr__(self):
        value = "None"
        if self.val != None:
            value = "{:.03f}".format(self.val)
        return "{0.name:<8} {3} IN: {1:<20} OUT: {2} HIST: {4}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value, self.hist)

    def set_cons(self, f, pred):
        self.cons = f
        self.pred = pred
        for p in pred:
            p.succ.append(self)

    def get_pred_name(self):
        return [p.name for p in self.pred]

    def get_succ_name(self):
        return [p.name for p in self.succ]


class NodeStock(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = [val]

    def eval(self, ts, save=True):
        #text = "{}:{}->".format(self.name, self.val)
        if self.val:
            self.val = self.val + self.cons(*[p.val for p in self.pred]) * ts
        else:
            self.val = self.cons(*[p.val for p in self.pred]) * ts
        if save:
            self.hist.append(self.val)
        #text += "{}".format(self.val)
        #print(text)


class NodeFlow(Node):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)
        self.hist = []

    def eval(self, dt, save=True):
        #text = "{}:{}->".format(self.name, self.val)
        self.val = self.cons(*[p.val for p in self.pred])
        if save:
            self.hist.append(self.val)
        #text += "{}".format(self.val)
        #print(text)

class NodeSmooth(Node):
    def __init__(self, name, t, size, val=None, hg=None):
        super().__init__(name, val, hg)
        self.type = t
        self.hist = [None] * size
        self.cst = None
        self.node = None
        self.k = 0
        if t == "DELAY3":
            self.I1 = None
            self.histI1 = [None] * size
            self.I2 = None
            self.histI2 = [None] * size
            self.I3 = None
            self.histI3 = [None] * size

    def eval(self, ts, save=True):
        #text = "{}:{}->".format(self.name, self.val)
        self.cons(*[p.val for p in self.pred])
        if self.type == "SMOOTH":
            self.val += (self.node - self.val) * ts / self.cst
        if self.type == "DELAY3":
            dl = self.cst / 3
            RT1 = self.I1 / dl
            self.I1 = self.I1 + (self.node - RT1) * ts
            RT2 = self.I2 / dl
            self.I2 = self.I2 + (RT1 - RT2) * ts
            self.I3 = self.I3 + (RT2 - self.I3 / dl) * ts
            self.val = self.I3 / dl
        if save:
            k = self.k
            self.hist[k] = self.val
            if self.type == "DELAY3":
                self.histI1[k] = self.I1
                self.histI2[k] = self.I2
                self.histI3[k] = self.I3
            self.k += 1
        #text += "{}".format(self.val)
        #print(text)

    def __repr__(self):
        value = "None"
        if self.val != None:
            value = "{:.03f}".format(self.val)
        return "{0.name:<8} {3} IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()),
                                                             ",".join(self.get_succ_name()), value)

    def f_smooth(self, flow, constant):
        self.node = flow
        self.cst = constant
        if not self.hist[0]:
            if self.type == "SMOOTH":
                self.val = flow
            if self.type == "DELAY3":
                self.val = flow
                self.I1 = self.I2 = self.I3 = flow * constant / 3


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


class Hypergraph():
    def __init__(self, nodes=[]):
        self.nodes = {n.name: n for n in nodes}
        self.nbrank = None
        self.nodesrank = None
        self.stocks = [n for n in nodes if type(n) == NodeStock]

    def __repr__(self):
        return "\n".join([str(v) for c,v in self.nodes.items()])

    def add_node(self, node):
        if node.name in self.nodes:
            print("Le Node {} existe déjà. Modifier la modélisation :".format(node.name))
            print(self.nodes[node.name])
            raise ErrorNodeAlreadyExists()
        self.nodes[node.name] = node
        if type(node) == NodeStock: self.stocks.append(node)

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_edge(self, f, x_target, x_s):
        x_target.set_cons(f, x_s)

    def eval(self, ts):
        for ns in self.nodesrank:
            ns.eval(ts)

    def run(self, nbpas, ts):
        for i in range(nbpas):
            self.eval(ts)
        for stock in self.stocks:
            stock.hist.pop()

    def cond(n): return type(n) == NodeFlow or type(n) == NodeSmooth
     
    def sub_graph_vertex(self, cond):
        d2 = [name for name, n in self.nodes.items() if cond(n)]
        d1 = {name : i for i, name in enumerate(d2)}
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
        
    def set_rank(self):
        d2, gM, gP = self.sub_graph_vertex(lambda x : type(x) != NodeStock and type(x) != NodeConstant or (type(x) == NodeStock and not x.val))
        #d2, gM, gP = self.sub_graph_vertex(lambda x: type(x) == NodeSmooth or (type(x) == NodeFlow and not x.val))
        size = len(d2)
        dM = [len(gi) for gi in gM]
        S0 = [i for i,di in enumerate(dM) if di == 0]
        r = [None]*size
        def rang_rec(Sk, k):
            Sk1 = []
            for i in Sk:
                r[i] = k
                for j in gP[i]:
                    dM[j] -= 1
                    if dM[j] == 0:
                        Sk1.append(j)
            if len(Sk1) > 0 :
                return rang_rec(Sk1, k+1)
        rang_rec(S0, 0)
        self.nbrank = max(r) + 1
        self.nodesrank = [self.nodes[d2[j]] for _,j in sorted([(ri, i) for i, ri in enumerate(r)])]
        self.nodesrank += self.stocks