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
        if self.val is not None:
                value = "{0.val:.03f} ".format(self)
        return "{0.name:<8} {3} ({0.t:<10}) IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)

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

    def eval(self, save):
        # text = "{}:{}->".format(self.name, self.val)
        self.val = self.cons(*[p.val for p in self.pred])
        if save:
            self.hist.append(self.val)
        #text += "{}".format(self.val)
        #print(text)


class NodeFlow(NodeStock):
    def __init__(self, name, val=None, hg=None):
        super().__init__(name, val, hg)


class NodeSmooth(Node):
    def __init__(self, name, t, size, val=None, initial=None, hg=None):
        super().__init__(name, val, hg)
        self.type = t
        self.hist = [None] * size
        self.hist[0] = val
        self.initial = initial
        if t == "SMOOTH3":
            self.I1 = val
            self.histI1 = [None] * size
            self.histI1[0] = val
            self.I2 = val
            self.histI2 = [None] * size
            self.histI2[0] = val
        if t == "DELAY3":
            self.I1 = None
            self.histI1 = [None] * size
            self.I2 = None
            self.histI2 = [None] * size
            self.I3 = None
            self.histI3 = [None] * size

    def eval(self, node, ts, dt, k, save):
        text = "{}:{}->".format(self.name, self.val)
        if self.type == "SMOOTH":
            self.val += (node.val-self.val) * ts / dt
        if self.type == "SMOOTHI":
            if len(self.hist) == 1:
                self.val += (node.val - self.initial) * ts / dt
            else:
                self.val += (node.val - self.val) * ts / dt
        if self.type == "SMOOTH3":
            dl = dt/3
            self.val += (self.I1 - self.val) * ts / dl
            self.I1 += (self.I2 - self.I1) * ts / dl
            self.I2 += (node.val - self.I2) * ts / dl
        if self.type == "DELAY3":
            dl = dt / 3
            if self.I1 is None:
                self.I1 = dl * node.val
                self.I2 = self.I1
                self.I3 = self.I1
            self.val = self.I1 / dl
            self.I1 += (self.I2 / dl - self.I1) * ts
            self.I2 += (self.I3 / dl - self.I2) * ts
            self.I3 += (node.val - self.I3) * ts
        if save:
            self.hist[k] = self.val
            if self.type == "SMOOTH3":
                self.histI1[k] = self.I1
                self.histI2[k] = self.I2
            if self.type == "DELAY3":
                self.histI1[k] = self.I1
                self.histI2[k] = self.I2
                self.histI3[k] = self.I3
        text += "{}".format(self.val)
        print(text)


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
            value = "{0.val:.03f} ".format(self)
        return "{0.name:<8} {3} ({0.t:<10}) IN: {1:<20} OUT: {2}".format(self, ",".join(self.get_pred_name()), ",".join(self.get_succ_name()), value)


class Hypergraph():
    def __init__(self, nodes=[]):
        self.nodes = {n.name: n for n in nodes}
        self.nbrank = None
        self.nodesrank = None
        self.terminaux = [n for n in nodes if type(n) == NodeStock]

    def __repr__(self):
        return "\n".join([str(v) for c,v in self.nodes.items()])

    def add_node(self, node):
        if node.name in self.nodes:
            print("Le Node {} existe déjà. Modifier la modélisation :".format(node.name))
            print(self.nodes[node.name])
            raise ErrorNodeAlreadyExists()
        self.nodes[node.name] = node
        if type(node) == NodeStock: self.terminaux.append(node)

    def add_nodes(self, nodes):
        for n in nodes:
            self.add_node(n)

    def add_edge(self, f, x_target, x_s):
        x_target.set_cons(f, x_s)

    def eval(self, save):
        for ns in self.nodesrank:
            for n in ns:
                n.eval(save)

    def eval2(self, t, y, save=False):
        for i, n in enumerate(self.terminaux):
            n.val = y[i]
        self.eval(save)
        return np.array([n.val for n in self.terminaux])

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
        d2, gM, gP = self.sub_graph_vertex(lambda x : type(x) == NodeFlow or type(x) == NodeSmooth)
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
        print(d2)
        print(r)
        self.nbrank = max(r) + 1
        #self.nodesrank = [[] for _ in range(self.nbrank)]
        self.nodesrank = [j for _,j in sorted([(ri, i) for i, ri in enumerate(r)])]
        #for i,ri in enumerate(r):
        #    self.nodesrank[ri].append(self.nodes[d2[i]])
        #self.nodesrank.append(self.terminaux)
        self.nodesrank += self.terminaux

        
    def set_rank2(self):
        d2 = [name for name, n in self.nodes.items() if type(n) != NodeConstant]
        d1 = {name : i for i, name in enumerate(d2)}
        size = len(d2)
        gM = [[] for _ in range(size)]
        gP = [[] for _ in range(size)]
        for name in d2:
            n = self.nodes[name]
            gM[d1[name]] = [d1[u.name] for u in n.pred if type(u) == NodeFlow or type(u) == NodeFlow]
            if type(n) != NodeStock:
                gP[d1[name]] = [d1[u.name] for u in n.succ if type(u) != NodeConstant]
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
        print(r)
        self.nbrank = max(r) + 1
        self.nodesrank = [j for _, j in sorted([(ri, i) for i, ri in enumerate(r)])]
        # for i,ri in enumerate(r):
        #    self.nodesrank[ri].append(self.nodes[d2[i]])
        # self.nodesrank.append(self.terminaux)
        self.nodesrank += self.terminaux


def traj_rungeKutta(x0, f, nbIter, pas):
    nbVar = len(x0)
    x = np.zeros((nbVar, nbIter), float)
    x[:, 0] = x0
    for k in range(nbIter - 1):
        k1 = f(k, x[:, k], k)
        k2 = f(k, x[:, k] + pas / 2 * k1)
        k3 = f(k, x[:, k] + pas / 2 * k2)
        k4 = f(k, x[:, k] + pas * k3)
        x[:, k + 1] = x[:, k] + pas / 6. * (k1 + 2 * k2 + 2 * k3 + k4)
    return x